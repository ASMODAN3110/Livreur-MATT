import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class plats(Base):

    __tablename__ = "plats"

    id = Column(Integer,primary_key=True,index=True)
    nom = Column(String,index=True)
    prix = Column(Float,index=True)
    description = Column(String,index=True)
    disponibilite = Column(String,index=True)
    intervalle_d_heure_de_disponibilite = Column(String,index=True)
    intervalle_de_jour_de_disponiblite = Column(String,index=True)
    affichage = Column(String,index=True)
    note = Column(String,index=True)
    like = Column(String,index=True)
    jour_de_creation = Column(String,index=True)
    moment_d_affichage = Column(String,index=True)
    moment_de_desaffichage = Column(String,index=True)
    moment_de_disponibilite = Column(String,index=True)
    moment_d_indisponibilite = Column(String,index=True)
    lien_image = Column(String,index=True)
    id_du_restaurant = Column(Integer,index=True)
    id_des_mood = Column(String,index=True)
