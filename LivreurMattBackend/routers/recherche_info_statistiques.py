from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.restaurants import restaurants
from models.commandes import commandes
from models.livraisons import livraisons
from models.plats import plats
from models.factures import factures
from sqlalchemy import select
from datetime import date, datetime
import json
import asyncio
import asyncpg
from typing import Dict, List
from .info_bd import connexion_a_ma_bd

router = APIRouter(prefix="/information_du_tableau_des_statistiques", tags=["information_du_tableau_des_statistiques"])

# Dictionnaire pour garder une référence aux WebSockets actives par restaurant
active_websockets: Dict[int, List[WebSocket]] = {}

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
        asyncio.create_task(listen_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_acceptation_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_annulation_to_postgres(listeners_stop_event))
    ]
    print("Listeners démarrés (singleton) pour les statistiques.")

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

async def listen_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'nouvelle_commande' pour les statistiques")
    await conn.add_listener('nouvelle_commande', verifie_la_notification)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL pour cette connexion")
        await conn.close()

async def listen_acceptation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur update_acceptation pour les statistiques")
    await conn.add_listener('update_acceptation', update_acceptation)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener pour update_acceptation")
        await conn.close()

async def listen_annulation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur update_annulation pour les statistiques")
    await conn.add_listener('update_annulation', update_annulation)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener pour update_annulation")
        await conn.close()

