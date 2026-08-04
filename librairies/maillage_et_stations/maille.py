##########
# Maille #
##########

""" Ce fichier contient les fonctions qui gèrent les mailles d'une zone donnée"""

import math
import pandas as pd
import numpy as np
from .stations_zone import cont_stat
from ..documents.fichiers_erreur import lecture_col, coord_obt
from ..constantes import *

def maille_exe(dict_coords:dict) -> np.ndarray:
    """ Execute maille france avec
    tous les paramètres nécessaires

    Args:
        dict_coords (dict): dictionnaire {ref: [lat, lon]} avec les 
        coordonnées de chaque station

    Returns:
        maille: résultat de maille_france, la grille avec les stations 
        regroupées par carré (> MIN_STATIONS)
    """
    lats = [coord[0] for coord in dict_coords.values()]
    lons = [coord[1] for coord in dict_coords.values()]

    # Limites pour définir la maille
    lat_lim = (min(lats), max(lats))
    lon_lim = (min(lons), max(lons))

    # Maille et dictionnaire des stations dans chaque carré avec > MIN_STATIONS
    maille = maille_france(lat_lim, lon_lim)

    return maille

def maille_france(lat:np.ndarray, lon:np.ndarray) -> np.ndarray:
    """
    Crée une maille couvrant la France métropolitaine avec une distance DELTA donnée entre les lignes.
    Écrit une liste des points de la maille dans un fichier CSV.
    
    Args:
        delta_km (float): Distance en kilomètres entre les lignes de la maille.
        lat (tuple): Tuple (lat_min, lat_max) représentant les limites de latitude de la maille.
        lon (tuple): Tuple (lon_min, lon_max) représentant les limites de longitude de la maille.
    
    Returns:
        list: Liste de listes, où chaque sous-liste représente une rangée de la maille,
              et chaque élément est un tuple (latitude, longitude) des sommets.
    """
    # Limites approximatives de la France métropolitaine en degrés
    # lat_min, lat_max = 41.0, 51.5
    # lon_min, lon_max = -5.0, 10.0
    lat_min, lat_max = lat
    lon_min, lon_max = lon
    
    # Adaptation du delta en km en degrés de latitude et de longitude
    km_par_degre_lat = 111.0  # Environ 111 km par degré de latitude
    lat_moyenne = (lat_min + lat_max) / 2
    km_par_degre_lon = 111.0 * math.cos(math.radians(lat_moyenne))  # Ajusté pour la longitude
    
    # Calcul du pas en degrés
    pas_lat = DELTA / km_par_degre_lat
    pas_lon = DELTA / km_par_degre_lon
    
    # Création de la maille
    maille = []
    lat = lat_min
    while lat <= lat_max + pas_lat / 2:  # Pour couvrir entièrement
        rangee = []
        lon = lon_min
        while lon <= lon_max + pas_lon / 2:  # Pour couvrir entièrement
            rangee.append((round(lat, 6), round(lon, 6)))  # Arrondi pour précision
            lon += pas_lon
        maille.append(rangee)
        lat += pas_lat

    df_scores = pd.DataFrame(maille)
    df_scores.reset_index(inplace=True)
    df_scores.rename(columns={'index': 'rangee'}, inplace=True)
    df_scores.to_csv("coord_maille", index=False)

    return maille

def dict_min5(maille:np.ndarray, dict_coords:dict):
    """ Parcourt la maille carré par carré et compte le nombre de stations
    dans chacun. Si le nombre de stations est supérieur ou égal à MIN_STAT,
    on ajoute la maille à un double dictionnaire.

    Args:
        maille (list): sortie de maille_france, liste de listes de tuples 
        (latitude, longitude) des sommets.
        dict_coords (dict): dictionnaire {ref: [lat, lon]} des coordonnées 
        des stations de mesure.

    Returns:
        dict_maille (dictionnaire): dictionnaire avec les infos sur les 
        zones du maillage contenant 5 stations de mesure ou plus.
    """
    n = len(maille)
    m = len(maille[0])
    cont_mailles = 0
    dict_maille = {}

    for i in range(1, n):
        for j in range(1, m):
            p1 = maille[i-1][j-1]
            p2 = maille[i-1][j]
            p3 = maille[i][j]
            p4 = maille[i][j-1]

            cont, stat_dans_zone, ref_stat_zone = cont_stat(p1, p2, p3, p4, dict_coords)

            if cont >= MIN_STAT:
                cont_mailles += 1
                dict_maille[f'maille_{i}_{j}'] = {
                    'points_maille': [p1, p2, p3, p4],
                    'stat_mesure': stat_dans_zone,
                    'ref_stat_mesure': ref_stat_zone  # ahora son referencias (ref), no adresses
                }

    print(f"Nombre de mailles avec au moins {MIN_STAT} stations: {cont_mailles}")
    return dict_maille


def MSE(yA, yB):
    """Calcule l'erreur quadratique moyenne entre yA et yB
    Args:
        yA (float): c'est la valeur de yA, c'est la moyenne des valeurs de yB.
        yB (numpy array): c'est un tableau numpy qui contient les valeurs de yB, 
        c'est les valeurs de chaque station à un instant donné.
    Returns:
        float: l'erreur quadratique moyenne entre yA et yB."""

    aux = 0
    for i in range(len(yB)):
        if not np.isnan(yB[i]):
            aux += (yA - yB[i]) ** 2
    mse = aux / len(yB)

    print(f"MSE entre yA={yA:.4f} et yB={yB}: {mse:.4f}")
        
    return mse

def MSE_all(mse):
    """Calcule l'erreur quadratique moyenne totale entre yA et yB pour toutes les mailles et tous les instants
    Args:
        mse (list): c'est une liste qui contient les erreurs quadratiques moyennes entre yA et yB pour toutes les mailles et tous les instants.
    Returns:
        float: l'erreur quadratique moyenne totale entre yA et yB pour toutes les mailles et tous les instants."""
    mse_total = np.mean(mse)
    return mse_total

