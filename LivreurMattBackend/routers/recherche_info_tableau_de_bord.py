from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.restaurants import restaurants
from models.commandes import commandes
from models.livraisons import livraisons  # import de la table livraison
from models.plats import plats
from sqlalchemy import select
from datetime import date, datetime
import json
import asyncio
import asyncpg
from typing import Dict, List
from .info_bd import connexion_a_ma_bd

router = APIRouter(prefix="/information_du_tableau_de_bord", tags=["information_du_tableau_de_bord"])

# Dictionnaire pour garder une référence aux WebSockets actives par restaurant
active_websockets: Dict[int, List[WebSocket]] = {}

# --- Globals pour listeners singleton ---
listeners_started = False
listeners_stop_event: asyncio.Event = asyncio.Event()
listener_tasks: List[asyncio.Task] = []

async def start_listeners_once():
    """Démarre les listeners PostgreSQL une seule fois pour tout le processus.
    Ne démarre rien si déjà démarré.
    """
    global listeners_started, listener_tasks, listeners_stop_event
    if listeners_started:
        return
    listeners_started = True
    # create tasks that will wait on listeners_stop_event
    listener_tasks = [
        asyncio.create_task(listen_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_acceptation_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_annulation_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_livraison_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_livraison_date_de_livraison_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_livraison_date_de_recuperation_de_la_commande_au_restau_to_postgres(listeners_stop_event)),
    ]
    print("Listeners démarrés (singleton) pour le tableau de bord.")

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
    # Se connecter à PostgreSQL
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'nouvelle_commande'")
    await conn.add_listener('nouvelle_commande', verifie_la_notification)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL pour cette connexion")
        await conn.close()

async def listen_acceptation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur update_acceptation ")
    await conn.add_listener('update_acceptation', update_acceptation)
    try:
        await stop_event.wait()
    finally:
        print("Arret du listener PostgreSQL pour cette update_acceptation")
        await conn.close()

async def listen_annulation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur update_annulation")
    await conn.add_listener('update_annulation', update_annulation)
    try:
        await stop_event.wait()
    finally:
        print("Arret du listener pour cette update_annulation")
        await conn.close()

async def listen_livraison_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur l émission d une livraison")
    await conn.add_listener('nouvelle_livraison', emission_livraison)
    try:
        await stop_event.wait()
    finally:
        print("Arret du listener pour l émission d une livraison")
        await conn.close()

async def listen_livraison_date_de_livraison_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur les dates de livraison")
    await conn.add_listener('update_date_de_livraison', emission_livraison)
    try:
        await stop_event.wait()
    finally:
        print("Arret du listener pour les dates de livraison")
        await conn.close()

async def listen_livraison_date_de_recuperation_de_la_commande_au_restau_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur les dates de récuperation de la commande au restaurant")
    await conn.add_listener('update_date_de_recuperation_de_la_commande_au_restau', emission_livraison)
    try:
        await stop_event.wait()
    finally:
        print("Arret du listener pour les dates de récuperation de la commande au restaurant")
        await conn.close()


