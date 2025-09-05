from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.recette import recette
import json
import os
import base64
from datetime import datetime

router = APIRouter(prefix="/restaurants_creation_de_recette", tags=["restaurants_creation_de_recette"])

@router.websocket("/createur_de_recette")
async def websocket_createur_de_recette(websocket: WebSocket):
    await websocket.accept()
    db: AsyncSession = AsyncSessionLocal()

    try:
        while True:
            data = await websocket.receive_text()

            try:
                contenu_dict = json.loads(data)
                if contenu_dict.get("type") != "enregistrement":
                    continue
            except json.JSONDecodeError:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Le message reçu n'est pas un JSON valide."
                }))
                continue

            # Extraction des champs
            champs = contenu_dict
            ingredients_texte = "||".join(champs.get("ingredients_de_ma_recette", []))
            instructions_texte = "||".join(champs.get("instructions_de_ma_recette", []))
            mon_image_en_base64 = champs.get("image_base64", "")

            # === Traitement de l'image ===
            dossier_racine = "restaurants"
            os.makedirs(dossier_racine, exist_ok=True)
            dossier_restaurant = os.path.join(
                dossier_racine,
                str(champs.get('identifiant_du_restaurant', '')),
                champs.get('nom_du_restaurant', ''),
                "images_des_recettes"
            )
            os.makedirs(dossier_restaurant, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nom_fichier_image = f"recette_{timestamp}.png"
            chemin_complet = os.path.join(dossier_restaurant, nom_fichier_image)

            # Découpage sécurisé du base64
            try:
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

            # === Enregistrement de la recette en base de données ===
            try:
                temps_int = int(champs.get("temps_de_ma_recette", 0))
            except ValueError:
                await websocket.send_text(json.dumps({
                    "status": "error",
                    "message": "Le champ 'temps' doit être un entier valide."
                }))
                continue

            nouvelle_recette = recette(
                titre=champs.get("nom_de_ma_recette", ""),
                id_du_mood="",
                lien_photo=lien_image,
                categorie=champs.get("type_de_ma_recette", ""),
                temps=temps_int,
                ingredient=ingredients_texte,
                etape=instructions_texte
            )

            db.add(nouvelle_recette)
            await db.commit()

            await websocket.send_text(json.dumps({
                "status": "success",
                "message": "Félicitations ! Votre recette a bien été enregistrée.",
                "action": "redirect",
                "interface": "Gestion_Des_Recettes"
            }))

    except WebSocketDisconnect:
        pass

    finally:
        await db.close()
