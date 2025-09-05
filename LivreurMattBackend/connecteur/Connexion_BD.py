from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

password = quote_plus("-iNVENTEURC1")
DATABASE_URL = f"postgresql+asyncpg://postgres:{password}@10.86.107.191:5432/MATT_RESEAU_SOCIAL"
# 10.92.214.191 telephone orange
# 192.168.114.191 telephone mtn
# 192.168.1.108 wifi
#  192.168.37.108 wifi alain
Base = declarative_base() 

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    connect_args={"command_timeout": 30}
)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
