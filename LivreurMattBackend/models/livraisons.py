import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class livraisons(Base):

    __tablename__ = "livraisons"

    id = Column(Integer,primary_key=True,index=True)
    id_du_livreur = Column(Integer,index=True)
    date_de_livraison = Column(String,index=True)
    date_de_recuperation_de_la_commande_au_restau = Column(String,index=True)
    id_de_la_redistribution = Column(String,index=True)
    prix = Column(Integer,index=True)
   
