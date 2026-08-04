""" Ce fichier contient les fonctions qui
vont réaliser l'analyse des valeurs de yA """

import numpy as np
from ..constantes import *

def yA_et_seuil (dict_yAyB):
    """ Cette fonction va compter le nombre de stations avec yA < 2 """
    cont_yA_all = 0
    cont_yA_all_by_quantiles = {}

    print(f"Nombre total de yA : {cont_yA_all}")
    print(f"Nombre total de yA par quantile : {cont_yA_all_by_quantiles}")

