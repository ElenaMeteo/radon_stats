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

def maille_exe(coords):
    """Execute maille france avec
    tous les paramètres nécessaires
    """

    lats = coords[:, 0]
    lons = coords[:, 1]

    # Limites pur définir la maille
    lat_lim = (min(lats), max(lats))
    lon_lim = (min(lons), max(lons))

    # Maille et dictionnaire des stations dans chaque carré avec > MIN_STATIONS
    maille = maille_france(lat_lim, lon_lim)

    return maille

def maille_france(lat, lon):
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


def dict_min5 (maille, coords, ad_all):
    """Parcourt la maille carré par carré et compte le nombre de stations
    dans chacun. Si le nombre de stations est supérieur ou égal à MIN_STAT,
    on ajoute la maille à un double diccionnaire.
    Args:
        maille (list): c'est la sortie de la fonction maille_france, c'est une liste de listes, 
        où chaque sous-liste représente une rangée de la maille, et chaque élément est un tuple 
        (latitude, longitude) des sommets.
        coords (numpy array): c'est un tableau numpy qui contient les coordonnées des stations de mesure.
        ad_all (numpy array): c'est un tableau numpy qui contient les adresses des stations de mesure.
    Returns:
        dict_maille (dictionnaire): c'est un dictionnaire qui contient les informations sur
        les zones du maillage contenant 5 stations de mesure ou plus: les points de la maille,
        les stations de mesure dans la maille et les adresses des stations de mesure."""

    # Dimensions de la maille
    n = len(maille)
    m = len(maille[0])

    cont_mailles = 0

    dict_maille = {}
    """ On parcourt la maille carré par carré et on compte le nombre de stations
    dans chacun. Si le nombre de stations est supérieur ou égal à MIN_STAT, 
    on ajoute la maille à un double diccionnaire """

    for i in range(1, n):
        for j in range(1, m):
            # 4 points de la maille qu'on regarde
            p1 = maille[i-1][j-1]
            p2 = maille[i-1][j]
            p3 = maille[i][j]
            p4 = maille[i][j-1]
            # On compte et on obtient la liste des stations dans la maille
            cont, stat_dans_zone, ad_stat_zone = cont_stat(p1, p2, p3, p4, coords, ad_all)
            # On agit si y a assez de stations
            if cont >= MIN_STAT:
                cont_mailles += 1
                # On ajoute un élement au diccionnaire en forme de diccionnaire
                dict_maille[f'maille_{i}_{j}'] = {
                    'points_maille': [p1, p2, p3, p4],
                    'stat_mesure': stat_dans_zone,
                    'ad_stat_mesure': ad_stat_zone
                }
    print(f"Nombre de mailles avec au moins {MIN_STAT} stations: {cont_mailles}")

    return dict_maille


def dict_yA_yB(dict_maille):
    """À partir du dictionnaire contenant les infromations sur les
    zones du maillage contenant 5 stations de mesure ou plus, cette 
    fonction génère un dictionnaire qui regroupe les valeurs yA avec 
    ses yB correspondents

    Args:
        dict_maille (dictionnaire): c'est la sortie de la fonction dict_min5, 
        c'est un dictionnaire qui contient les informations sur les zones du 
        maillage contenant 5 stations de mesure ou plus: les points de la maille, 
        les stations de mesure dans la maille et les adresses des stations de mesure.

    Returns:
        dictionnaire: un dictionnaire qui regroupe les valeurs yA avec 
        ses yB correspondents. Chaque clé est une maille contenant 5 stations 
        de mesure ou plus, pareil que pour dict_maille.
    """
    dict_yAyB = {}

    for maille_min5, info_maille in dict_maille.items():

        ad_list = info_maille['ad_stat_mesure']  # Liste de directions
        gamma_obs = []
        gamma_simu = []
        liste_yB_all = []
        
        # Itérer sur chaque adresse et combiner les données
        for ad in ad_list:
            # On ajoute les valeurs de chaque station à la liste gamma_obs et gamma_simu
            # Chaque colonne de gamma_obs correspond à une station, chaque ligne correspond à un instant de temps
            gamma_obs.append(lecture_col(ad, VALOBS)) 
            gamma_simu.append(lecture_col(ad, VALSIMU))
        
        gamma_obs = np.array(gamma_obs).T
        gamma_simu = np.array(gamma_simu).T
        # print("gamma_obs, shape:", gamma_obs, np.array(gamma_obs).shape)
        # print("gamma_simu, shape:", gamma_simu, np.array(gamma_simu).shape)

        # Sélection d'informations sur les pics  
        for i in range(len(gamma_obs[:, 0])):
            ligne_obs_i = gamma_obs[i, :]
            ligne_simu_i = gamma_simu[i, :]

            # Deux conditions:
                # Pic en obs
                # Pic en simu avec un minimum en obs 
            masc1 = any(val>= PIC for val in ligne_obs_i ) and all(not np.isnan(val) for val in ligne_obs_i)
            masc2 = any(val >= PIC + TOL_SIMU for val in ligne_simu_i)

            # Vérification que obs est assez grand
            if masc2 == True:
                for j in range(gamma_obs.shape[1]):
                    if (gamma_obs[i, j] <= PIC - TOL_OBS) or np.isnan(gamma_obs[i, j]):
                        masc2 = False
            
            # On prend en compte si une des conditions est vérifiée
            if (masc1 == True) or (masc2 == True):
                liste_yB_all.append(ligne_obs_i)
        
        liste_yB_all = np.array(liste_yB_all)
        # print("liste_yB_all, shape:", liste_yB_all, liste_yB_all.shape)

        # Supposons que toutes les stations ont le même nombre de valeurs
        
        for n in range(liste_yB_all.shape[0]):
            # Calcul de yA par cas de pic
            yB = liste_yB_all[n, :]
            yA = np.nanmean(yB)

            # On rajoute un autre contrôle de NaN
            if not np.isnan(yA):
                # Crear una clave única para cada instante en cada maille
                dict_yAyB[f'{maille_min5}_{n}'] = {'yA': yA, 'yB': yB}

    return dict_yAyB


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

