import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base




class recette(Base):

    __tablename__ = "recette"

    id = Column(Integer,primary_key=True,index=True)
    titre = Column(String,index=True)
    id_du_mood = Column(String,index=True)
    lien_photo = Column(String,index=True)
    categorie = Column(String,index=True)
    ingredient = Column(String,index=True)
    etape = Column(String,index=True)
    temps = Column(Integer,index=True)
    