
import asyncpg

async def connexion_a_ma_bd():

    conn = await asyncpg.connect(
        user='postgres',
        password='-iNVENTEURC1',
        database='MATT_RESEAU_SOCIAL',
        host='10.86.107.191',
        port=5432
    )

    return conn 

addresse_ip = '10.86.107.191'
port_frontend  = '8000'
    