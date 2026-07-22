##################################
# Analyse Observations Radon 222 #
##################################

"""Ce fichier contient le main de l'analyse des 
données radon des années 2023/2024. On va gèrer ça
d'une façon différente qu'avec la version 0625 
puisqu'on va traiter les stations individuellement
et pas par département"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from collections import defaultdict

from librairies.constantes import *

from librairies.documents.fichiers_erreur import coord_obt
from librairies.documents.fichiers import lecture_json
from librairies.documents.docs import docs_dict_yAyB_to_json, docs_dict_by_quantiles_to_json

from librairies.exe_analyse.fitting import dict_fit_yB
from librairies.exe_analyse.gamma_data import dict_yAyB_by_quantiles

from librairies.maillage_et_stations.maille import maille_exe, dict_min5, dict_yA_yB_filtre, dict_yA_yB_sans_filtre
from librairies.maillage_et_stations.stations_zone import dict_coord_stats

from librairies.graphs.graphs_yA import graph_yA_yB, graph_hist_equit, graph_params_yA
from librairies.graphs.graphs_distributions import exec_graph_dist, graph_eval
from librairies.graphs.graphs_tout_en_1 import graph_dist_tout_en_1, graph_eval_tout_en_1

from librairies.fitting_par_classes.fitting_classe import fitting_simple_et_double
from librairies.fitting_par_classes.graphs_classe import graphs_eval_simple_et_double

# Là on va garder nos résultats .csv
dossier = Path(__file__).parent
dossier_docs = dossier / "docs"
dossier_json = dossier / "json"

def main():
    """Execute main script"""

    # Données par maille
    ####################

    # Lecture document référence pour coordonnées
    data23 = lecture_json(NOM_DATA_23)

    # Coordonnées stations
    dict_coord = dict_coord_stats(data23)
    print("Fin de la création du dictionnaire des coordonnées des stations")
    coords, ad_all = coord_obt(dict_coord)

    # Maille
    maille = maille_exe(coords)
    print("Fin de la création de la maille")

    # Filtrations des mailles contenant assez de stations
    dict_maille = dict_min5(maille, coords, ad_all)
    print("Fin de la filtration des mailles")

    # Traîtement des données
    ########################

    # Analyse des pics dans les mailles filtrées
    dict_yAyB = dict_yA_yB_filtre(dict_maille)
    print("Fin de l'analyse des pics dans les mailles filtrées")

    ad_dict_yAyB = dossier_json / "dict_yAyB.json"
    docs_dict_yAyB_to_json(dict_yAyB, ad_dict_yAyB)
    print(f"Fin de l'écriture de dict_yAyB dans {ad_dict_yAyB}")

    # Separation par quantiles de yA
    dict_by_quantiles = dict_yAyB_by_quantiles(dict_yAyB)
    print(f"\nSeparation par quantiles de yA:")

    ad_dict_yAyB_quant = dossier_json / "dict_yAyB_quantiles.json"
    docs_dict_by_quantiles_to_json(dict_by_quantiles, ad_dict_yAyB_quant)
    print(f"Fin de l'écriture de dict_yAyB dans {ad_dict_yAyB_quant}")

    # Analyse des valeurs yA
    cont_yA = 0
    ref_yA = []
    cont_yA_all = 0
    for ref, values in dict_yAyB.items():
        yA = values.get("yA")
        cont_yA_all += 1
        if isinstance(yA, (int, float, np.floating, np.integer)) and yA < 2:
            cont_yA += 1
            ref_yA.append(ref)
    print(f"Nombre de stations avec yA < 2 : {cont_yA}")
    print(f"Références des stations avec yA < 2 : {ref_yA}")
    print(f"Nombre total de yA : {cont_yA_all}")

    # Graphiques
    ############
    
    # Scatters des yB en fonction de yA
    # graph_yA_yB(dict_yAyB, xlabel="yA", ylabel="yB", titre="yB en fonction de yA")
    print("Fin de la génération du graphique yB en fonction de yA")

    # Histogramme de yB
    #par_bin, bins = graph_hist_equit(dict_by_quantiles)
    print("Fin de la génération de l'histogramme de yB")

    # Graphique de yB en fonction du quantile de yA
    # exec_graph_dist(dict_by_quantiles)
    # graph_dist_tout_en_1(dict_by_quantiles, titre="yB en fonction du quantile de yA", xlabel="Signal gamma observé (yB, nSv/h)", ylabel="Fréquence")
    print("Fin de la génération des graphiques de yB en fonction de yA à partir de l'histogramme")

    # Fitting par quantile
    ######################

    # graph_eval(dict_by_quantiles, titre="yB en fonction du quantile de yA", xlabel="yA", ylabel="yB", type=HIST, eval=EVAL)
    # graph_eval_tout_en_1(dict_by_quantiles, 
    #                      titre="Fitting distribution yB en fonction du quantile de yA", 
    #                      xlabel="Signal gamma observé (yB, nSv/h)", 
    #                      ylabel="Fréquence", 
    #                      type=HIST, 
    #                      eval=EVAL)
    
    # CODE FAIT AVEC DES CLASSES
    for ref, values in dict_by_quantiles.items():

        yB = values['yB']
        yB_flat = np.concatenate(yB).astype(float)
        print(f"\nEssai triple fitting avec {ref}\n\n")

        # Fitting
        resultats_fitting = fitting_simple_et_double(yB=yB_flat, dossier_json=dossier_json)

        # Plot
        graphs_eval_simple_et_double(
            yB=yB_flat, 
            quantile=ref, 
            info_quantile=dict_by_quantiles[ref], 
            resultats_fitting=resultats_fitting
        )
    print("Fin du fitting des yB par yA moyen de chaque bin")
    # plt.show()
    print("Fin de la génération du graphique des paramètres de la distribution gamma en fonction de yA")

    #dict_fit = dict_fit_yB(dict_by_quantiles)
    
    # Graphique des paramètres de la distribution gamma en fonction de yA
    #graph_params_yA(dict_fit, xlabel="yA", ylabel="Paramètres de la distribution gamma", titre="Paramètres de la distribution gamma en fonction de yA")

    

if __name__ == "__main__":
    main()