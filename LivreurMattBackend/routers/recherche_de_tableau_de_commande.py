from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.commandes import commandes
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

router = APIRouter(
    prefix="/information_du_tableau_de_commande",
    tags=["information_du_tableau_de_commande"]
)

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
        asyncio.create_task(listen_commande_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_acceptation_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_annulation_to_postgres(listeners_stop_event))
    ]
    print("Listeners démarrés (singleton) pour le tableau de commandes.")

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

async def listen_commande_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'nouvelle_commande'")
    await conn.add_listener('nouvelle_commande', update_commande_tableau_de_commande)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'nouvelle_commande'")
        await conn.close()

async def listen_acceptation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_acceptation'")
    await conn.add_listener('update_acceptation', update_commande_tableau_de_commande)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_acceptation'")
        await conn.close()

async def listen_annulation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_annulation'")
    await conn.add_listener('update_annulation', update_commande_tableau_de_commande)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_annulation'")
        await conn.close()

def _parse_date_for_sort(d):
    """Helper pour parser les dates de différentes formats."""
    if d is None:
        return datetime.min

    if isinstance(d, datetime):
        return d

    if isinstance(d, (int, float)):
        try:
            return datetime.fromtimestamp(d, tz=timezone.utc)
        except Exception:
            return datetime.min

    s = str(d).strip()
    if not s:
        return datetime.min

    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S%z"
    ]

    for fmt in formats:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue

    try:
        return datetime.fromisoformat(s)
    except Exception:
        return datetime.min

def trier_mon_tableau_par_date_desc(tableau):
    """Trie un tableau de commandes par date décroissante."""
    tableau.sort(key=lambda item: _parse_date_for_sort(item.get('date')), reverse=True)
    return tableau

async def update_commande_tableau_de_commande(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        id_de_commande = data.get("id")
        if not id_de_commande:
            return

        parties = id_de_commande.strip("/").split("/")
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and p.split("-")[1].isdigit()}

        for rest_id in restaurants_concernes:
            nom_du_restaurant = active_nom_de_restaurant.get(rest_id)
            if not nom_du_restaurant:
                continue

            db = AsyncSessionLocal()
            try:
                Mon_Tableau_De_Commande = await trouve_les_commandes(db, rest_id, nom_du_restaurant)
                webs = list(active_websockets.get(rest_id, []))
                message = json.dumps({
                    "status": "update",
                    "Mon_Tableau_De_Commande": Mon_Tableau_De_Commande
                })

                for ws in webs:
                    try:
                        await ws.send_text(message)
                    except Exception as e:
                        print("Erreur en envoyant au websocket:", e)
                        try:
                            active_websockets[rest_id].remove(ws)
                        except ValueError:
                            pass
            finally:
                await db.close()

    except Exception as e:
        print(f"Erreur dans update_commande_tableau_de_commande: {e}")

async def trouve_les_commandes(db: AsyncSession, rest_id: int, nom_du_restaurant: str) -> List[dict]:
    """Récupère et formate les commandes pour un restaurant donné."""
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_restaurant = []
    for commande in toutes_les_commandes:
        # Vérifie si la commande concerne ce restaurant via acceptation ou annulation
        if (commande.acceptation and str(rest_id) in [a.split("|")[0].strip() for a in commande.acceptation.strip("/").split("/") if a]) or \
           (commande.annulation and str(rest_id) in [a.split("|")[0].strip() for a in commande.annulation.strip("/").split("/") if a]):
            commandes_du_restaurant.append(commande)

    Mon_Tableau_De_Commande = []
    base_url = f"http://{addresse_ip}:{port_frontend}/restaurants"

    for commande in commandes_du_restaurant:
        sous_commandes = commande.id.strip("/").split("/")
        for index_sous_commande, sous_commande in enumerate(sous_commandes):
            if sous_commande.strip().split("-")[1] != str(rest_id):
                continue

            # Récupération des informations
            facture_result = await db.execute(
                select(factures).where(factures.id_de_la_commande == commande.id)
            )
            facture = facture_result.scalars().first()
            prix_total = facture.prix_total.strip("/").split("/")[index_sous_commande]

            # Plats de la commande
            liste_plats = []
            for plat_info in commande.plat.strip("/").split("/"):
                id_plat, quantite = map(int, plat_info.split(':'))
                
                plat_result = await db.execute(
                    select(plats).where(plats.id == id_plat)
                )
                plat = plat_result.scalars().first()
                
                if plat.id_du_restaurant != rest_id:
                    continue

                personnalisation_result = await db.execute(
                    select(personnalisation_plat.description).where(
                        and_(
                            personnalisation_plat.id_redistribution == sous_commande,
                            personnalisation_plat.id_du_plat == id_plat
                        )
                    )
                )
                personnalisation = personnalisation_result.scalars().first()

                img_enc = quote(plat.lien_image)
                liste_plats.append({
                    'mon_lien': f"{base_url}/{quote(str(rest_id))}/{quote(nom_du_restaurant)}/images_des_plats/{img_enc}",
                    'nom': plat.nom,
                    'prix_unitaire': plat.prix,
                    'quantite': quantite,
                    'prix_total': plat.prix * quantite,
                    'personnalisation': personnalisation
                })

            # Informations client
            client_result = await db.execute(
                select(utilisateurs.nom).where(
                    utilisateurs.id == int(commande.id_de_l_utilisateur)
                )
            )
            nom_client = client_result.scalars().first()

            # État de la commande
            etat = 'En Attente'
            if commande.acceptation and str(rest_id) in [a.split("|")[0].strip() for a in commande.acceptation.strip("/").split("/") if a]:
                etat = 'Validé'
            elif commande.annulation and str(rest_id) in [a.split("|")[0].strip() for a in commande.annulation.strip("/").split("/") if a]:
                etat = 'Refusé'

            Mon_Tableau_De_Commande.append({
                'photo': f"{base_url}/MATT_COMMANDE.jpg",
                'titre': f"commande {len(Mon_Tableau_De_Commande)+1}",
                'prix_total': prix_total,
                'nbre_total_de_plat': sum(p['quantite'] for p in liste_plats),
                'nom_du_client': nom_client,
                'etat_de_la_commande': etat,
                'mot_de_passe': commande.code_de_livraison.split('|')[index_sous_commande].strip(),
                'liste_des_plats': liste_plats,
                'identifiant_de_la_commande': commande.id,
                'id_de_la_redistribution': sous_commande,
                'date': commande.date
            })

    trier_mon_tableau_par_date_desc(Mon_Tableau_De_Commande)
    return Mon_Tableau_De_Commande

@router.websocket("/recherche")
async def websocket_recherche_tableau_de_commande_journaliere(websocket: WebSocket):
    await websocket.accept()
    rest_id = None
    db: AsyncSession = AsyncSessionLocal()

    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get('type') != 'recherche_d_info_du_tableau_de_commande':
            await websocket.close()
            return

        rest_id = int(contenu.get('identifiant_du_restaurant'))
        nom_du_restaurant = contenu.get('nom_du_restaurant')

        active_websockets.setdefault(rest_id, []).append(websocket)
        active_nom_de_restaurant[rest_id] = nom_du_restaurant

        Mon_Tableau_De_Commande = await trouve_les_commandes(db, rest_id, nom_du_restaurant)
        await websocket.send_text(json.dumps({
            'status': 'success',
            'action': 'affichage',
            'Mon_Tableau_De_Commande': Mon_Tableau_De_Commande
        }))

        # Démarrer les listeners singleton
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