import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlalchemy import Column , Integer , String , Float
from connecteur.Connexion_BD import Base


class moods (Base) :

    __tablename__ = "moods"

    id = Column(Integer,primary_key=True,index=True)
    id_du_restaurant = Column(Integer,index=True)
    titre = Column(String,index=True)
    video_url = Column(String,index=True)
    image_url = Column(String,index=True)
    description = Column(String,index=True)
    categorie = Column(String,index=True)
    date_de_creation = Column(String,index=True)
    date_de_publication = Column(String,index=True)
    visibilite = Column(String,index=True)
    note = Column(String,index=True)
    like = Column(String,index=True)
    vue = Column(String,index=True)
