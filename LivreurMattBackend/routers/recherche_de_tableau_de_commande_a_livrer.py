from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.commandes import commandes
from models.livraisons import livraisons
from models.plats import plats
from models.factures import factures
from models.utilisateurs import utilisateurs
from models.restaurants import restaurants
from models.personnalisation_plat import personnalisation_plat
from sqlalchemy import select, and_ , cast , Date
from datetime import date, datetime, timezone
import json
import asyncio
import asyncpg
from typing import Dict, List
from urllib.parse import quote
from .info_bd import connexion_a_ma_bd, addresse_ip, port_frontend

router = APIRouter(
    prefix="/information_du_tableau_de_commande_a_livrer",
    tags=["information_du_tableau_de_commande_a_livrer"]
)

# Dictionnaires pour garder références des WS et noms
active_websockets: Dict[int, WebSocket] = {}
active_nom_du_livreur: Dict[int, str] = {}
"""
# --- Globals pour listeners singleton ---
listeners_started = False
listeners_stop_event: asyncio.Event = asyncio.Event()
listener_tasks: List[asyncio.Task] = []

async def start_listeners_once():
    #Démarre les listeners PostgreSQL une seule fois pour tout le processus.
    global listeners_started, listener_tasks, listeners_stop_event
    if listeners_started:
        return
    listeners_started = True
    listener_tasks = [
        asyncio.create_task(listen_commande_journaliere_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_acceptation_to_postgres(listeners_stop_event)),
        asyncio.create_task(listen_annulation_to_postgres(listeners_stop_event))
    ]
    print("Listeners démarrés (singleton) pour le tableau de commandes journalières.")

async def stop_listeners_once():
    #Arrête proprement les listeners (utiliser seulement au shutdown global si besoin).
    global listeners_started, listeners_stop_event, listener_tasks
    if not listeners_started:
        return
    listeners_stop_event.set()
    await asyncio.gather(*listener_tasks, return_exceptions=True)
    listeners_started = False
    listeners_stop_event = asyncio.Event()
    listener_tasks = []
    print("Listeners arrêtés proprement.")

async def listen_commande_journaliere_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'nouvelle_commande'")
    await conn.add_listener('nouvelle_commande', update_commande_tableau_de_commande_journaliere)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'nouvelle_commande'")
        await conn.close()

async def listen_acceptation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_acceptation'")
    await conn.add_listener('update_acceptation', update_commande_tableau_de_commande_journaliere)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_acceptation'")
        await conn.close()

async def listen_annulation_to_postgres(stop_event: asyncio.Event):
    conn = await connexion_a_ma_bd()
    print("Listener PostgreSQL activé sur 'update_annulation'")
    await conn.add_listener('update_annulation', update_commande_tableau_de_commande_journaliere)
    try:
        await stop_event.wait()
    finally:
        print("Arrêt du listener PostgreSQL sur 'update_annulation'")
        await conn.close()

def _parse_date_for_sort(d):
    #Helper pour parser les dates de différentes formats.
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
    #Trie un tableau de commandes par date décroissante.
    tableau.sort(key=lambda item: _parse_date_for_sort(item.get('date')), reverse=True)
    return tableau

async def update_commande_tableau_de_commande_journaliere(conn, pid, channel, payload):
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
                Mon_Tableau_De_Commande_Journaliere = await trouve_les_commandes_journaliere(db, rest_id, nom_du_restaurant)
                webs = list(active_websockets.get(rest_id, []))
                message = json.dumps({
                    "status": "update",
                    "Mon_Tableau_De_Commande_Journaliere": Mon_Tableau_De_Commande_Journaliere
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
        print(f"Erreur dans update_commande_tableau_de_commande_journaliere: {e}")

async def trouve_les_commandes_journaliere(db: AsyncSession, rest_id: int, nom_du_restaurant: str) -> List[dict]:
    #Récupère et formate les commandes journalières pour un restaurant donné.
    aujourdhui = date.today()
    result = await db.execute(select(commandes))
    toutes_les_commandes = result.scalars().all()

    commandes_du_jour = []
    for commande in toutes_les_commandes:
        try:
            date_de_commande = datetime.strptime(commande.date.strip(), "%Y-%m-%d %H:%M:%S").date()
            if date_de_commande == aujourdhui:
                parties = commande.id.strip("/").split("/")
                if any(p.split("-")[1] == str(rest_id) for p in parties if p):
                    commandes_du_jour.append(commande)
        except Exception:
            continue

    Mon_Tableau_De_Commande_Journaliere = []
    base_url = f"http://{addresse_ip}:{port_frontend}/restaurants"

    for commande in commandes_du_jour:
        sous_commandes = commande.id.strip("/").split("/")
        for index_sous_commande, sous_commande in enumerate(sous_commandes):
            if sous_commande.strip().split("-")[1] != str(rest_id):
                continue

            # Récupération des informations
            facture_result = await db.execute(
                select(factures).where(factures.id_de_la_commande == commande.id)
            )
            facture = facture_result.scalars().first()
            if not facture:
                continue

            try:
                prix_total = facture.prix_total.strip("/").split("/")[index_sous_commande]
            except (AttributeError, IndexError):
                prix_total = "0"

            # Plats de la commande
            liste_plats = []
            for plat_info in commande.plat.strip("/").split("/"):
                try:
                    id_plat, quantite = map(int, plat_info.split(':'))
                except ValueError:
                    continue

                plat_result = await db.execute(
                    select(plats).where(plats.id == id_plat)
                )
                plat = plat_result.scalars().first()
                if not plat or plat.id_du_restaurant != rest_id:
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
            nom_client = ""
            try:
                client_result = await db.execute(
                    select(utilisateurs.nom).where(
                        utilisateurs.id == int(commande.id_de_l_utilisateur)
                    )
                )
                nom_client = client_result.scalars().first() or ""
            except Exception:
                pass

            # État de la commande
            etat = 'En Attente'
            if commande.acceptation and str(rest_id) in [a.split("|")[0].strip() for a in commande.acceptation.strip("/").split("/") if a]:
                etat = 'Validé'
            elif commande.annulation and str(rest_id) in [a.split("|")[0].strip() for a in commande.annulation.strip("/").split("/") if a]:
                etat = 'Refusé'

            Mon_Tableau_De_Commande_Journaliere.append({
                'photo': f"{base_url}/MATT_COMMANDE.jpg",
                'titre': f"commande {len(Mon_Tableau_De_Commande_Journaliere)+1}",
                'prix_total': prix_total,
                'nbre_total_de_plat': sum(p['quantite'] for p in liste_plats),
                'nom_du_client': nom_client,
                'etat_de_la_commande': etat,
                'mot_de_passe': commande.code_de_livraison.split('|')[index_sous_commande].strip() if commande.code_de_livraison else "",
                'liste_des_plats': liste_plats,
                'identifiant_de_la_commande': commande.id,
                'id_de_la_redistribution': sous_commande,
                'date': commande.date
            })

    trier_mon_tableau_par_date_desc(Mon_Tableau_De_Commande_Journaliere)
    return Mon_Tableau_De_Commande_Journaliere
"""

