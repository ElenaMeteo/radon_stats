##################################
# Analyse Observations Radon 222 #
##################################

"""Ce fichier contient le main de l'analyse des 
données radon des années 2023/2024. On va gèrer ça
d'une façon différente qu'avec la version 0625 
puisqu'on va traiter les stations individuellement
et pas par département"""

from pathlib import Path


from structure_donnees import structure_donnees
from def_maille import def_maille

from librairies.constantes import *

from librairies.exe_analyse.fitting import fit_et_plot_par_quantile
from librairies.exe_analyse.yA_yB_org import dict_yAyB_by_quantiles, dict_yA_yB_filtre, dict_yA_yB_sans_filtre

from librairies.eval.scores import stats_scores_fittings
from librairies.eval.mu_sigma import regression_params

from librairies.maillage_et_stations.stations_zone import eligibilite_stations

from librairies.documents.org_lecture_calcul import lecture_ou_calcul
from librairies.documents.ad_dependantes import loc_json_structure_bd, loc_graphs_fitting


def main():
    """Execute main script"""

    # Données initales
    ##################

    ad_structure_bd = loc_json_structure_bd() # Localisation des données de structure

    # Adresses des données
    
    adresse = ad_structure_bd / "dict_adresses_all_bd.json"
    dict_adresses = lecture_ou_calcul(adresse, structure_donnees, "dict_adresses_all_bd.json", force=False)
    print("Dictionnaire d'adresses chargé avec succès.")

    # Coordonnées des stations
    adresse = ad_structure_bd / "dict_coords_all_bd.json"
    dict_coords = lecture_ou_calcul(adresse, structure_donnees, "dict_coords_all_bd.json", force=False)
    print("Dictionnaire de coordonnées chargé avec succès.")

    # Valeurs (simu/obs) des stations
    adresse = ad_structure_bd / "dict_vals_all_bd.json"
    dict_vals = lecture_ou_calcul(adresse, structure_donnees, "dict_vals_all_bd.json",  force=False)
    print("Dictionnaire de valeurs chargé avec succès.")

    # Stations éligibles (eau et altitude)
    # adresse = STRUCTURE_BD / "dict_eligible_stations.json"
    # dict_stations_eligibles = lecture_ou_calcul(adresse, eligibilite_stations, "dict_eligible_stations.json", force=False)
    # print("Dictionnaire de stations éligibles chargé avec succès.")

    # Maille
    adresse = MAILLES / f"maille_{DELTA}km.json"
    dict_maille = lecture_ou_calcul(adresse, 
                                    lambda: def_maille(dict_coords), 
                                    f"maille_{DELTA}km.json",
                                    force=True)
    print("Dictionnaire de mailles chargé avec succès.")

    # Traîtement des données
    ########################

    # yA et yB filtrés
    adresse = JSON / "yAyB"
    adresse = adresse / f"dict_yAyB_filtre_delta{DELTA}km_{N_QUANTILES}q.json"
    dict_yAyB_filtre = lecture_ou_calcul(adresse, 
                                  lambda: dict_yA_yB_filtre(dict_maille, dict_vals, adresse), 
                                  "dict_yAyB_filtre.json",
                                  force=True)
    print("Dictionnaire yAyB filtré chargé avec succès.")
    
    # yA et yB non filtrés
    adresse = JSON / "yAyB"
    adresse = adresse / f"dict_yAyB_sans_filtre_delta{DELTA}km_{N_QUANTILES}q.json"
    dict_yAyB_sans_filtre = lecture_ou_calcul(adresse, 
                                  lambda: dict_yA_yB_sans_filtre(dict_maille, dict_vals, adresse), 
                                  "dict_yAyB_sans_filtre.json",
                                  force=True)
    print("Dictionnaire yAyB non filtré chargé avec succès.")

    if (FILTRE_PIC_RADON == True):
        dict_yAyB = dict_yAyB_filtre
    else:
        dict_yAyB = dict_yAyB_sans_filtre

    # Separation par quantiles de yA
    adresse = JSON / "yAyB"
    adresse = adresse / f"dict_yAyB_by_quantiles_delta{DELTA}km_{N_QUANTILES}q_{FILTRE_MARQUE}.json"
    dict_by_quantiles = lecture_ou_calcul(adresse, 
                                          lambda: dict_yAyB_by_quantiles(dict_yAyB, adresse), 
                                          "dict_yAyB_by_quantiles.json",
                                          force=True)
    print("Dictionnaire yAyB par quantiles chargé avec succès.")
    print("Número de quantiles:", len(dict_by_quantiles))
    # Analyse des yA

    # Fitting par quantile
    ######################
    
    # Fitting et plots des distributions
    resultats_all_q, yA_abs = fit_et_plot_par_quantile(dict_by_quantiles)

    # Statistiques des résultats
    _, ad_txt = loc_graphs_fitting()
    stats_scores_fittings(resultats_all_q, Path(ad_txt)/"stats_resultats.txt")

    # Régressions linéaires des paramètres par quantile
    regression_params(resultats_all_q, yA_abs)

if __name__ == "__main__":
    main()
