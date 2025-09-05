from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.restaurants import restaurants
from models.commandes import commandes
from models.livraisons import livraisons
from models.plats import plats
from models.factures import factures
from models.utilisateurs import utilisateurs
from models.personnalisation_plat import personnalisation_plat
from sqlalchemy import select, and_
from datetime import date, datetime, timezone
import json
import asyncio
import asyncpg
from typing import Dict, List
from urllib.parse import quote
from .info_bd import connexion_a_ma_bd, addresse_ip, port_frontend

router = APIRouter(prefix="/information_du_tableau_de_plat", tags=["information_du_tableau_de_plat"])

# Dictionnaires pour garder références des WS et noms
active_websockets: Dict[int, List[WebSocket]] = {}
active_nom_de_restaurant: Dict[int, str] = {}

# --- Globals pour listeners singleton ---
listeners_started = False
listeners_stop_event: asyncio.Event = asyncio.Event()
listener_tasks: List[asyncio.Task] = []

async def start_listeners_once():
    """Démarre les listeners PostgreSQL une seule fois pour tout le processus."""
    global listeners_started, listener_tasks, listeners_stop_event
    if listeners_started:
        return
    listeners_started = True
    listener_tasks = [
        asyncio.create_task(listen_plat_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_update_affichage_plat_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_update_disponibilite_plat_to_postgres(listeners_stop_event))
    ]
    print("Listeners démarrés (singleton) pour le tableau de plats.")

async def stop_listeners_once():
    """Arrête proprement les listeners (utiliser seulement au shutdown global si besoin)."""
    global listeners_started, listeners_stop_event, listener_tasks
    if not listeners_started:
        return
    listeners_stop_event.set()
    await asyncio.gather(*listener_tasks, return_exceptions=True)
    listeners_started = False
    listeners_stop_event = asyncio.Event()
    listener_tasks = []
    print("Listeners arrêtés proprement.")

async def listen_plat_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'nouveau_plat'")
    await conn.add_listener('nouveau_plat', update_tableau_de_plat)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'nouveau_plat'")
        await conn.close()

async def listen_update_affichage_plat_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_affichage_d_un_plat'")
    await conn.add_listener('update_affichage_d_un_plat', update_tableau_de_plat)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_affichage_d_un_plat'")
        await conn.close()

async def listen_update_disponibilite_plat_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_disponibilite_d_un_plat'")
    await conn.add_listener('update_disponibilite_d_un_plat', update_tableau_de_plat)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_disponibilite_d_un_plat'")
        await conn.close()

async def update_tableau_de_plat(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}, Payload: {payload}")
    try:
        data = json.loads(payload)
        rest_id_raw = data.get("id_du_restaurant")
        if rest_id_raw is None:
            print("Pas d'id_du_restaurant dans le payload")
            return

        identifiant_du_restaurant = int(rest_id_raw)
        nom_du_restaurant = active_nom_de_restaurant.get(identifiant_du_restaurant)
        if not nom_du_restaurant:
            print("Nom du restaurant non trouvé pour id:", identifiant_du_restaurant)
            return

        db = AsyncSessionLocal()
        try:
            Mon_Tableau_De_Plat = await trouve_les_plats(db, identifiant_du_restaurant, nom_du_restaurant)
        finally:
            await db.close()

        webs = list(active_websockets.get(identifiant_du_restaurant, []))
        message = json.dumps({
            'status': 'update',
            'Mon_Tableau_De_Plat': Mon_Tableau_De_Plat,
        })

        for ws in webs:
            try:
                await ws.send_text(message)
            except Exception as e:
                print("Erreur en envoyant au websocket:", e)
                try:
                    active_websockets[identifiant_du_restaurant].remove(ws)
                except ValueError:
                    pass

    except json.JSONDecodeError:
        print("Payload non JSON:", payload)
    except Exception as e:
        print(f"Erreur dans update_tableau_de_plat: {e}")

async def trouve_les_plats(db: AsyncSession, rest_id: int, nom_du_restaurant: str) -> List[dict]:
    result = await db.execute(select(plats).where(plats.id_du_restaurant == rest_id))
    plats_du_restaurant = result.scalars().all()

    Mon_Tableau_De_Plat = []
    base_url = f"http://{addresse_ip}:{port_frontend}/restaurants"
    rest_id_enc = quote(str(rest_id))
    nom_rest_enc = quote(nom_du_restaurant)

    for plat in plats_du_restaurant:
        img_enc = quote(plat.lien_image)
        base_url_plat = f"{base_url}/{rest_id_enc}/{nom_rest_enc}/images_des_plats/{img_enc}"

        couleur = "green" if plat.affichage == "oui" else "red"
        texte_d_affichage = "afficher" if plat.affichage == "oui" else "désafficher"

        Mon_Tableau_De_Plat.append({
            "id": plat.id,
            "image": base_url_plat,
            "nom": plat.nom,
            "bouton_d_affichage": {
                "largeur": "100%",
                "couleur": couleur,
                "couleur_du_texte": "white",
                "texte": texte_d_affichage,
            },
            "etat_du_switch": plat.disponibilite.strip(),
        })

    return Mon_Tableau_De_Plat

@router.websocket("/recherche")
async def websocket_recherche_tableau_de_plat(websocket: WebSocket):
    await websocket.accept()
    rest_id = None
    db: AsyncSession = AsyncSessionLocal()

    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get('type') != 'recherche_d_info_du_tableau_de_plats':
            await websocket.close()
            return

        rest_id = int(contenu.get('identifiant_du_restaurant'))
        nom_du_restaurant = contenu.get('nom_du_restaurant')

        active_websockets.setdefault(rest_id, []).append(websocket)
        active_nom_de_restaurant[rest_id] = nom_du_restaurant

        Mon_Tableau_De_Plat = await trouve_les_plats(db, rest_id, nom_du_restaurant)
        await websocket.send_text(json.dumps({
            'status': 'success',
            'action': 'affichage',
            'Mon_Tableau_De_Plat': Mon_Tableau_De_Plat,
        }))

        # Démarrer les listeners singleton (non bloquant)
        asyncio.create_task(start_listeners_once())

        # Boucle pour garder la connexion ouverte
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"Erreur WebSocket: {e}")
    finally:
        if rest_id is not None and rest_id in active_websockets:
            try:
                active_websockets[rest_id].remove(websocket)
                if not active_websockets[rest_id]:
                    del active_websockets[rest_id]
                    active_nom_de_restaurant.pop(rest_id, None)
            except ValueError:
                pass
        await db.close()