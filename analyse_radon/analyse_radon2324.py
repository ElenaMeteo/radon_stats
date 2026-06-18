##################################
# Analyse Observations Radon 222 #
##################################

"""Ce fichier contient le main de l'analyse des 
données radon des années 2023/2024. On va gèrer ça
d'une façon différente qu'avec la version 0625 
puisqu'on va traiter les stations individuellement
et pas par département"""

import numpy as np
from pathlib import Path

from fonctions.constantes import *

from fonctions.analyse.fichiers import lecture_json
from fonctions.analyse.gamma_data import dict_yAyB_by_quantiles
from fonctions.analyse.maille import maille_exe, dict_min5, dict_yA_yB
from fonctions.analyse.fichiers_erreur import coord_obt
from fonctions.analyse.stations_zone import dict_coord_stats
from fonctions.analyse.docs import docs_dict_yAyB_to_json
from fonctions.analyse.graphs import graph_yA_yB, graph_hist_equit, graph_params_yA
from fonctions.analyse.graphs_analyse import exec_graph_dist
from fonctions.analyse.fitting import dict_fit_yB

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
    dict_yAyB = dict_yA_yB(dict_maille)
    print("Fin de l'analyse des pics dans les mailles filtrées")

    ad_dict_yAyB = dossier_json / "dict_yAyB.json"
    docs_dict_yAyB_to_json(dict_yAyB, ad_dict_yAyB)
    print(f"Fin de l'écriture de dict_yAyB dans {ad_dict_yAyB}")

    # Separation par quantiles de yA
    dict_by_quantiles = dict_yAyB_by_quantiles(dict_yAyB)
    print(f"\nSeparation par quantiles de yA:")

    # for quantile_name, data in dict_by_quantiles.items():
    #     yA_min, yA_max = data['yA_range']
    #     count = data['count']
    #     print(f"  {quantile_name}: yA in [{yA_min:.4f}, {yA_max:.4f}], {count} elements")
    
    # # Sauvegarde des quantiles
    # dict_quantiles_json = {}
    # for quantile_name, data in dict_by_quantiles.items():
    #     yA_min, yA_max = data['yA_range']
    #     dict_quantiles_json[quantile_name] = {
    #         'yA_range': [float(yA_min), float(yA_max)],
    #         'yA_list': [float(yA) for yA in data['yA_list']],
    #         'yB_list': [np.asarray(yB).tolist() for yB in data['yB_list']],
    #         'keys': data['keys'],
    #         'count': data['count']
    #     }
    
    # ad_quantiles = dossier_json / "dict_yAyB_by_quantiles.json"
    # with open(ad_quantiles, "w", encoding="utf-8") as f:
    #     json.dump(dict_quantiles_json, f, ensure_ascii=False, indent=2, sort_keys=True)
    # print(f"Fin de la sauvegarde des quantiles dans {ad_quantiles}")

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

    # Scatters des yB en fonction de yA
    # graph_yA_yB(dict_yAyB, xlabel="yA", ylabel="yB", titre="yB en fonction de yA")
    print("Fin de la génération du graphique yB en fonction de yA")

    # Histogramme de yB
    #par_bin, bins = graph_hist_equit(dict_by_quantiles)
    print("Fin de la génération de l'histogramme de yB")

    # Graphique de yB en fonction du quantile de yA
    exec_graph_dist(dict_by_quantiles)
    print("Fin de la génération des graphiques de yB en fonction de yA à partir de l'histogramme")

    # Fitting par yA moyen de chaque bin
    dict_fit = dict_fit_yB(dict_by_quantiles)
    print("Fin du fitting des yB par yA moyen de chaque bin")
    
    # Graphique des parametres de la distribution gamma en fonction de yA
    graph_params_yA(dict_fit, xlabel="yA", ylabel="Paramètres de la distribution gamma", titre="Paramètres de la distribution gamma en fonction de yA")
    print("Fin de la génération du graphique des paramètres de la distribution gamma en fonction de yA")
    

if __name__ == "__main__":
    main()