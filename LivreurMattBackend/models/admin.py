import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class admin(Base):

    __tablename__ = "admin"


    id = Column(Integer,primary_key=True,index=True)
    nom = Column(String,index=True)
    mot_de_passe = Column(String,index=True)