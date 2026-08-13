""" Ce fichier contient toutes les fonctions qui
vont organiser les données en dictionnaires yA et yB"""

import numpy as np
from ..constantes import *

from ..documents.docs import docs_dict_to_json_generique

def dict_yA_yB_filtre(dict_maille:dict, dict_vals:dict, ad_filtre:str) -> dict:
    """ À partir du dictionnaire contenant les informations sur les
    zones du maillage contenant 5 stations de mesure ou plus, cette 
    fonction génère un dictionnaire qui regroupe les valeurs yA avec 
    ses yB correspondants, en filtrant seulement les instants où il y a 
    un pic (en obs, ou en simu avec un minimum en obs).

    Args:
        dict_maille (dict): sortie de dict_min5, contient les infos sur 
        les zones du maillage avec 5 stations ou plus (points de la maille, 
        stations, et références des stations de mesure).
        dict_vals (dict): dictionnaire {ref: [simu, obs]} avec les valeurs 
        déjà lues pour chaque station (sortie de structure_donnees).

    Returns:
        dictionnaire: un dictionnaire qui regroupe les valeurs yA avec 
        ses yB correspondants, seulement pour les instants de pic. Chaque 
        clé est une maille contenant 5 stations de mesure ou plus.
    """
    dict_yAyB = {}

    for maille_min5, info_maille in dict_maille.items():

        ref_list = info_maille['ref_stat_mesure']  # Liste de références (ref)
        gamma_obs = []
        gamma_simu = []
        gamma_rain = []
        liste_yB_all = []

        # Itérer sur chaque référence et combiner les données
        for ref in ref_list:
            simu = dict_vals[ref]["simu"]
            obs = dict_vals[ref]["obs"]
            rain = dict_vals[ref]["rain"]

            # Chaque colonne de gamma_obs/gamma_simu correspond à une station, 
            # chaque ligne correspond à un instant de temps
            gamma_obs.append(obs)
            gamma_simu.append(simu)
            gamma_rain.append(rain)

        gamma_obs = np.array(gamma_obs).T
        gamma_simu = np.array(gamma_simu).T
        gamma_rain = np.array(gamma_rain).T

        # Sélection d'informations sur les pics  
        for i in range(len(gamma_obs[:, 0])):
            ligne_obs_i = gamma_obs[i, :]
            ligne_simu_i = gamma_simu[i, :]
            ligne_rain_i = gamma_rain[i, :]

            # Deux conditions:
            # Pic en obs
            masc1 = any(val >= PIC for val in ligne_obs_i) and all(not np.isnan(val) for val in ligne_obs_i)
            # Précipitation non nulle
            masc2 = all((val >= RAIN_MIN) or np.isnan(val) for val in ligne_rain_i)

            # Pic en simu avec un minimum en obs 
            # masc2 = any(val >= PIC + TOL_SIMU for val in ligne_simu_i)
            # Vérification que obs est assez grand
            # if masc2 == True:
            #     for j in range(gamma_obs.shape[1]):
            #         if (gamma_obs[i, j] <= PIC - TOL_OBS) or np.isnan(gamma_obs[i, j]):
            #             masc2 = False

            # On prend en compte si une des conditions est vérifiée
            if (masc1 == True & masc2 == True):
                liste_yB_all.append(ligne_obs_i)

        liste_yB_all = np.array(liste_yB_all)

        # Supposons que toutes les stations ont le même nombre de valeurs
        for n in range(liste_yB_all.shape[0]):
            # Calcul de yA par cas de pic
            yB = liste_yB_all[n, :]
            yA = np.nanmean(yB)

            # On rajoute un autre contrôle de NaN
            if not np.isnan(yA):
                # On garde chaque instant de chaque maille
                dict_yAyB[f'{maille_min5}_{n}'] = {'yA': yA, 'yB': yB}

    docs_dict_to_json_generique(dict_yAyB, ad_filtre)

    return dict_yAyB


def dict_yA_yB_sans_filtre(dict_maille: dict, dict_vals: dict, ad_sans_filtre:str):
    """ À partir du dictionnaire contenant les informations sur les
    zones du maillage contenant 5 stations de mesure ou plus, cette 
    fonction génère un dictionnaire qui regroupe les valeurs yA avec 
    ses yB correspondants, SANS filtrer par condition de pic (on garde 
    tous les instants de temps).

    Args:
        dict_maille (dict): sortie de dict_min5, contient les infos sur 
        les zones du maillage avec 5 stations ou plus (points de la maille, 
        stations, et références des stations de mesure).
        dict_vals (dict): dictionnaire {ref: [simu, obs]} avec les valeurs 
        déjà lues pour chaque station (sortie de structure_donnees).

    Returns:
        dictionnaire: un dictionnaire qui regroupe les valeurs yA avec 
        ses yB correspondants, pour tous les instants de temps (pas seulement 
        les pics). Chaque clé est une maille contenant 5 stations de mesure 
        ou plus, pareil que pour dict_maille.
    """
    dict_yAyB = {}

    for maille_min5, info_maille in dict_maille.items():

        ref_list = info_maille['ref_stat_mesure']  # Liste de références
        gamma_obs = []

        # Itérer sur chaque référence et combiner les données
        for ref in ref_list:
            obs = dict_vals[ref]["obs"]

            # Chaque colonne de gamma_obs correspond à une station, 
            # chaque ligne correspond à un instant de temps
            gamma_obs.append(obs)

        gamma_obs = np.array(gamma_obs).T
        # print("gamma_obs, shape:", gamma_obs, np.array(gamma_obs).shape)

        # On prend tous les instants de temps, sans filtrer par pic
        for n in range(gamma_obs.shape[0]):
            yB = gamma_obs[n, :]
            yA = np.nanmean(yB)

            # On garde le contrôle de NaN pour yA
            if not np.isnan(yA) and not np.any(np.isnan(yB)):
                # On garde chaque instant de chaque maille
                dict_yAyB[f'{maille_min5}_{n}'] = {'yA': yA, 'yB': yB}

    docs_dict_to_json_generique(dict_yAyB, ad_sans_filtre)

    return dict_yAyB

def dict_yAyB_by_quantiles(dict_yAyB: dict, ad_by_quant: str):
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

    docs_dict_to_json_generique(quantiles_dict, ad_by_quant)
    
    return quantiles_dict