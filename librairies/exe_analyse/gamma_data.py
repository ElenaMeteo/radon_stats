"""Ce document contient les fonctions qui gèrent
les données étudiées sur le rayonnement gamma"""

import numpy as np
import pandas as pd

from ..constantes import *
from ..eval.scores import brier
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

def dict_simu_vs_obs(data_base):
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

    for bloc in data_base["adresses"]:

        for ref, adresse in bloc.items():
            if ref == "dep":
                continue

            # data = lecture_csv(adresse)
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

def combiner_n_dicts(*dicts):
    """Concatène les vecteurs de N dictionnaires 
    avec les mêmes références

    Args:
        *dicts (dict): nombre variable de dictionnaires, chacun contenant 
        les valeurs structurées de simu et obs d'une année

    Returns:
        dict: dictionnaire avec les vecteurs concaténés
    """
    dict_all = {}

    for d in dicts:
        for ref, vals in d.items():
            if ref in dict_all:
                dict_all[ref] = {
                    cle: np.concatenate([dict_all[ref][cle], vals[cle]])
                    for cle in vals
                }
            else:
                dict_all[ref] = {cle: v.copy() for cle, v in vals.items()}

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

