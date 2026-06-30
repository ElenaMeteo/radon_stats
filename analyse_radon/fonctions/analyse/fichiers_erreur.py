##########
# Format #
##########

"""Ce document contient les fonctions qui
gèrent les formats des données qu'on regarde"""

import json
import numpy as np
import pandas as pd
import os

from ..constantes import *

def lecture_csv(adresse):
    """Reads the csv and put it in pandas Dataframe."""
    data = pd.read_csv(adresse, sep=";")
    return data

def lecture_json():
    """Lit les données du document json"""
    print(os.getcwd())
    with open(NOM_DATA_06_25, "r") as file:
        data = json.load(file)
    return data

def coord(adresse):
    """Lit les coordonnées des 
    stations de mesure afin de les
    mettre sur la carte."""

    # Lecture du fichier entier
    data = lecture_csv(adresse)

    # Recherche des colonnes selon nos intérêts
    lat = data[COORD_X].iloc[0]
    lon = data[COORD_Y].iloc[0]
    
    return lat, lon

def coord_obt(dict_coord):
    """Reçoit un dictionnaire avec les adresses en référence et les coordonnées en éléments
    et sort un tableau de coordonnées.
    
    Args:
        dict_coord (dict): dictionnaire qui organise les coordonnées par station en utilisant l'adresse comme référence
    Returns:
        coords (tableau): tableau de coordonnées de toutes les stations"""
    
    coords = []
    ad_all = []
    for adresse, coord in dict_coord.items():
        coords.append(coord)
        ad_all.append(adresse)
    coords = np.array(coords)
    ad_all = np.array(ad_all)
    return coords, ad_all

    # for bloc in dict["adresses"]:
    #     ad = [adresse for code, adresse in bloc.items() if code != "dep"] # Ça nous donne une liste d'adresses du departement dep
    #     coords = np.array([coord(ad) for ad in ad_all])
    # return coords

def lecture_col(adresse, col):
    """Lit les données de la colonne indiquée
    et les met dans un diccionnaire avec
    son adresse en référence"""

    v = []
    # Ouverture du fichier qu'on veut lire
    data = lecture_csv(adresse)

    # Lecture de la colonne qui nous intérésse
    if col == DATE:
        var = data[col]
        var = pd.to_datetime(var).to_numpy() # Conversion format
    else:
        var = np.array(data[col])    

    # Mise en place de la variable dans le vecteur    
    v = var
            
    return v