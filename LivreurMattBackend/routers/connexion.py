from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.livreurs import livreurs
from sqlalchemy import select
import json

router = APIRouter(prefix="/livreurs_connexion", tags=["livreurs_connexion"])

# Connexion d'un restaurant (enregistrement)
@router.websocket("/connexion")
async def websocket_connexion(websocket: WebSocket):
    await websocket.accept()

    async with AsyncSessionLocal() as db:  # Connexion gérée proprement
        try:
            while True:
                data = await websocket.receive_text()
                contenu = json.loads(data)

                if contenu.get("type") == "connexion":
                    email_du_livreur = contenu.get("email")
                    mot_de_passe = contenu.get("password")

                    result = await db.execute(
                        select(livreurs).where(livreurs.email == email_du_livreur)
                    )
                    livreurs_trouve = result.scalars().first()

                    if livreurs_trouve:
                        if livreurs_trouve.mot_de_passe == mot_de_passe:
                            await websocket.send_text(json.dumps({
                                "status": "success",
                                "action": "redirect",
                                "interface": "Dashboard",
                                "identifiant_du_livreur": livreurs_trouve.id,
                                "nom_du_livreur": livreurs_trouve.nom,
                            }))
                            print("le nom du livreur est :",livreurs_trouve.nom)
                            print("l identifiant du livreur est :",livreurs_trouve.id)
                        else:
                            await websocket.send_text(json.dumps({
                                "status": "error",
                                "message": "Email du livreur ou mot de passe incorrect"
                            }))
                    else:
                        await websocket.send_text(json.dumps({
                            "status": "error",
                            "message": "Email du livreur ou mot de passe incorrect"
                        }))
                else:
                    await websocket.send_text(json.dumps({
                        "status": "error",
                        "message": "Connexion échouée (type de requête invalide)"
                    }))

        except WebSocketDisconnect:
            pass  # Le client s'est déconnecté

