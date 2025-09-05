import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class commentaires_plat(Base) :

    __tablename__ =  "commentaires_plat"

    id = Column(Integer,primary_key=True,index=True)
    id_de_l_utilisateur = Column(Integer,index=True)
    id_du_plat = Column(Integer,index=True)
    description = Column(String,index=True)