def commandes_to_dict(commande):
    return {
        "id": commande.id,
        "id_de_l_utilisateur": commande.id_de_l_utilisateur,
        "plat": commande.plat,
        "date": str(commande.date),  # convertir date en str
        "localisation": commande.localisation,
        "acceptation": commande.acceptation,
        "annulation": commande.annulation,
        "code_de_livraison": commande.code_de_livraison,
        "destination": commande.destination,
        "code_utilisateur": commande.code_utilisateur
    }


"""
  const orderData = {
    id: orderId,
    customerName: 'Marie Dubois',
    customerPhone: '+237 6 12 34 56 78',
    address: '15 Rue de la Paix, 75001 Paris',
    items: [
      {name: 'Pizza Margherita', quantity: 1},
      {name: 'Pizza 4 Fromages', quantity: 1},
      {name: 'Coca Cola 33cl', quantity: 2},
    ],
    mattPoints: '45 Points MATT',
    status: 'en_attente',
   
  };

"""

async def trouve_les_plats_d_une_redistribution( db: AsyncSession, identifiant_du_livreur: int, nom_du_livreur: str, toutes_les_commandes_en_attente_de_livraison: List[dict], tous_les_id_de_la_redistribution: List[str] ) -> dict:
    """
    Cette méthode permet de récupérer les noms des plats et leurs quantités
    pour chaque redistribution.
    """
    liste_plats_de_chaque_redistribution = {}

    for compteur_de_redistribution, redistribution in enumerate(toutes_les_commandes_en_attente_de_livraison):
        id_de_la_redistribution = tous_les_id_de_la_redistribution[compteur_de_redistribution]
        rest_id = id_de_la_redistribution.strip().split("-")[1]

        for plat_info in redistribution.plat.strip("/").split("/"):
            id_plat, quantite = map(int, plat_info.split(':'))

            plat_result = await db.execute(
                select(plats.nom).where(
                    and_(
                        plats.id_du_restaurant == int(rest_id),
                        plats.id == id_plat
                    )
                )
            )

            nom_du_plat = plat_result.scalars().first()

            #  Initialiser la clé si elle n’existe pas
            if id_de_la_redistribution not in liste_plats_de_chaque_redistribution:
             liste_plats_de_chaque_redistribution[id_de_la_redistribution] = []


            liste_plats_de_chaque_redistribution[id_de_la_redistribution].append({
                "name": nom_du_plat,
                "quantity": quantite,
            })

      

    return liste_plats_de_chaque_redistribution



