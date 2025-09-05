import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class evenements(Base) :

    __tablename__ = "evenements"

    id = Column(Integer,primary_key=True,index=True)
    duree = Column(Integer,index=True)
    date_de_depart = Column(String,index=True)
    date_de_lancement = Column(String,index=True)
    duree_d_inscription = Column(Integer,index=True)
    categorie = Column(String,index=True)
    nbre_de_point_a_gagner = Column(Float,index=True)
    nbre_de_point_pour_s_inscrire = Column(Float,index=True)
    date_de_creation_de_l_evenement = Column(String,index=True)
    

    
   