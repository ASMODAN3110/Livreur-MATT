import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float , Text
from connecteur.Connexion_BD import Base



class commandes (Base):

    __tablename__ =  "commandes"

    id = Column(String,primary_key=True,index=True)
    id_de_l_utilisateur = Column(Integer,index=True)
    plat = Column(String,index=String)
    date = Column(String,index=True)
    localisation = Column(String,index=True)
    acceptation = Column(String,index=True)
    annulation = Column(String,index=True)
    code_de_livraison = Column(Text,index=True)
    destination = Column(String, index=True)
    code_utilisateur = Column(String, index=True)
