from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from connecteur.Connexion_BD import AsyncSessionLocal
from models.plats import plats
from sqlalchemy import select

router = APIRouter(prefix="/mise_a_jour_d_un_plat", tags=["mise_a_jour_d_un_plat"])

@router.put("/plats/{id_plat}/toggle_disponibilite")
async def toggle_disponibilite(id_plat: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(plats).where(plats.id == id_plat))
        plat_obj = result.scalars().first()
        if not plat_obj:
            raise HTTPException(status_code=404, detail="Plat non trouvé")

        current = (plat_obj.disponibilite or "").strip().lower()
        nouvelle_dispo = "non" if current == "oui" else "oui"
        plat_obj.disponibilite = nouvelle_dispo

        session.add(plat_obj)
        await session.commit()

    return {"message": f"Disponibilité mise à jour en '{nouvelle_dispo}'"}


@router.put("/plats/{id_plat}/toggle_affichage")
async def toggle_affichage(id_plat: int):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(plats).where(plats.id == id_plat))
        plat_obj = result.scalars().first()
        if not plat_obj:
            raise HTTPException(status_code=404, detail="Plat non trouvé")

        current = (plat_obj.affichage or "").strip().lower()
        nouvelle_affichage = "non" if current == "oui" else "oui"
        plat_obj.affichage = nouvelle_affichage

        session.add(plat_obj)
        await session.commit()

    return {"message": f"Affichage mis à jour en '{nouvelle_affichage}'"}
