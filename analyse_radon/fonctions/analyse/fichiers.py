############
# Fichiers #
############

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

def lecture_json(data):
    """Lit les données du document json"""
    print(os.getcwd())
    with open(data, "r") as file:
        data = json.load(file)
    return data

def lecture_df(data):
    """Lit le fichier summary_all_peaks.csv et retourne un DataFrame."""

    df_summary = pd.read_csv(data)
    return df_summary

def liste_dep(data):
    """Sort la liste de départements
    dans notre dictionnaire"""
    dep = []
    for bloc in data["adresses"]:
        dep.append(bloc["dep"]) 
    print(dep)   

def lecture_col(adresse, col):
    """Lit les données de la colonne indiquée dans un fichier CSV."""

    data = lecture_csv(adresse)

    # Lecture de la colonne qui nous intéresse
    if col == DATE:
        v = data[col]
        v = pd.to_datetime(v).to_numpy() # Conversion format
    else:
        v = np.array(data[col])
    return v


def dict_all(dict):
    """Prend un dictionnaire et retourne un vecteur de toutes les valeurs du dictionnaire"""
    return np.array(list(dict.values())).T.flatten()

# def lecture_json_filtre (ad_json, ref_valides):
#     """Lit les données du document json et filtre les blocs en 
#     gardant seulement les références valides
    
#     Args:
#         ad_json (str): chemin du document json à lire
#         ref_valides (list): liste des références valides à garder

#     Returns:
#             dict: dictionnaire filtré
#     """
#     with open(ad_json, "r") as file:
#         data = json.load(file)
    
#     # Filtrar los bloques manteniendo solo las referencias válidas
#     for bloc in data["adresses"]:
#         keys_a_eliminar = [ref for ref in bloc.keys() 
#                           if ref != "dep" and ref not in ref_valides]
#         for key in keys_a_eliminar:
#             del bloc[key]
#     return data