async def trouve_les_commandes_a_livrer(db: AsyncSession, identifiant_du_livreur: int, nom_du_livreur: str) -> List[dict]:

    # le plan est simple pour trouver les commandes a livrer , il faut suivre les étapes suivantes
    # 1 . chercher toutes les livraisons dans la table livraisons qui n ont pas un identifiant de livreur car si une commande a un identifiant de livreur cela veut simplement dire qu un livreur l a accepter pour sa course
    # 2 . récupérer son identifiant de redistribution et aller le chercher dans la table de commande
    # 3 . comparer la date de cette identifiant si la date correspond a celle d aujourd hui récupérer les informations de cette commande qui vont me servir et ceux sont ces informations que je vais utiliser pour afficher les livraisons a faire ajourd hui 

    #Récupère et formate les commandes journalières pour un restaurant donné.

    aujourdhui = date.today()
    # 1 . je cherche toutes les livraisons dans la table livraisons qui n ont pas un identifiant
    result = await db.execute(select(livraisons).where(livraisons.id_du_livreur.is_(None))) # requete me permettant de rechercher toutes les livraisons en attente
    
    toutes_les_livraisons_en_attente = result.scalars().all() # je stocke cela dans un tableau de livraisons en attente

    # 2 . récupérer chacun de ces identifiants de redistribution et aller le chercher dans la table commande
    toutes_les_commandes_en_attente_de_livraison = [] # cette liste va contenir toutes les livraisons que les livreurs doivent faire lors de cette journée
    tous_les_id_de_la_redistribution = [] # cette liste va contenir tous les identifiants de redistribution
    for livraison in toutes_les_livraisons_en_attente : # parcours de ma boucle de livraisons en attente
        result = await db.execute( select(commandes).where( and_(commandes.id.contains(livraison.id_de_la_redistribution),cast(commandes.date, Date) == aujourdhui) ) )# pour chacune des livraisons je récupère
        commande_en_attente_de_livraison = result.scalars().first()
        if commande_en_attente_de_livraison is not None :
            toutes_les_commandes_en_attente_de_livraison.append(commande_en_attente_de_livraison) # recupération de toutes mes commandes du jour
            tous_les_id_de_la_redistribution.append(livraison.id_de_la_redistribution) # récupération de toutes les identifiants de redistribution

    # 3 . ici j affiche les commandes du jour 

    print("voici mes commandes du jour",  toutes_les_commandes_en_attente_de_livraison)

    # bon maintenant ici je vais maintenant chercher a récupérer le nom de chaque plat de cette commande et sa quantité
    
    return toutes_les_commandes_en_attente_de_livraison

