import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base

class ingredients(Base) :

    __tablename__ = "ingredients"

    id = Column(Integer,primary_key=True,index=True)
    nom = Column(String,index=True)
    image = Column(String,index=True)
    categorie = Column(String,index=True)
    lieu = Column(String,index=True)
    caracteristique = Column(String,index=True)
    icone = Column(String,index=True)
    date_d_ajout = Column(String,index=True)
    