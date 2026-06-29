""" Ce fichier contient les fonctions relatives au graphique 
de la distribution de pics dans toute la france issus des 
données 'summary_all_peaks.csv'. """

import pandas as pd
import matplotlib.pyplot as plt

from librairies.constantes import *
from librairies.graphs.graphs_distributions import graph_eval_all_peaks
from librairies.documents.fichiers import lecture_df

def distribution_peaks(): 
    """Affiche la distribution des pics pour toute la France."""

    # On suppose que df_summary a une colonne 'peak_values' qui contient les valeurs des pics
    df_summary = lecture_df(NOM_SUMMARY)

    peak_values = df_summary[VALOBS]  
    peak_simu = df_summary[VALSIMU]
    
    
    filtre = peak_values > PIC
    peak_values_filtre = peak_values[filtre]

    filtre_tol = (peak_values > PIC) | \
        ((peak_values > PIC - TOL_OBS) \
         & (peak_simu > PIC + TOL_SIMU))
    peak_values_filtre_tol = peak_values[filtre_tol]


    # Affichage de la distribution (par exemple, un histogramme)
    titre = "Distribution des pics gamma pour toute la France"
    titre_filtre = f"Distribution des pics gamma pour toute la France obs > {PIC}"
    titre_filtre_tol = f"Distribution des pics gamma pour toute la France obs > {PIC}\n avec tolérence si simulé"
    xlabel = "Signal Gamma (nSv/h)"
    ylabel = "Fréquence"
    graph_eval_all_peaks(peak_values, titre, xlabel, ylabel, EVAL)
    graph_eval_all_peaks(peak_values_filtre, titre_filtre, xlabel, ylabel, EVAL)
    graph_eval_all_peaks(peak_values_filtre_tol, titre_filtre_tol, xlabel, ylabel, EVAL)


    # plt.figure(figsize=(10, 6))
    # plt.hist(peak_values, bins='auto', density=True, color='orange')
    # plt.title()
    # plt.xlabel("Valeur du pic (nSv/h)")
    # plt.ylabel("Densité")
    # plt.grid()
    # plt.show()

distribution_peaks()
