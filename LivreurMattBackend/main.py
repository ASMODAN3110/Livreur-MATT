from fastapi import FastAPI
from models import Base
from connecteur.Connexion_BD import engine
from routers import connexion
from routers import recherche_de_tableau_de_commande_a_livrer
from routers import envoi_l_etat_de_la_livraison

import os
# Créer automatiquement le dossier s'il n'existe pas
os.makedirs("images_recettes", exist_ok=True)
from fastapi.staticfiles import StaticFiles

app = FastAPI() 
app.include_router(connexion.router)
app.include_router(recherche_de_tableau_de_commande_a_livrer.router)
app.include_router(envoi_l_etat_de_la_livraison.router)










