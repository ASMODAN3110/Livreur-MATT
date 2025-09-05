from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.restaurants import restaurants
from sqlalchemy import select, func
import json

router = APIRouter(prefix="/recherche_des_restaurants", tags=["recherche_des_restaurants"])

# Fonction utilitaire pour convertir un objet restaurant en dictionnaire
def restaurant_to_dict(r):
    return {
        "id": r.id,
        "nom": r.nom,
        "localisation": r.localisation,
        "email": r.email,
        "numero": r.numero,
        "type_de_cuisine": r.type_de_cuisine,
        "description": r.description,
        "lien_logo": r.lien_logo,
        "jour_d_inscription": str(r.jour_d_inscription),
        "date_et_heure_de_connexion": str(r.date_et_heure_de_connexion),
        "date_et_heure_fin_connexion": str(r.date_et_heure_fin_connexion),
    }

# WebSocket de recherche de restaurants
@router.websocket("/recherche")
async def websocket_connexion(websocket: WebSocket):
    await websocket.accept()

    async with AsyncSessionLocal() as db:
        try:
            while True:
                data = await websocket.receive_text()
                contenu = json.loads(data)

                if contenu.get("type") == "recherche_de_restaurant":
                    Texte_Saisi = contenu.get("Texte_Saisi", "").strip()
                    Tableau_de_restaurant = []  # Initialisation par défaut

                    if len(Texte_Saisi) > 0:
                        stmt = select(restaurants).where(
                            func.lower(restaurants.nom).contains(Texte_Saisi.lower())
                        )
                        result = await db.execute(stmt)
                        Tableau_de_restaurant = result.scalars().all()

                    if Tableau_de_restaurant:
                        restaurants_dicts = [restaurant_to_dict(r) for r in Tableau_de_restaurant]
                        await websocket.send_text(json.dumps({
                            "status": "success",
                            "action": "rien",
                            "message": "restaurant trouvé avec succès",
                            "Tableau_de_restaurant": restaurants_dicts,
                        }))
                    else:
                        await websocket.send_text(json.dumps({
                            "status": "success",
                            "action": "rien",
                            "message": "aucun restaurant n'a pu être trouvé",
                            "Tableau_de_restaurant": [],
                        }))
                else:
                    await websocket.send_text(json.dumps({
                        "status": "error",
                        "message": "Connexion échouée (type de requête invalide)"
                    }))
        except WebSocketDisconnect:
            print("Client déconnecté.")
