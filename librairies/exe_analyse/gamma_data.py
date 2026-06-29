"""Ce document contient les fonctions qui gèrent
les données étudiées sur le rayonnement gamma"""

import numpy as np
import pandas as pd

from ..constantes import *
from ..scores import brier
from ..documents.fichiers import lecture_col

def lecture_csv(adresse):
    """Lit les données d'un fichier csv et les met dans un dataframe"""
    data = pd.read_csv(adresse, sep=";")
    return data

def dict_lecture(ad, col):
    """Lit les données de la colonne indiquée
    et les met dans un diccionnaire avec
    son adresse en référence"""

    dict = {}

    for adresse in ad:
        # Ouverture du fichier qu'on veut lire
        data = lecture_csv(adresse)

        # Lecture de la colonne qui nous intérésse
        if col == DATE:
            var = data[col]
            var = pd.to_datetime(var).to_numpy() # Conversion format
        else:
            var = np.array(data[col])    

        # Mise en place de la variable dans le dictionnaire    
        dict[adresse] = var
            
    return dict

def dict_simu_vs_obs(data):
    """Sort un dictionnaire ayant les 
    références des adresses en "keys" et les 
    vecteurs simu et obs de la base de données
    data en éléments. Organisation de toute la
    base de données par station

    Args:
        data (tableau): données de toutes les stations 
        à traîter. 

    Returns:
        dictionnaire: dictionnaire completé 
        avec les infos classifiées par station
    """

    dict = {}

    for bloc in data["adresses"]:

        for ref, adresse in bloc.items():
            if ref == "dep":
                continue

            data = lecture_csv(adresse)
            obs = lecture_col(adresse, VALOBS)
            simu = lecture_col(adresse, VALSIMU)

            # On va comparer les vecteurs, donc il faut qu'ils aient du sens
            if (len(simu) != len(obs)):
                mask = np.isfinite(obs) & np.isfinite(simu)
                obs = obs[mask]
                simu = simu[mask]

            dict[adresse] = [simu, obs]

    return dict

def combiner_dicts(dict1, dict2):
    """Concatène les vecteurs de deux diccionaires
    avec les mêmes références

    Args:
        dict1 (dict): contient les valeurs structurees de simu et obs d'une année
        dict2 (dict): contient les valeurs structurees de simu et obs d'une année

    Returns:
        dict: dictionnaire avec les vecteurs concatenés
    """
    dict_all = {}

    for ref, vals in dict1.items():
        dict_all[ref] = [vals[0], vals[1]]

    for ref, vals in dict2.items():
        if ref in dict_all:
            dict_all[ref][1] = np.concatenate([dict_all[ref][1], vals[1]])
            dict_all[ref][0] = np.concatenate([dict_all[ref][0], vals[0]])
        else:
            dict_all[ref] = [vals[0], vals[1]]

    return dict_all


def pic_gamma(adresse):
    """Compte le nombre de fois
    où y a eu un pic gamma à la station
    pointée par l'adresse"""

    data = lecture_csv(adresse)

    # Lecture des valeurs de gamma
    gamma = np.array(data[VALOBS])

    cont = 0
    for i in range(len(gamma)):
        if gamma[i] >= PIC:
            cont +=1

    return cont

def stations_dep(ad):
    """Conte le nombre de stations 
    par département"""

    cont = 0
    for _ in ad:
        cont += 1
    return cont

def dict_yAyB_by_quantiles(dict_yAyB):
    """Sépare le dictionnaire dict_yAyB par quantiles de yA et 
    regroupe les yB correspondants pour chaque quantile.
    
    Args:
        dict_yAyB (dict): dictionnaire avec structure {'yA': float, 'yB': array}
        n_quantiles (int): nombre de quantiles à créer (défaut: 5)
    
    Returns:
        dict: dictionnaire avec clés 'quantile_0', 'quantile_1', etc. 
              Chaque valeur contient:
                - 'yA_range': tuple (min_yA, max_yA) du quantile
                - 'yB_list': liste de tous les yB du quantile
                - 'yA_list': liste de tous les yA du quantile
                - 'keys': liste des clés originales du quantile
    """
    
    # Extraire tous les yA et garder track des clés
    yA_values = []
    key_mapping = {}
    
    for key, values in dict_yAyB.items():
        yA = values.get('yA')
        if isinstance(yA, (int, float, np.floating, np.integer)) and not np.isnan(yA):
            yA_values.append(yA)
            key_mapping[yA] = key
    
    yA_values = np.array(yA_values)
    
    # Calculer les quantiles de yA
    quantiles = np.linspace(0, 1, N_QUANTILES + 1)
    yA_bins = np.quantile(yA_values, quantiles)
    
    # Créer les groupes par quantile
    quantiles_dict = {}
    
    for i in range(len(yA_bins) - 1):
        quantile_name = f'quantile_{i}'
        yB_list = []
        yA_list = []
        keys_list = []
        
        # Déterminer les limites du quantile (inclure la limite supérieure pour le dernier bin)
        if i < len(yA_bins) - 2:
            mask = (yA_values >= yA_bins[i]) & (yA_values < yA_bins[i+1])
        else:
            mask = (yA_values >= yA_bins[i]) & (yA_values <= yA_bins[i+1])
        
        # Grouper les yB et yA pour ce quantile
        for idx, is_in_quantile in enumerate(mask):
            if is_in_quantile:
                yA_val = yA_values[idx]
                key = key_mapping[yA_val]
                yB = dict_yAyB[key].get('yB')
                
                yA_list.append(yA_val)
                yB_list.append(yB)
                keys_list.append(key)
        
        quantiles_dict[quantile_name] = {
            'yA_range': (f"{yA_bins[i]:.2f}", f"{yA_bins[i+1]:.2f}"),
            'yA': yA_list,
            'yB': yB_list,
            'keys': keys_list,
            'count': len(keys_list)
        }
    
    return quantiles_dict