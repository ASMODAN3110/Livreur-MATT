import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String
from connecteur.Connexion_BD import Base


class restaurants(Base) :

    __tablename__ =  "restaurants" 

    id = Column(Integer,primary_key=True,index=True)
    nom = Column(String, index=True)
    mot_de_passe = Column(String,index=True)
    localisation = Column(String,index=True)
    numero = Column(String,index=True)
    email = Column(String,index=True)
    date_et_heure_de_connexion = Column(String,index=True)
    date_et_heure_fin_connexion = Column(String,index=True)
    jour_d_inscription = Column(String,index=True)
    type_de_cuisine = Column(String,index=True)
    description = Column(String,index=True)
    lien_logo = Column(String,index=True)