async def trouve_les_commandes_d_un_livreur_en_cours(db: AsyncSession, identifiant_du_livreur: int, nom_du_livreur: str) -> List[dict]:

    # le plan est simple pour trouver les commandes a livrer , il faut suivre les étapes suivantes
    # 1 . chercher toutes les livraisons dans la table livraisons qui n ont pas un identifiant de livreur car si une commande a un identifiant de livreur cela veut simplement dire qu un livreur l a accepter pour sa course
    # 2 . récupérer son identifiant de redistribution et aller le chercher dans la table de commande
    # 3 . comparer la date de cette identifiant si la date correspond a celle d aujourd hui récupérer les informations de cette commande qui vont me servir et ceux sont ces informations que je vais utiliser pour afficher les livraisons a faire ajourd hui 

    #Récupère et formate les commandes journalières pour un restaurant donné.

    aujourdhui = date.today()
    # 1 . je cherche toutes les livraisons dans la table livraisons qui n ont pas un identifiant
    result = await db.execute(select(livraisons).where( and_(livraisons.id_du_livreur == identifiant_du_livreur, livraisons.date_de_livraison.is_(None) ))  ) # requete me permettant de rechercher toutes les livraisons qu un livreur a dit qu il doit livrer et que son client n a pas encore reçu
    
    toutes_les_livraisons_en_cours_d_un_livreur = result.scalars().all() # je stocke cela dans un tableau de livraisons en cours d un livreur

    # 2 . récupérer chacun de ces identifiants de redistribution et aller le chercher dans la table commande
    toutes_les_commandes_en_attente_de_livraison = [] # cette liste va contenir toutes les livraisons que les livreurs doivent faire lors de cette journée
    tous_les_id_de_la_redistribution = [] # cette liste va contenir tous les identifiants de redistribution
    for livraison in toutes_les_livraisons_en_cours_d_un_livreur : # parcours de ma boucle de livraisons en cours d un livreur
        result = await db.execute( select(commandes).where( and_(commandes.id.contains(livraison.id_de_la_redistribution),cast(commandes.date, Date) == aujourdhui) ) )# pour chacune des livraisons je récupère
        commande_en_attente_de_livraison = result.scalars().first()
        if commande_en_attente_de_livraison is not None :
            toutes_les_commandes_en_attente_de_livraison.append(commande_en_attente_de_livraison) # recupération de toutes mes commandes du jour
            tous_les_id_de_la_redistribution.append(livraison.id_de_la_redistribution) # récupération de toutes les identifiants de redistribution

    # 3 . ici j affiche les commandes du jour 

    print("voici mes commandes a livrer est",  toutes_les_commandes_en_attente_de_livraison)

    # bon maintenant ici je vais maintenant chercher a récupérer le nom de chaque plat de cette commande et sa quantité
    
    return toutes_les_commandes_en_attente_de_livraison


