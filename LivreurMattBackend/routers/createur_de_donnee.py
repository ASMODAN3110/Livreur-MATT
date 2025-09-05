from fastapi import APIRouter , WebSocket , WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.recette import recette
from models.restaurants import restaurants
from models.admin import admin
from models.allergies import allergies
from models.boissons import boissons
from models.commandes import commandes
from models.commentaires_mood import commentaires_mood
from models.commentaires_plat import commentaires_plat
from models.commentaires_recettes import commentaires_recettes
from models.evenements import evenements
from models.factures import factures
from models.factures_evenements import factures_evenements
from models.ingredients import ingredients
from models.livraisons import livraisons
from models.livreurs import livreurs
from models.messagerie import messagerie
from models.moods import moods
from models.personnalisation_plat import personnalisation_plat
from models.plats import plats
from models.point_matt import point_matt
from models.recette import recette
from models.restaurants import restaurants
from models.supplements import supplements
from models.utilisateurs import utilisateurs
import json

router = APIRouter(prefix="/BD", tags=["BD"])

@router.websocket("/creation_de_donnee") # ceci est le nom de ma route pour la création de mes interfaces
async def websocket_creation_de_donnee(websocket:WebSocket) : # ceci est le nom de ma fonction qui me permet de créer les données en base de donnée dans toutes les tables
    await websocket.accept() # j accepte mon websocket dans cette fonction
    db : AsyncSession = AsyncSessionLocal() # création de ma session local

    try :

        while True :
            data = await websocket.receive_text()
            contenu = json.loads(data)

            if contenu.get("type") == "enregistrement" :

                await websocket.send_text(json.dumps({
                    "status" : "success" ,
                    "message" : "les données ont bien été enregistrés"
                }))

    except WebSocketDisconnect :
        # Ici la personne c est déconnecté
        pass

    finally :
        await db.close() # fermeture de la base de donnée


