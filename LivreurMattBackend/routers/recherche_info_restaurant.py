from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.restaurants import restaurants
from sqlalchemy import select
import json

router = APIRouter(prefix="/information_d_un_restaurant", tags=["information_d_un_restaurant"])



@router.websocket("/recherche")
async def websocket_connexion(websocket: WebSocket):
     await websocket.accept() # j accepte mon websocket dans cette fonction
     db : AsyncSession = AsyncSessionLocal()

     try:

        while True:
            data = await websocket.receive_text()
            contenu = json.loads(data)


            if contenu.get("type") == "recherche_d_info_personnel":

                identifiant_du_restaurant = contenu.get("identifiant_du_restaurant")
                identifiant_du_restaurant = int(identifiant_du_restaurant) # ici je convertis l identifiant que je reçois pour reste un entier
                
                result = await db.execute(
                    select(restaurants).where(restaurants.id == identifiant_du_restaurant)
                )
                restaurant_trouve = result.scalars().first()

                if restaurant_trouve:

                    Info_De_Mon_Restaurant = {

                     "nom" : restaurant_trouve.nom ,
                     "localisation" : restaurant_trouve.localisation ,
                     "numero" : restaurant_trouve.numero , 
                     "email" : restaurant_trouve.email ,
                     "jour_d_inscription" : restaurant_trouve.jour_d_inscription ,
                     "type_de_cuisine" : restaurant_trouve.type_de_cuisine ,
                     "description" : restaurant_trouve.description ,

                    }

                    
                    await websocket.send_text(json.dumps({
                        "status": "success",
                        "message": "recherche effectuée avec succès" ,
                        "action" : "affichage" , 
                        "Info_De_Mon_Restaurant": Info_De_Mon_Restaurant ,

                    }))
                    
                else:

                    await websocket.send_text(json.dumps({
                        "status": "error",
                        "message": "la recherche n a pas été abouti" ,
                        "action" : "affichage" , 
                        "Info_De_Mon_Restaurant" : {

                            "nom" : "" , 
                            "localisation" : "" ,
                            "numero" : "" , 
                            "email" : "" ,
                            "jour_d_inscription" : "" ,
                            "type_de_cuisine" : "" ,
                            "description" : "" ,

                         }

                    }))
            else:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Connexion échouée (type de requête invalide)"
                }))

     except WebSocketDisconnect:
            pass  # Le client s'est déconnecté
     
     finally:
        await db.close()

