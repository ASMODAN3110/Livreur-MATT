import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base

class factures_evenements(Base) :


    __tablename__ = "factures_evenements"

    id = Column(Integer,primary_key=True,index=True)
    id_de_l_utilisateur = Column(Integer,index=True)
    id_de_l_evenement = Column(Integer,index=True)
    nbre_de_point_a_gagner  = Column(Float,index=True)
    nbre_de_point_depenser = Column(Float,index=True)