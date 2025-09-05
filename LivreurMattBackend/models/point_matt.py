import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class point_matt(Base):

    __tablename__ = "point_matt"

    id = Column(Integer,primary_key=True,index=True)
    id_de_l_utilisateur = Column(Integer,index=True)
    nbre_de_point_actuel = Column(Float,index=True)