""" Ce script permet de créer la maille sur la france """

from librairies.constantes import *
from librairies.documents.docs import docs_dict_to_json_generique
from librairies.maillage_et_stations.maille import maille_exe, dict_min5

def def_maille(dict_coords):

    """ Cette fonction permet de créer la maille sur la france """
    ad_maille = Path(MAILLES / f"maille_{DELTA}km.json")

    # Création de la maille
    maille = maille_exe(dict_coords)

    # Filtrations des mailles contenant assez de stations
    dict_maille = dict_min5(maille, dict_coords)
    docs_dict_to_json_generique(dict_maille, ad_maille)

