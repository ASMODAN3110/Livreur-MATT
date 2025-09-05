import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class allergies(Base) :

    __tablename__ = "allergies"

    id = Column(Integer,primary_key=True,index=True)
    id_de_l_utilisateur = Column(Integer,index=True)
    id_de_l_ingredient = Column(Integer,index=True)
    