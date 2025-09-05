from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.commandes import commandes
from models.livraisons import livraisons
from sqlalchemy import select, and_
from datetime import date, datetime
import json
import asyncio

router = APIRouter(
    prefix="/envoi_de_l_etat_de_la_livraison",
    tags=["envoi_de_l_etat_de_la_livraison"]
)

async def verifie_si_c_est_ma_livraison(db: AsyncSession, livreur_id: int, nom_du_livreur: str , id_de_la_redistribution: str)  -> bool:
      # je récupère la redistribution en question grace a son identifiant
    result = await db.execute(
        select(livraisons).where(livraisons.id_de_la_redistribution == id_de_la_redistribution) # ceci est une requete me permettant de selectionner la redistribution sur laquelle le livreur a cliquer
    )
    ma_livraison = result.scalar_one_or_none() # je recupère la livraison en question et je vais l update

    c_est_ma_livraison = False # par défaut je considère que ce n est pas commande

    if ma_livraison: # si ma livraison existe
        # la première des choses est de vérifier si un autre livreur n a pas déjà accepter la commande pour cela voici ce que je fais
        if ma_livraison.id_du_livreur == livreur_id : # cela veut dire que j ai déjà accepter la commande
              c_est_ma_livraison = True
    
    return c_est_ma_livraison

         
async def accepte_une_livraison(db: AsyncSession, livreur_id: int, nom_du_livreur: str , id_de_la_redistribution: str) -> str:

    action = "" # ceci est une variable qui représente l action a mener pour l interface utilisateur dans certaines conditions

    # je récupère la redistribution en question grace a son identifiant
    result = await db.execute(
        select(livraisons).where(livraisons.id_de_la_redistribution == id_de_la_redistribution) # ceci est une requete me permettant de selectionner la redistribution sur laquelle le livreur a cliquer
    )
    ma_livraison = result.scalar_one_or_none() # je recupère la livraison en question et je vais l update

    if ma_livraison: # si ma livraison existe
        # la première des choses est de vérifier si un autre livreur n a pas déjà accepter la commande pour cela voici ce que je fais
        if ma_livraison.id_du_livreur is None : # cela veut dire qu aucun livreur ne sait positionner sur la redistribution en question
            # je positionne le livreur en question sur cette commande
            ma_livraison.id_du_livreur = int(livreur_id) # j enregistre l identifiant du livreur qui c est positionner dessus et j ai par conséquent accepter la commande
            await db.commit()
            action = "redirection"
        else : # dans le cas contraire  ou cette case n est pas null cela veut simplement dire qu il y a un livreur dessus et que je ne peux plus le prendre
            action = "pas_de_redirection"

    return action # je retourne message

async def verification_de_l_identifiant_du_livreur(db: AsyncSession, livreur_id: int, nom_du_livreur: str , id_de_la_redistribution: str) -> bool :

       # je récupère la redistribution en question grace a son identifiant
    result = await db.execute(
        select(livraisons).where(livraisons.id_de_la_redistribution == id_de_la_redistribution) # ceci est une requete me permettant de selectionner la redistribution sur laquelle le livreur a cliquer
    )
    ma_livraison = result.scalar_one_or_none() # je recupère la livraison en question et je vais l update

    verification_id_livreur = False # par défaut je considère que ce n est pas commande

    if ma_livraison: # si ma livraison existe
       if ma_livraison.id_du_livreur is None :
        verification_id_livreur = True
    
    return verification_id_livreur
   

