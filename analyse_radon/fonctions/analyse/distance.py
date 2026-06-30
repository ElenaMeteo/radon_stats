""" Ce fichier contient les fonctions
relatifs à la position et distance entre 
les stations."""

import math
from .gamma_data import lecture_csv
from ..constantes import *

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

def distance_2points(lat1, lon1, lat2, lon2):
    """Cette fonction calcule la ditance entre 
    deux points de la terre en utilisant la 
    formule de Haversine."""

    # On converti à radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Différences des coordonnées
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Formule d'Haversine
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance finale
    d = R * c

    return d