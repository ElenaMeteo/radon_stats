"""Fonctions pour la création de documents .csv """

import json
import numpy as np
import pandas as pd
from ..constantes import *
from .distance import coord, distance_2points

def doc_scores(dict_scores, ad_scores_par_dep):
    """Crée un document .csv avec les scores par département"""

    df_scores = pd.DataFrame.from_dict(dict_scores, orient='index', columns=['score', 'fp', 'fn'])
    df_scores.reset_index(inplace=True)
    df_scores.rename(columns={'index': 'dep'}, inplace=True)
    df_scores.to_csv(ad_scores_par_dep, index=False)
    
def docs_distances(ad_all, ref_all, dossier):
    """Crée un document .csv avec la matrice de distances entre stations"""

    coords = np.array([coord(ad) for ad in ad_all])
    lats = coords[:, 0]
    lons = coords[:, 1]
    n = len(coords)
    moins_tol = []

    df_distances = pd.DataFrame(np.nan, index=ref_all, columns=ref_all)

    for i in range(n):
        lat1, lon1 = lats[i], lons[i]

        for j in range (i+1, n):
            lat2 = lats[j]
            lon2 = lons[j]

            d = distance_2points(lat1, lon1, lat2, lon2)
            if (d <= TOL_DIST):
                moins_tol.append((ref_all[i], ref_all[j], d))
            
            df_distances.iloc[i, j] = d

    ad_matrice_de_distance = dossier / "matrice_de_distances.csv"
    ad_moins_de_tol = dossier / "moins_de_tol.csv"

    df_moins_tol = pd.DataFrame(moins_tol, columns=["station_1", "station_2", "distance"])

    df_distances.to_csv(ad_matrice_de_distance)
    df_moins_tol.to_csv(ad_moins_de_tol, index=False)

# def docs_dict_to_json(dict_, ad):
#     """Crée un document .json à partir d'un dictionnaire"""

#     df = pd.DataFrame.from_dict(dict_, orient='index')
#     df.reset_index(inplace=True)
#     df.rename(columns={'index': 'ref'}, inplace=True)
#     df.to_json(ad, orient='records', indent=4)


def docs_dict_to_json(dict_all, path):
    """Crée un document .json à partir de dict_all (avec arrays NumPy)."""

    dict_json = {}
    for ref in sorted(dict_all):
        vals = dict_all[ref]
        dict_json[ref] = [
            np.asarray(vals[0]).tolist(),
            np.asarray(vals[1]).tolist()
        ]

    with open(path, mode="w", encoding="utf-8") as write_file:
        json.dump(dict_json, write_file, ensure_ascii=False, indent=2, sort_keys=True)


def docs_dict_yAyB_to_json(dict_yAyB, path):
    """Crée un document .json à partir du dictionnaire dict_yA_yB."""

    dict_json = {}
    for ref, values in dict_yAyB.items():
        dict_json[ref] = {
            "yA": None if np.isnan(values["yA"]) else float(values["yA"]),
            "yB": np.asarray(values["yB"]).tolist()
        }

    with open(path, mode="w", encoding="utf-8") as write_file:
        json.dump(dict_json, write_file, ensure_ascii=False, indent=2)