async def recupere_une_livraison(db: AsyncSession, livreur_id: int, nom_du_livreur: str , id_de_la_redistribution: str) -> bool :
        
    recuperation = False # ici je n ais encore rien récupérer

    # Date + heure actuelle
    aujourdhui = datetime.now()

    # Transformation en string
    aujourdhui_str = aujourdhui.strftime("%Y-%m-%d %H:%M:%S") # je convertis la date en string et en prenant la date d aujourd hui avec ces minutes et ces secondes

    result = await db.execute(
        select(livraisons).where(livraisons.id_de_la_redistribution == id_de_la_redistribution)
    )
    ma_livraison = result.scalar_one_or_none() # je recupère la livraison en question et je vais l update

    if ma_livraison: # si ma livraison existe alors
        # Modification des champs
        if str(ma_livraison.id_du_livreur) == str(livreur_id) : # la personne ne peut que récupérer s il est la personne qui a accepter la livraison
            if ma_livraison.date_de_recuperation_de_la_commande_au_restau is None or ma_livraison.date_de_recuperation_de_la_commande_au_restau == "" :
                ma_livraison.date_de_recuperation_de_la_commande_au_restau = aujourdhui_str 
                await db.commit()
                recuperation = True # ici la récupération est bonne



    return recuperation # ici je retourne pour savoir savoir 

async def verifie_le_mot_de_passe_de_la_recuperation_de_livraison(db: AsyncSession, livreur_id: int, nom_du_livreur: str , id_de_la_redistribution: str , Code_De_Recuperation_De_Commande: str) -> bool :

    # je déclare mon booléan qui me permet de savoir si le mot de passe est vrai est ou faux
    equivalence_de_mot_de_passe = False # je le met a False par défaut qu il n est pas valide
    # maintenant ici je vais d abord vérifier si la livraison à été prise

    # ceci sert a faire le marquage en vérifiant le mot de mot de passe que le livreur a saisi
    
    result = await db.execute(
     select(commandes.code_de_livraison).where(commandes.id.contains(id_de_la_redistribution)) # ceci est une requete me permettant de selectionner les différents code de livraison d une commande
    )
    ma_chaine_de_code_de_livraison = result.scalar_one_or_none() # je recupère ces différents code de livraison sous forme de chaine
    mon_tableau_de_code_de_livraison = ma_chaine_de_code_de_livraison.strip().split("|") # ici j ai mon tableau de code de livraison

    # vu que j ai l identifiant de la redistribution de cette commande je vais maintenant chercher sa position parmi les autres redistributions
    result = await db.execute(
     select(commandes.id).where(commandes.id.contains(id_de_la_redistribution)) # ceci est une requete me permettant de selectionner les différents code de livraison d une commande
    )
    ma_chaine_d_identifiant = result.scalar_one_or_none() # je recupère ces différents code de livraison sous forme de chaine
    mon_tableau_d_identifiant = ma_chaine_d_identifiant.strip("/").split("/") # ici j ai mon tableau d identifiant de commande
    position_de_l_identifiant = None # je met d abord la position de l identifiant a None

    for index_id_redistribution ,id_redistribution in enumerate(mon_tableau_d_identifiant) : # je parcours mon tableau d identifiant
        if id_redistribution == id_de_la_redistribution :
            position_de_l_identifiant = index_id_redistribution # j enregistre la position de mon identifiant
            break # je casse la boucle en question
    
    # maintenant que j ai récupérer la position de mon identifiant
    # je récupère le code livraison de ma redistribution

    mon_code_de_livraison = mon_tableau_de_code_de_livraison[position_de_l_identifiant].strip() # récupération de mon code livraison

    if str(mon_code_de_livraison) == str(Code_De_Recuperation_De_Commande) : # alors je peux valider la récupération de la commande

        equivalence_de_mot_de_passe = True # je met que le mot de passe est valide en ce moment

        # ensuite je dois récupérer le code de récupération de cette commande
        # ensuite je dois les comparer si le code de cette commande est le meme que l utilisateur a saisi alors tout est bon
    

    return equivalence_de_mot_de_passe # ici je retourne l état du mot de passe

    # je récupère la livraison au restaurant en question . Pour le noté au niveau de ma base de donnée je dois enregistrer sa date de récupération de commande au restaurant
    # et je signale que je l ai récupéré

