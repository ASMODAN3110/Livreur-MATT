import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float , Text
from connecteur.Connexion_BD import Base



class factures(Base):

    __tablename__ = "factures"

    id = Column(Integer,primary_key=True,index=True)
    id_de_la_commande = Column(String,index=True)
    date = Column(String,index=True)
    prix_total = Column(Text,index=True)
    