##################################
# Analyse Observations Radon 222 #
##################################

"""Ce fichier contient le main de l'analyse des données radon du 06/2025"""

import numpy as np
import pandas as pd

from collections import defaultdict
from pathlib import Path

from librairies.constantes import *
from librairies.graphs.graphs_distributions import graph_carte
from librairies.documents.fichiers import lecture
from librairies.scores import recap_stats_scores
from librairies.documents.docs import doc_scores, docs_distances 
from librairies.fonctions_main import distrib_par_dep, lecture_bloc, scores_par_dep, infos_carte


# Là on va garder nos résultats .csv
dossier = Path(__file__).parent / "docs"

def main():
    """Execute main script."""
    
    # Lecture du document json par département
    data = lecture(NOM_DATA_06_25)
    
    # Vecteurs nécessaires
    titre_dist_dep = "Distribution observations signal gamma par département"
    dict_scores = {}
    lat=[]
    lon=[]
    val=[]
    scores = []

    ad_all = []
    ref_all = []
    dep_all = []

    # Compte le nombre de fois que chaque distribution a été choisie.
    compteur_dist = defaultdict(int)

    # Différence entre les critères des distributions et la valeur du meilleur
    diff_aic = defaultdict(list)
    diff_bic = defaultdict(list)
    
    for bloc in data["adresses"]:
        # Infos du bloc
        dep, ad, dep_all, ad_all, ref_all, temps_all, gamma_all_clean, simu_all_clean, dict_gamma, dict_simu = lecture_bloc(bloc, dep_all, ad_all, ref_all)
        
        # Distributions par département
        distrib_par_dep(dep, temps_all, gamma_all_clean, compteur_dist, diff_aic, diff_bic)
        
        # Évaluation simulations avec des scores par département
        dict_scores = scores_par_dep(dep, gamma_all_clean, simu_all_clean, dict_scores)

        # Infos pour la carte de mesure des pics gamma
        lat, lon, val, scores = infos_carte(ad, dict_gamma, dict_simu, lat, lon, val, scores)

    # Recap des statistiques concernant les distributions
    recap_stats_scores(compteur_dist, diff_aic, diff_bic)

    # Carte
    graph_carte(lat, lon, val, scores)

    # Document des scores
    ad_scores_par_dep = dossier / "scores_par_dep.csv"
    doc_scores(dict_scores, ad_scores_par_dep)

    # Document de distances entre stations
    docs_distances(ad_all, ref_all, dossier)


if __name__ == "__main__":
    main()