async def update_annulation(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        chaine_d_annulation = data.get("annulation")
        if not chaine_d_annulation:
            return

        entries = chaine_d_annulation.split("/")
        liste_de_chaque_annulation = [e.strip() for e in entries if e.strip()]
        
        restaurants_concernes = {
            int(part.split("|")[0].strip())
            for part in liste_de_chaque_annulation
            if "|" in part and part.split("|")[0].strip().isdigit()
        }

        for rest_id in restaurants_concernes:
            db = AsyncSessionLocal()
            try:
                stats = await calculer_toutes_les_stats(db, rest_id)
            finally:
                await db.close()

            webs = list(active_websockets.get(rest_id, []))
            for ws in webs:
                try:
                    await ws.send_text(json.dumps({"status": "update", **stats}))
                except Exception as e:
                    print("Erreur en envoyant au websocket (update_annulation):", e)

    except Exception as e:
        print(f"Erreur dans update_annulation: {e}")

async def update_acceptation(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        chaine_d_acceptation = data.get("acceptation")
        if not chaine_d_acceptation:
            return

        entries = chaine_d_acceptation.split("/")
        liste_de_chaque_acceptation = [e.strip() for e in entries if e.strip()]
        
        restaurants_concernes = {
            int(part.split("|")[0].strip())
            for part in liste_de_chaque_acceptation
            if "|" in part and part.split("|")[0].strip().isdigit()
        }

        for rest_id in restaurants_concernes:
            db = AsyncSessionLocal()
            try:
                stats = await calculer_toutes_les_stats(db, rest_id)
            finally:
                await db.close()

            webs = list(active_websockets.get(rest_id, []))
            for ws in webs:
                try:
                    await ws.send_text(json.dumps({"status": "update", **stats}))
                except Exception as e:
                    print("Erreur en envoyant au websocket (update_acceptation):", e)

    except Exception as e:
        print(f"Erreur dans update_acceptation: {e}")

async def calculer_total_commandes(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    result = await db.execute(select(plats.id).where(plats.id_du_restaurant == identifiant_du_restaurant))
    ids_plats_du_restaurant = set(str(id) for id in result.scalars().all())

    total_commandes = 0
    commandes_de_ce_restaurant = []

    for commande in toutes_les_commandes:
        parties = commande.id.strip("/").split('/')
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and p.split("-")[1].isdigit()}
        for rest_id in restaurants_concernes:
            if rest_id == identifiant_du_restaurant:
                commandes_de_ce_restaurant.append(commande)

    for commande in commandes_de_ce_restaurant:
        try:
            plats_str = commande.plat.strip().split("/")
            for plat_info in plats_str:
                id_plat = plat_info.split(":")[0].strip()
                if id_plat in ids_plats_du_restaurant:
                    total_commandes += 1
                    break
        except Exception as e:
            print(f"Erreur de traitement du champ plat: {commande.plat} - {e}")

    return total_commandes

async def calculer_commandes_validees(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    total_commandes_valider = 0
    commandes_de_ce_restaurant = []

    for commande in toutes_les_commandes:
        parties = commande.id.strip("/").split('/')
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and p.split("-")[1].isdigit()}
        for rest_id in restaurants_concernes:
            if rest_id == identifiant_du_restaurant:
                commandes_de_ce_restaurant.append(commande)

    for commande in commandes_de_ce_restaurant:
        try:
            plat_accepter_str = commande.acceptation.strip().split("/")
            for plat_info in plat_accepter_str:
                id_du_restaurant_accepteur = plat_info.split("|")[0].strip()
                if id_du_restaurant_accepteur == str(identifiant_du_restaurant):
                    total_commandes_valider += 1
                    break
        except Exception:
            pass

    return total_commandes_valider

async def calculer_commandes_refusees(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    total_commandes_annuler = 0
    commandes_de_ce_restaurant = []

    for commande in toutes_les_commandes:
        parties = commande.id.strip("/").split('/')
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and p.split("-")[1].isdigit()}
        for rest_id in restaurants_concernes:
            if rest_id == identifiant_du_restaurant:
                commandes_de_ce_restaurant.append(commande)

    for commande in commandes_de_ce_restaurant:
        try:
            plat_refuser_str = commande.annulation.strip().split("/")
            for plat_info in plat_refuser_str:
                id_du_restaurant_refuseur = plat_info.split("|")[0].strip()
                if id_du_restaurant_refuseur == str(identifiant_du_restaurant):
                    total_commandes_annuler += 1
                    break
        except Exception:
            pass

    return total_commandes_annuler

async def trouve_info_plats(db: AsyncSession, rest_id: int) -> dict:
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_restaurant = []
    for commande in toutes_les_commandes:
        chaine_d_acception = commande.acceptation
        if chaine_d_acception is not None and chaine_d_acception != "":
            liste_d_acceptation = chaine_d_acception.strip("/").split("/")
            for chaque_acceptation in liste_d_acceptation:
                id_str = chaque_acceptation.strip().split("|")[0].strip()
                if id_str.isdigit():
                    resto_accepteur = int(id_str)
                    if resto_accepteur == rest_id:
                        commandes_du_restaurant.append(commande)
                        break

    nombre_de_plat_de_toutes_les_commandes = 0
    argent_total_gagne = 0
    
    for commande in commandes_du_restaurant:
        liste_de_sous = commande.id.strip("/").split("/")
        for index_de_la_sous_commande, sous_commande in enumerate(liste_de_sous):
            if sous_commande.strip()[-1] != str(rest_id):
                continue

            result_facture = await db.execute(
                select(factures).where(factures.id_de_la_commande == commande.id)
            )
            information_de_la_facture = result_facture.scalars().first()
            if information_de_la_facture:
                liste_prix = information_de_la_facture.prix_total.strip("/").split("/")
                if index_de_la_sous_commande < len(liste_prix):
                    prix_total_de_ma_sous_commande = liste_prix[index_de_la_sous_commande]
                    try:
                        argent_total_gagne += int(prix_total_de_ma_sous_commande)
                    except ValueError:
                        pass

            liste_plats = commande.plat.strip("/").split("/")
            for plat in liste_plats:
                try:
                    id_plat, quantite = map(int, plat.split(':'))
                    result_resto = await db.execute(select(plats.id_du_restaurant).where(plats.id == id_plat))
                    if result_resto.scalars().first() == rest_id:
                        nombre_de_plat_de_toutes_les_commandes += quantite
                except Exception:
                    continue

    return {
        "total_de_plat_vendu": nombre_de_plat_de_toutes_les_commandes,
        "total_d_argent": argent_total_gagne
    }

async def calculer_toutes_les_stats(db: AsyncSession, restaurant_id: int) -> dict:
    info_plats = await trouve_info_plats(db, restaurant_id)
    return {
        "total_de_commande": await calculer_total_commandes(db, restaurant_id),
        "total_commandes_valider": await calculer_commandes_validees(db, restaurant_id),
        "total_commandes_refuser": await calculer_commandes_refusees(db, restaurant_id),
        **info_plats
    }

async def verifie_la_notification(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        id_de_commande = data.get("id")
        if not id_de_commande:
            return

        parties = id_de_commande.split('/')
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and p.split("-")[1].isdigit()}

        for rest_id in restaurants_concernes:
            db = AsyncSessionLocal()
            try:
                stats = await calculer_toutes_les_stats(db, rest_id)
            finally:
                await db.close()

            webs = list(active_websockets.get(rest_id, []))
            for ws in webs:
                try:
                    await ws.send_text(json.dumps({"status": "update", **stats}))
                except Exception as e:
                    print("Erreur en envoyant au websocket (verifie_la_notification):", e)

    except Exception as e:
        print(f"Erreur dans verifie_la_notification: {e}")

@router.websocket("/recherche")
async def websocket_recherche_tableau_de_bord(websocket: WebSocket):
    await websocket.accept()
    rest_id = None
    db: AsyncSession = AsyncSessionLocal()

    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get("type") != "recherche_des_statistiques":
            await websocket.close()
            return

        rest_id = int(contenu.get("identifiant_du_restaurant"))
        active_websockets.setdefault(rest_id, []).append(websocket)

        # Envoi initial des stats
        stats = await calculer_toutes_les_stats(db, rest_id)
        await websocket.send_text(json.dumps({
            "status": "success",
            "action": "affichage",
            **stats
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
            except ValueError:
                pass
        await db.close()