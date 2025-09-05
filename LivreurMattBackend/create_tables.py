
import asyncio
from connecteur.Connexion_BD import engine
from models import Base # Grace a ton __init__.py

async def create_all_tables():
    async with engine.begin() as conn :
        await conn.run_sync(Base.metadata.create_all)

    print("toutes les tables ont été crééés.")


if __name__ == "__main__" :
    asyncio.run(create_all_tables())