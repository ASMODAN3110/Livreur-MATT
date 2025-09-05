import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class livreurs(Base):

    __tablename__ = "livreurs"

    id = Column(Integer,primary_key=True,index=True)
    nom = Column(String,index=True)
    lien_cni = Column(String,index=True)
    sexe = Column(String,index=True)
    lien_photo = Column(String,index=True)
    quartier = Column(String,index=True)
    numero = Column(String,index=True)
    email = Column(String,index=True)
    mot_de_passe = Column(String,index=True)

    