# --- Notification handlers : une session DB par rest_id (pas par websocket) ---
async def emission_livraison(conn, pid, channel, payload):
    print(f"Notification reçue - PID : {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        id_de_la_redistribution = data.get("id_de_la_redistribution")
        if not id_de_la_redistribution:
            return

        # Extraire l'identifiant du restaurant
        try:
            rest_id = int(id_de_la_redistribution.split("-")[1])
        except Exception:
            print("Impossible d'extraire rest_id de id_de_la_redistribution:", id_de_la_redistribution)
            return

        # Calculer stats une seule fois pour ce rest_id
        db = AsyncSessionLocal()
        try:
            stats = await calculer_toutes_les_stats(db, rest_id)
        finally:
            await db.close()

        # Envoyer à tous les websockets actifs pour ce restaurant
        webs = list(active_websockets.get(rest_id, []))
        for ws in webs:
            try:
                await ws.send_text(json.dumps({"status": "update", **stats}))
            except Exception as e:
                # log l'erreur mais ne crée pas de session supplémentaire
                print("Erreur en envoyant au websocket (emission_livraison):", e)

    except Exception as e:
        print(f"Erreur dans l'émission d'une livraison : {e}")


async def update_annulation(conn, pid, channel, payload):
    print(f"Notification reçue - PID : {pid}, Channel: {channel}")
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
        print(f"Erreur dans update annulation : {e}")


async def update_acceptation(conn, pid, channel, payload):
    print(f"Notification reçue - PID : {pid}, Channel: {channel}")
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
        print(f"Erreur dans update acceptation : {e}")


# --- Fonctions de calcul (inchangées dans leur logique, seulement utilisation de la session) ---
async def calculer_total_commandes_du_jour(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    aujourdhui = date.today()
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_jour = []
    for commande in toutes_les_commandes:
        try:
            date_de_commande = datetime.strptime(commande.date.strip(), "%Y-%m-%d %H:%M:%S").date()
            if date_de_commande == aujourdhui:
                commandes_du_jour.append(commande)
        except Exception as e:
            print(f"Erreur de parsing: {commande.date} - {e}")

    result = await db.execute(select(plats.id).where(plats.id_du_restaurant == identifiant_du_restaurant))
    ids_plats_du_restaurant = set(str(id) for id in result.scalars().all())

    total_commandes = 0
    for commande in commandes_du_jour:
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


async def calculer_commandes_validees_du_jour(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    aujourdhui = date.today()
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_jour = []
    for commande in toutes_les_commandes:
        try:
            date_de_commande = datetime.strptime(commande.date.strip(), "%Y-%m-%d %H:%M:%S").date()
            if date_de_commande == aujourdhui:
                commandes_du_jour.append(commande)
        except Exception:
            pass

    total_commandes_valider = 0
    for commande in commandes_du_jour:
        try:
            plat_accepter_str = commande.acceptation.strip().split("/")
            for plat_info in plat_accepter_str:
                id_du_restaurant_accepteur = plat_info.split("|")[0].strip()
                if id_du_restaurant_accepteur == str(identifiant_du_restaurant):
                    total_commandes_valider += 1
                    break
        except Exception:
            pass

    print("Total Des Commandes validées :", total_commandes_valider)
    return total_commandes_valider


async def calculer_commandes_refusees_du_jour(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    aujourdhui = date.today()
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_jour = []
    for commande in toutes_les_commandes:
        try:
            date_de_commande = datetime.strptime(commande.date.strip(), "%Y-%m-%d %H:%M:%S").date()
            if date_de_commande == aujourdhui:
                commandes_du_jour.append(commande)
        except Exception:
            pass

    total_commandes_annuler = 0
    for commande in commandes_du_jour:
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


async def calculer_commandes_en_attentes_du_jour(Nbre_Total_De_Commande: int, Nbre_Total_De_Commande_Accepter: int, Nbre_Total_De_Commande_Refuser: int) -> int:
    return Nbre_Total_De_Commande - Nbre_Total_De_Commande_Accepter - Nbre_Total_De_Commande_Refuser


async def calculer_livraisons_total_du_jour(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(livraisons))
    toutes_les_livraisons = result.scalars().all()

    livraisons_du_restaurant = []
    for livraison in toutes_les_livraisons:
        try:
            identifiant_dans_la_redistribution = livraison.id_de_la_redistribution.strip().split("-")[1]
            if identifiant_dans_la_redistribution == str(identifiant_du_restaurant):
                livraisons_du_restaurant.append(livraison)
        except Exception:
            pass

    aujourdhui = date.today()
    livraisons_du_restaurant_du_jour = []
    for livraison in livraisons_du_restaurant:
        result = await db.execute(select(commandes).where(commandes.id.contains(livraison.id_de_la_redistribution)))
        commande_lie_a_cette_livraison = result.scalars().first()
        if not commande_lie_a_cette_livraison:
            continue
        date_de_commande = datetime.strptime(commande_lie_a_cette_livraison.date.strip(), "%Y-%m-%d %H:%M:%S").date()
        if date_de_commande == aujourdhui:
            livraisons_du_restaurant_du_jour.append(livraison)

    return len(livraisons_du_restaurant_du_jour)


async def calculer_livraisons_total_du_jour_livrer(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(livraisons))
    toutes_les_livraisons = result.scalars().all()

    livraisons_du_restaurant = []
    for livraison in toutes_les_livraisons:
        try:
            identifiant_dans_la_redistribution = livraison.id_de_la_redistribution.strip().split("-")[1]
            if identifiant_dans_la_redistribution == str(identifiant_du_restaurant):
                livraisons_du_restaurant.append(livraison)
        except Exception:
            pass

    aujourdhui = date.today()
    livraisons_du_restaurant_du_jour = []
    for livraison in livraisons_du_restaurant:
        result = await db.execute(select(commandes).where(commandes.id.contains(livraison.id_de_la_redistribution)))
        commande_lie_a_cette_livraison = result.scalars().first()
        if not commande_lie_a_cette_livraison:
            continue
        date_de_commande = datetime.strptime(commande_lie_a_cette_livraison.date.strip(), "%Y-%m-%d %H:%M:%S").date()
        if date_de_commande == aujourdhui:
            livraisons_du_restaurant_du_jour.append(livraison)

    livraisons_du_restaurant_du_jour_livrer = [l for l in livraisons_du_restaurant_du_jour if l.date_de_livraison is not None]
    return len(livraisons_du_restaurant_du_jour_livrer)


async def calculer_livraisons_total_du_jour_en_cours_de_livraison(db: AsyncSession, identifiant_du_restaurant: int) -> int:
    result = await db.execute(select(livraisons))
    toutes_les_livraisons = result.scalars().all()

    livraisons_du_restaurant = []
    for livraison in toutes_les_livraisons:
        try:
            identifiant_dans_la_redistribution = livraison.id_de_la_redistribution.strip().split("-")[1]
            if identifiant_dans_la_redistribution == str(identifiant_du_restaurant):
                livraisons_du_restaurant.append(livraison)
        except Exception:
            pass

    aujourdhui = date.today()
    livraisons_du_restaurant_du_jour = []
    for livraison in livraisons_du_restaurant:
        result = await db.execute(select(commandes).where(commandes.id.contains(livraison.id_de_la_redistribution)))
        commande_lie_a_cette_livraison = result.scalars().first()
        if not commande_lie_a_cette_livraison:
            continue
        date_de_commande = datetime.strptime(commande_lie_a_cette_livraison.date.strip(), "%Y-%m-%d %H:%M:%S").date()
        if date_de_commande == aujourdhui:
            livraisons_du_restaurant_du_jour.append(livraison)

    livraisons_du_restaurant_du_jour_en_cours = [l for l in livraisons_du_restaurant_du_jour if l.date_de_livraison is None and l.date_de_recuperation_de_la_commande_au_restau is not None]
    return len(livraisons_du_restaurant_du_jour_en_cours)


async def calculer_livraisons_total_du_jour_non_prise_en_charge(Nbre_Total_De_Livraison: int, Nbre_Total_De_Livraison_Accepter: int, Nbre_Total_De_Livraison_En_Cours: int) -> int:
    return Nbre_Total_De_Livraison - Nbre_Total_De_Livraison_Accepter - Nbre_Total_De_Livraison_En_Cours


async def calculer_toutes_les_stats(db: AsyncSession, restaurant_id: int) -> dict:
    return {
        "total_de_commande": await calculer_total_commandes_du_jour(db, restaurant_id),
        "total_commandes_valider": await calculer_commandes_validees_du_jour(db, restaurant_id),
        "total_commandes_refuser": await calculer_commandes_refusees_du_jour(db, restaurant_id),
        "total_de_commande_en_attente": await calculer_commandes_en_attentes_du_jour(
            await calculer_total_commandes_du_jour(db, restaurant_id),
            await calculer_commandes_validees_du_jour(db, restaurant_id),
            await calculer_commandes_refusees_du_jour(db, restaurant_id)
        ),
        "total_de_livraison": await calculer_livraisons_total_du_jour(db, restaurant_id),
        "total_de_commande_livraison_livrer": await calculer_livraisons_total_du_jour_livrer(db, restaurant_id),
        "total_de_commande_livraison_en_cours": await calculer_livraisons_total_du_jour_en_cours_de_livraison(db, restaurant_id),
        "total_de_commande_livraison_non_prise_en_charge": await calculer_livraisons_total_du_jour_non_prise_en_charge(
            await calculer_livraisons_total_du_jour(db, restaurant_id),
            await calculer_livraisons_total_du_jour_livrer(db, restaurant_id),
            await calculer_livraisons_total_du_jour_en_cours_de_livraison(db, restaurant_id)
        )
    }


# Handler de notification PostgreSQL
async def verifie_la_notification(conn, pid, channel, payload):
    print(f"Notification reçue - PID: {pid}, Channel: {channel}")
    try:
        data = json.loads(payload)
        id_de_commande = data.get("id")
        if not id_de_commande:
            return

        parties = id_de_commande.split('/')
        restaurants_concernes = {int(p.split("-")[1]) for p in parties if p and len(p.split("-")) > 1 and p.split("-")[1].isdigit()}

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
    rest_id = None  # initialisé pour éviter UnboundLocalError dans finally
    db: AsyncSession = AsyncSessionLocal()

    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get("type") != "recherche_d_info_du_tableau_de_bord":
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
        # Ne pas arrêter les listeners ici (ils sont globaux/shared)
        if rest_id is not None and rest_id in active_websockets:
            try:
                active_websockets[rest_id].remove(websocket)
                if not active_websockets[rest_id]:
                    del active_websockets[rest_id]
            except ValueError:
                pass
        await db.close()