async def trouve_les_id_des_redistributions_d_un_livreur_en_cours(db: AsyncSession, identifiant_du_livreur: int, nom_du_livreur: str) -> List[dict]:

    # le plan est simple pour trouver les commandes a livrer , il faut suivre les étapes suivantes
    # 1 . chercher toutes les livraisons dans la table livraisons qui n ont pas un identifiant de livreur car si une commande a un identifiant de livreur cela veut simplement dire qu un livreur l a accepter pour sa course
    # 2 . récupérer son identifiant de redistribution et aller le chercher dans la table de commande
    # 3 . comparer la date de cette identifiant si la date correspond a celle d aujourd hui récupérer les informations de cette commande qui vont me servir et ceux sont ces informations que je vais utiliser pour afficher les livraisons a faire ajourd hui 

    #Récupère et formate les commandes journalières pour un restaurant donné.

    aujourdhui = date.today()
    # 1 . je cherche toutes les livraisons dans la table livraisons qui n ont pas un identifiant
    result = await db.execute(select(livraisons).where( and_(livraisons.id_du_livreur == identifiant_du_livreur, livraisons.date_de_livraison.is_(None) ))  ) # requete me permettant de rechercher toutes les livraisons qu un livreur a dit qu il doit livrer et que son client n a pas encore reçu
    
    toutes_les_livraisons_en_cours_d_un_livreur = result.scalars().all() # je stocke cela dans un tableau de livraisons en cours d un livreur

    # 2 . récupérer chacun de ces identifiants de redistribution et aller le chercher dans la table commande
    toutes_les_commandes_en_attente_de_livraison = [] # cette liste va contenir toutes les livraisons que les livreurs doivent faire lors de cette journée
    tous_les_id_de_la_redistribution = [] # cette liste va contenir tous les identifiants de redistribution
    for livraison in toutes_les_livraisons_en_cours_d_un_livreur : # parcours de ma boucle de livraisons en cours d un livreur
        result = await db.execute( select(commandes).where( and_(commandes.id.contains(livraison.id_de_la_redistribution),cast(commandes.date, Date) == aujourdhui) ) )# pour chacune des livraisons je récupère
        commande_en_attente_de_livraison = result.scalars().first()
        if commande_en_attente_de_livraison is not None :
            toutes_les_commandes_en_attente_de_livraison.append(commande_en_attente_de_livraison) # recupération de toutes mes commandes du jour
            tous_les_id_de_la_redistribution.append(livraison.id_de_la_redistribution) # récupération de toutes les identifiants de redistribution

    # 3 . ici j affiche les commandes du jour 

    print("voici mes commandes a livrer est",  toutes_les_commandes_en_attente_de_livraison)

    # bon maintenant ici je vais maintenant chercher a récupérer le nom de chaque plat de cette commande et sa quantité
    
    return  tous_les_id_de_la_redistribution



async def trouve_les_id_des_redistributions(db: AsyncSession, identifiant_du_livreur: int, nom_du_livreur: str) -> List[str]:

    # le plan est simple pour trouver les commandes a livrer , il faut suivre les étapes suivantes
    # 1 . chercher toutes les livraisons dans la table livraisons qui n ont pas un identifiant de livreur car si une commande a un identifiant de livreur cela veut simplement dire qu un livreur l a accepter pour sa course
    # 2 . récupérer son identifiant de redistribution et aller le chercher dans la table de commande
    # 3 . comparer la date de cette identifiant si la date correspond a celle d aujourd hui récupérer les informations de cette commande qui vont me servir et ceux sont ces informations que je vais utiliser pour afficher les livraisons a faire ajourd hui 

    #Récupère et formate les commandes journalières pour un restaurant donné.

    aujourdhui = date.today()
    # 1 . je cherche toutes les livraisons dans la table livraisons qui n ont pas un identifiant
    result = await db.execute(select(livraisons).where(livraisons.id_du_livreur.is_(None))) # requete me permettant de rechercher toutes les livraisons en attente
    toutes_les_livraisons_en_attente = result.scalars().all() # je stocke cela dans un tableau de livraisons en attente

    # 2 . récupérer chacun de ces identifiants de redistribution et aller le chercher dans la table commande
    toutes_les_commandes_en_attente_de_livraison = [] # cette liste va contenir toutes les livraisons que les livreurs doivent faire lors de cette journée
    tous_les_id_de_la_redistribution = [] # cette liste va contenir tous les identifiants de redistribution
    for livraison in toutes_les_livraisons_en_attente : # parcours de ma boucle de livraisons en attente
        result = await db.execute( select(commandes).where( and_(commandes.id.contains(livraison.id_de_la_redistribution),cast(commandes.date, Date) == aujourdhui) ) )# pour chacune des livraisons je récupère
        commande_en_attente_de_livraison = result.scalars().first()
        if commande_en_attente_de_livraison is not None :
            toutes_les_commandes_en_attente_de_livraison.append(commande_en_attente_de_livraison) # recupération de toutes mes commandes du jour
            tous_les_id_de_la_redistribution.append(livraison.id_de_la_redistribution) # récupération de toutes les identifiants de redistribution

    # 3 . ici j affiche les commandes du jour 

    print("voici les identifiants de redistribution",  tous_les_id_de_la_redistribution)

    # bon maintenant ici je vais maintenant chercher a récupérer le nom de chaque plat de cette commande et sa quantité
    
    return tous_les_id_de_la_redistribution


