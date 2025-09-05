from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.plats import plats
import json
import os
import base64
from datetime import datetime

router = APIRouter(prefix="/restaurants_creation_de_plat", tags=["restaurants_creation_de_plat"])

@router.websocket("/createur_de_plat")
async def websocket_createur_de_plat(websocket: WebSocket):
    await websocket.accept()
    db: AsyncSession = AsyncSessionLocal()

    try:
        while True:
            data = await websocket.receive_text()

            # Vérification JSON
            try:
                contenu_dict = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Le message reçu n'est pas un JSON valide."
                }))
                continue

            if contenu_dict.get("type") != "enregistrement":
                continue

            # Extraction des champs
            nom_de_mon_plat = contenu_dict.get("nom_de_mon_plat", "").strip()
            description_de_mon_plat = contenu_dict.get("description_de_mon_plat", "").strip()
            mon_image_en_base64 = contenu_dict.get("image_base64", "")
            identifiant_du_restaurant = contenu_dict.get("identifiant_du_restaurant", "")
            nom_du_restaurant = contenu_dict.get("nom_du_restaurant", "")

            # Prix → vérification
            try:
                prix_de_mon_plat = int(contenu_dict.get("prix_de_mon_plat", 0))
            except (ValueError, TypeError):
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Le champ 'prix' doit être un entier valide."
                }))
                continue

            # === Traitement de l'image ===
            try:
                dossier_racine = "restaurants"
                dossier_restaurant = os.path.join(
                    dossier_racine,
                    str(identifiant_du_restaurant),
                    nom_du_restaurant,
                    "images_des_plats"
                )
                os.makedirs(dossier_restaurant, exist_ok=True)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                nom_fichier_image = f"plat_{timestamp}.png"
                chemin_complet = os.path.join(dossier_restaurant, nom_fichier_image)

                # Extraction du vrai base64 (après "data:image/...;base64,")
                parts = mon_image_en_base64.split(',', 1)
                if len(parts) != 2:
                    raise ValueError("Format de chaîne base64 invalide")
                image_data = parts[1]

                with open(chemin_complet, "wb") as f:
                    f.write(base64.b64decode(image_data))

                lien_image = f"/{chemin_complet}"
            except Exception as e:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": f"Erreur lors de l'enregistrement de l'image : {str(e)}"
                }))
                continue

            # === Enregistrement dans la base ===
            try:
                nouveau_plat = plats(
                    nom=nom_de_mon_plat,
                    prix=prix_de_mon_plat,
                    description=description_de_mon_plat,
                    disponibilite='ferme',
                    affichage='non',
                    lien_image=nom_fichier_image,
                    id_du_restaurant = int(contenu_dict.get('identifiant_du_restaurant'))
                )
                db.add(nouveau_plat)
                await db.commit()

                await websocket.send_text(json.dumps({
                    "status": "success",
                    "message": "Félicitations ! Votre plat a bien été enregistré.",
                    "action": "redirect",
                    "interface": "Barre_De_Navigation",
                    "ecran": "Menu",
                }))
            except Exception as e:
                await db.rollback()
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": f"Erreur lors de l'enregistrement en base : {str(e)}"
                }))

    except WebSocketDisconnect:
        pass

    finally:
        await db.close()