@router.websocket("/traiteur_de_livraison")
async def traite_la_livraison(websocket: WebSocket):
    
    await websocket.accept()
    db: AsyncSession = AsyncSessionLocal()
   
    try:
        data = await websocket.receive_text()
        contenu = json.loads(data)
        if contenu.get('type') != 'acceptation_de_la_livraison' and contenu.get('type') != 'recuperation_de_la_livraison' and contenu.get('type') != 'livrer_la_livraison' :
            await websocket.close()
            return

        livreur_id = int(contenu.get('identifiant_du_livreur'))
        nom_du_livreur = contenu.get('nom_du_livreur')
        id_de_la_redistribution = contenu.get('id_de_la_redistribution')
       
        action = ""
        
        if contenu.get('type') == 'acceptation_de_la_livraison' :
         verification_id_livreur = await verification_de_l_identifiant_du_livreur(db,livreur_id,nom_du_livreur,id_de_la_redistribution) # ceci me permet de savoir si un identifiant du livreur a été insérer au moment ou un autre veut la validé
         if verification_id_livreur : # si rien n a été insérer alors tout va bien je peux accepter tranquillement cette commande  
           action =  await accepte_une_livraison(db,livreur_id,nom_du_livreur,id_de_la_redistribution) # ceci est une variable qui représente l action a mener pour l interface utilisateur dans certaines conditions
         else : # dans le cas contraire ou ça été déjà accepter alors il ne peut accepter cette livraison
            action = "pas_de_redirection"
             
        if contenu.get('type') == 'recuperation_de_la_livraison' : # je vérifie que le livreur a réellement appuyer sur le bouton qui sert a marquer qu une commande à été récupéré au restaurant
            # maintenant ici je vérifie que la livraison a appartient bien au livreur qui est entrain de regarder la livraison
            si_c_est_ma_livraison = await verifie_si_c_est_ma_livraison(db,livreur_id,nom_du_livreur,id_de_la_redistribution) # ce booléan va me permettre de dire si la livraison sur laquelle je suis va à été prise par moi ou pas
            # si c est ma livraison alors  
            if si_c_est_ma_livraison : # si c est moi qui est accepter cette livraison alors je peux la récupérer

                Code_De_Recuperation_De_Commande = contenu.get('Code_De_Recuperation_De_Commande') # récupération du code de la commande du restaurant 
                equivalence_de_mot_de_passe = await verifie_le_mot_de_passe_de_la_recuperation_de_livraison(db,livreur_id,nom_du_livreur,id_de_la_redistribution,Code_De_Recuperation_De_Commande) # cette variable me permet de vérifier si le mot de passe entrer par le livreur est le meme de la commande

                if equivalence_de_mot_de_passe : # si les mots de passe sont équivalents c est a dire égaux alors
                      # ensuite je dois récupérer le code de récupération de cette commande
                      # ensuite je dois les comparer si le code de cette commande est le meme que l utilisateur a saisi alors tout est bon
                      recuperation = await recupere_une_livraison(db,livreur_id,nom_du_livreur,id_de_la_redistribution) # ici je récupère l etat de la
                      if recuperation : # alors je viens de récupérer la commande au restaurant
                        action = "recuperation_success"
                    
                else : # alors la livraison avait déjà été récupérer
                        action = "recuperation_failed"


            else : # la commande à été par un livreur qui n est pas moi
                    # alors ici je dois dire que la commande à été prise par un autre livreur donc je ne peux pas la récupéré 
                action = "pas_acceptation_faite"
                # print("la livraison sera accepter")

        await websocket.send_text(json.dumps({
            'status': 'success',
            'action': action,
            #'Mon_Tableau_De_Commande_Journaliere': Mon_Tableau_De_Commande_Journaliere
        }))
        

    except Exception as e:
        print(f"Erreur WebSocket: {e}")
    finally:
        
        await db.close()
