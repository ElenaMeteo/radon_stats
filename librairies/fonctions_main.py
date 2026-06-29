"""Ce fichier contient les fonctions issues 
de la reorganisation du main"""

import numpy as np

from .constantes import *
from .graphs.graphs_distributions import graph_eval
from .scores import brier
from .maillage_et_stations.distance import coord
from .exe_analyse.gamma_data import dict_lecture, pic_gamma
from .documents.fichiers import dict_all

def distrib_par_dep(dep, temps_all, gamma_all_clean, compteur_dist, diff_aic, diff_bic):
    """Affiche la distribution des observations de signal gamma
    par département et met à jour les compteurs de distribution choisies
    et les différences de critères AIC et BIC"""

    # On trace les graphiques de distribution par département
    titre_dist_dep = f"Distribution observations gamma au département {dep}" 
    graph_eval(temps_all, gamma_all_clean, titre_dist_dep, dep, compteur_dist, diff_aic, diff_bic, XLABEL_DIST, YLABEL_DIST, HIST, EVAL)

def scores_par_dep(dep, gamma_all_clean, simu_all_clean, dict_scores):
    """Affiche les scores de chaque simulation par département"""
    
    score_dep, fp, fn = brier(simu_all_clean, gamma_all_clean)
    dict_scores[dep] = [score_dep, fp, fn]
    
    return dict_scores

def dep_ad_ref(bloc):
    """Récupère le département, les adresses et les références d'un bloc du json"""

    dep = bloc['dep']
    ad = [adresse for code, adresse in bloc.items() if code != "dep"] # Ça nous donne une liste d'adresses du departement dep
    ref = [k for k in bloc.keys() if not k.startswith("dep")]

    return dep, ad, ref

def infos_carte(ad, dict_gamma, dict_simu, lat, lon, val, scores ):
    """Récupère les informations nécessaires pour la carte de mesure des pics gamma"""

    for adresse in ad:
        latitude, longitude = coord(adresse)
        valeur = pic_gamma(adresse)

        lat.append(latitude)
        lon.append(longitude)
        val.append(valeur)

        simu_i = np.array(dict_simu[adresse])
        gamma_i = np.array(dict_gamma[adresse])

        mask = np.isfinite(simu_i) & np.isfinite(gamma_i)
        simu_i_clean = simu_i[mask]
        gamma_i_clean = gamma_i[mask]

        if len(simu_i_clean) > 0:
            score_i, _, _ = brier(simu_i_clean, gamma_i_clean)
        else:
            score_i = np.nan 

        scores.append(score_i)

    return lat, lon, val, scores      

def lecture_bloc(bloc, dep_all, ad_all, ref_all):
    """Lit les données d'un bloc du json et les met dans des vecteurs"""

    dep, ad, ref = dep_ad_ref(bloc)
    dict_temps = dict_lecture(ad, DATE)
    dict_gamma = dict_lecture(ad, VALOBS)
    dict_simu = dict_lecture(ad, VALSIMU)

    dep_all.append(dep)
    ad_all.extend(ad)
    ref_all.extend(ref)

    temps_all = dict_all(dict_temps)
    gamma_all = dict_all(dict_gamma)    
    simu_all = dict_all(dict_simu)    

    # On applique le même masque aux deux vecteurs pour assurer même longueur
    mask = np.isfinite(gamma_all) & np.isfinite(simu_all)
    gamma_all_clean = gamma_all[mask]
    simu_all_clean = simu_all[mask]

    return dep, ad, dep_all, ad_all, ref_all, temps_all, gamma_all_clean, simu_all_clean, dict_gamma, dict_simu 