async def trouve_le_statut_de_la_livraison(db: AsyncSession, id_de_la_redistribution_trouve: str) -> str: # cette méthode va me permettre de récupérer le statut de livraison d une commande
    # 1. rechercher la livraison en question a travers son identifiant et ou l identifiant du livreur n a pas été défini
    # c est ça qui va nous faire l état En attente de prise en charge
    # 2 . ensuite ou il y a un idenfiant d un livreur en cours de livraison
    # 3 . ensuite ou il y a la date de livraison la livraison est accompli
    result = await db.execute(select(livraisons).where(livraisons.id_de_la_redistribution == id_de_la_redistribution_trouve)) # récupération de la livraison en question a travers son identifiant
    ma_livraison = result.scalars().first() # vu qu il y a qu une seule redistribution donc une seule livraison possible contenant cette identifiant
    
    if ma_livraison.id_du_livreur is None : 
         status =  'en_attente'
    elif ma_livraison.id_du_livreur is not None :
        status = 'en_cours'
    elif ma_livraison.date_de_livraison is not None and ma_livraison.date_de_recuperation_de_la_commande_au_restau is not None :
        status = 'livre'


   
    return status


@router.websocket("/recherche")
async def websocket_recherche_tableau_de_commande_a_livrer(websocket: WebSocket):
    await websocket.accept()
    identifiant_du_livreur = None
    db: AsyncSession = AsyncSessionLocal()

    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get('type') != 'recherche_d_info_du_tableau_de_commande_a_livrer':
            await websocket.close()
            return

        identifiant_du_livreur = contenu.get('identifiant_du_livreur')
        nom_du_livreur = contenu.get('nom_du_livreur')

        print("l identifiant du livreur dans le backend dashboard est : ",identifiant_du_livreur)
        print("nom du livreur dans le backend dashboard est : ",nom_du_livreur)

        active_websockets[identifiant_du_livreur] = websocket
        active_nom_du_livreur[identifiant_du_livreur] = nom_du_livreur

        # Mon_Tableau_De_Commande_Journaliere = await trouve_les_commandes_a_livrer(db, rest_id, nom_du_restaurant)
        Mon_Tableau_De_Commande_A_Livrer = await trouve_les_commandes_a_livrer(db,identifiant_du_livreur,nom_du_livreur)  # ceci représente mon tableau de commande a livrer pour chaque livreur
                
        # Transformer tout le tableau
    
        Mon_Tableau_De_Commande_A_Livrer_dict = [
         commandes_to_dict(c) for c in Mon_Tableau_De_Commande_A_Livrer
        ]
        
        # recupération des plats et des quantités de chaque redistribution

        tous_les_id_de_la_redistribution = await trouve_les_id_des_redistributions(db,identifiant_du_livreur,nom_du_livreur) # je récupère tous les identifiants de redistribution

        Mon_Enregistrement_De_Plat_Par_Redistribution = await trouve_les_plats_d_une_redistribution(db,identifiant_du_livreur,nom_du_livreur,Mon_Tableau_De_Commande_A_Livrer,tous_les_id_de_la_redistribution) 

        print("mon enregistrement de plat par redistribution", Mon_Enregistrement_De_Plat_Par_Redistribution)

        recentOrders = [] # ceci je représente le tableau que je vais renvoyer au niveau de l interface 
        compteur = 0
                     
        for commande in Mon_Tableau_De_Commande_A_Livrer_dict : # pour chacune de mes commandes 
            
            compteur = compteur + 1 
            # Convertir en datetime
            date_commande = datetime.strptime(commande["date"], "%Y-%m-%d %H:%M:%S")

            # Date et heure actuelles
            #maintenant = datetime.now()

            # Différence en minutes
            #diff_minutes = (maintenant - date_commande).total_seconds() / 60

            result = await db.execute( select(utilisateurs.nom).where( utilisateurs.id ==  int(commande["id_de_l_utilisateur"])) )# pour chacune des livraisons je récupère
            nom_du_client = result.scalars().first()

            result = await db.execute( select(utilisateurs.numero).where( utilisateurs.id ==  int(commande["id_de_l_utilisateur"])) )# pour chacune des livraisons je récupère
            numero_du_client = result.scalars().first()

            # extraire les sous-identifiants présents dans commande["id"]
            parts = [p for p in commande.get("id", "").strip("/").split("/") if p]

            prix_de_la_livraison = 0
            id_de_la_redistribution_trouve = ""

            for part in parts:
                # chercher la livraison dont id_de_la_redistribution == part
                res = await db.execute(select(livraisons.prix).where(livraisons.id_de_la_redistribution == part))
                prix = res.scalars().first()
                if prix is not None:
                    prix_de_la_livraison = prix
                    id_de_la_redistribution_trouve = part
                    break
            
            order_time_str = date_commande.strftime("%Y-%m-%d %H:%M:%S")
            articles_de_la_commande =  Mon_Enregistrement_De_Plat_Par_Redistribution[id_de_la_redistribution_trouve] # ce qui me permet de récupérer les différents plats qu il a commandé
            # je trouve l identifiant du restaurant dans lequel il y a cette redistribution
            identifiant_du_resto_dans_la_redistribution = id_de_la_redistribution_trouve.strip().split("-")[1] # je récupère l identifiant du restaurant qui se trouve dans la redistribution
            
            # maintenant je recherche la localisation de ce restaurant pour aider le livreur a le trouver lors d une livraison
            
            result = await db.execute( select(restaurants.localisation).where( restaurants.id ==  int(identifiant_du_resto_dans_la_redistribution) ) )# pour chacune des livraisons je récupère
            localisation_du_restaurant = result.scalars().first() # ceci représente la localisation du restaurant ou le client a commander

            recentOrders.append({
                "id" : compteur ,
                "customerName": nom_du_client , 
                "address" : commande["destination"] ,
                "mattPoints" :  str(prix_de_la_livraison) + " MATT " , 
                "status": await trouve_le_statut_de_la_livraison(db,id_de_la_redistribution_trouve),
                "estimatedTime": "",
                "orderTime":  order_time_str,
                "customerPhone" : numero_du_client ,
                "items" : articles_de_la_commande ,
                "localisation_du_restaurant" : localisation_du_restaurant ,
                "id_de_la_redistribution" : id_de_la_redistribution_trouve

            })


        Nombre_De_Commande_En_Attente_De_Livraison = len(Mon_Tableau_De_Commande_A_Livrer)

        print("voici le nombre de commande qui attende d etre prise en charge",Nombre_De_Commande_En_Attente_De_Livraison)

        Mon_Tableau_De_Statistiques_Recentes = [] # ceci représente mon tableau de statistiques recentes

        Mon_Tableau_De_Commande_En_Cours = await trouve_les_commandes_d_un_livreur_en_cours(db,identifiant_du_livreur,nom_du_livreur) # me permet de récupérer un tableau de commande que le livreur est la pris doit livrer
       
        Mon_Tableau_De_Commande_En_Cours_dict = [
         commandes_to_dict(c) for c in  Mon_Tableau_De_Commande_En_Cours
        ]

        LivreurOrders = [] # ceci je représente le tableau que je vais renvoyer au niveau de l interface 
        compteur_commande_en_cours = 0

        ids_redistributions_en_cours = await trouve_les_id_des_redistributions_d_un_livreur_en_cours(db,identifiant_du_livreur,nom_du_livreur) # je récupère tous les identifiants de redistribution
        Mon_Enregistrement_De_Plat_Par_Redistribution_Du_Livreur = await trouve_les_plats_d_une_redistribution(db,identifiant_du_livreur,nom_du_livreur,Mon_Tableau_De_Commande_En_Cours,ids_redistributions_en_cours) 

        for commande in  Mon_Tableau_De_Commande_En_Cours_dict : # pour chacune de mes commandes 
            
            compteur_commande_en_cours = compteur_commande_en_cours + 1 
            # Convertir en datetime
            date_commande = datetime.strptime(commande["date"], "%Y-%m-%d %H:%M:%S")

            # Date et heure actuelles
            #maintenant = datetime.now()

            # Différence en minutes
            #diff_minutes = (maintenant - date_commande).total_seconds() / 60

            result = await db.execute( select(utilisateurs.nom).where( utilisateurs.id ==  int(commande["id_de_l_utilisateur"])) )# pour chacune des livraisons je récupère
            nom_du_client = result.scalars().first()

            result = await db.execute( select(utilisateurs.numero).where( utilisateurs.id ==  int(commande["id_de_l_utilisateur"])) )# pour chacune des livraisons je récupère
            numero_du_client = result.scalars().first()

            # extraire les sous-identifiants présents dans commande["id"]
            parts = [p for p in commande.get("id", "").strip("/").split("/") if p]

            prix_de_la_livraison = 0
            id_de_la_redistribution_trouve = ""

            for part in parts:
                # chercher la livraison dont id_de_la_redistribution == part
                res = await db.execute(select(livraisons.prix).where(livraisons.id_de_la_redistribution == part))
                prix = res.scalars().first()
                if prix is not None:
                    prix_de_la_livraison = prix
                    id_de_la_redistribution_trouve = part
                    break
            
            order_time_str = date_commande.strftime("%Y-%m-%d %H:%M:%S")
            articles_de_la_commande =  Mon_Enregistrement_De_Plat_Par_Redistribution_Du_Livreur[id_de_la_redistribution_trouve] # ce qui me permet de récupérer les différents plats qu il a commandé
            # je trouve l identifiant du restaurant dans lequel il y a cette redistribution
            identifiant_du_resto_dans_la_redistribution = id_de_la_redistribution_trouve.strip().split("-")[1] # je récupère l identifiant du restaurant qui se trouve dans la redistribution
            
            # maintenant je recherche la localisation de ce restaurant pour aider le livreur a le trouver lors d une livraison
            
            result = await db.execute( select(restaurants.localisation).where( restaurants.id ==  int(identifiant_du_resto_dans_la_redistribution) ) )# pour chacune des livraisons je récupère
            localisation_du_restaurant = result.scalars().first() # ceci représente la localisation du restaurant ou le client a commander

            LivreurOrders.append({
                "id" : compteur_commande_en_cours ,
                "customerName": nom_du_client , 
                "address" : commande["destination"] ,
                "mattPoints" :  str(prix_de_la_livraison) + " MATT " , 
                "status": await trouve_le_statut_de_la_livraison(db,id_de_la_redistribution_trouve),
                "estimatedTime": "",
                "orderTime":  order_time_str,
                "customerPhone" : numero_du_client ,
                "items" : articles_de_la_commande ,
                "localisation_du_restaurant" : localisation_du_restaurant ,
                "id_de_la_redistribution" : id_de_la_redistribution_trouve

            })


        await websocket.send_text(json.dumps({
            'status': 'success',
            'action': 'affichage',
            'Mon_Tableau_De_Commande_A_Livrer': recentOrders ,
            'Mon_Tableau_De_Statistiques_Recentes': Mon_Tableau_De_Statistiques_Recentes , 
            'Nombre_De_Commande_En_Attente_De_Livraison' : Nombre_De_Commande_En_Attente_De_Livraison , 
            'Mon_Tableau_De_Commande_En_Cours' :  LivreurOrders ,

        }))

        # Démarrer les listeners singleton
        # asyncio.create_task(start_listeners_once())

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
        if identifiant_du_livreur is not None and identifiant_du_livreur in active_websockets:
            websocket = active_websockets[identifiant_du_livreur]
            if websocket == websocket:  # tu fermes bien le bon
                del active_websockets[identifiant_du_livreur]
                active_nom_du_livreur.pop(identifiant_du_livreur, None)
        await db.close()
