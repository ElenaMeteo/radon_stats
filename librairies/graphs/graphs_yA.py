##############
# Graphiques #
##############

""" Ce fichier contient les fonctions de génération 
de graphiques pour les données séparées par yB et yA"""

import numpy as np
import matplotlib.pyplot as plt
from ..constantes import *

def graph_yA_yB(dict_yAyB, xlabel, ylabel, titre):
    """Génère un graphique de yB en fonction de yA à partir du dictionnaire 
    qui regroupe les valeurs yA avec ses yB correspondents

    Args:
        dict_yAyB (dictionnaire): un dictionnaire qui regroupe les valeurs yA avec 
        ses yB correspondents. Chaque clé est une maille contenant 5 stations 
        de mesure ou plus, pareil que pour dict_maille.
    Returns:
        None
    """
    yA_all = []
    id = np.linspace(0, XLIM, 100)

    plt.figure()
    plt.xlim(0, XLIM)
    plt.ylim(0, YLIM)
    plt.plot(id, id, color='black', linestyle='--', label='yA = yB')

    for maille, info in dict_yAyB.items():
        yA = info['yA']
        yB = info['yB']
        x = [yA] * len(yB)
        yA_all.extend(x)
        # plt.hexbin(x, yB, gridsize=50, cmap='viridis', label=maille)
        plt.scatter(x, yB, facecolors='none', edgecolors='blue', label=maille)

    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
    # plt.legend()
    plt.grid()
    plt.show()

def graph_hist_equit(dict_yAyB):
    """Génère un histogramme de yB en fonction de yA à partir du dictionnaire 
    qui regroupe les valeurs yA avec ses yB correspondents

    Args:
        dict_yAyB (dictionnaire): un dictionnaire qui regroupe les valeurs yA avec 
        ses yB correspondents. Chaque clé est une maille contenant 5 stations 
        de mesure ou plus, pareil que pour dict_maille.
    Returns:
        None
    """
    yB_all = []
    for _, info in dict_yAyB.items():
        yB = info['yB']
        yB_all.extend(yB)

    yB_all = np.array(yB_all)
    quantiles = np.linspace(0, 1, BINS_ALL_PEAKS + 1)
    bins = np.quantile(yB_all, quantiles)

    plt.hist(yB_all, edgecolor='black', bins=bins)
    plt.xlabel('yB')
    plt.ylabel('Nombre d\'observations')
    plt.show()

    # Liste des éléments de yB_all pour chaque bin
    par_bin = elements_par_bin(yB_all, bins)

    return par_bin, bins

def elements_par_bin(yB_all, bins):
    """Organise les éléments de yB_all en fonction des bins définis par les quantiles
        Args:
        yB_all (numpy array): c'est un tableau numpy qui contient toutes les valeurs de yB extraites du dictionnaire dict_yAyB.
        bins (numpy array): c'est un tableau numpy qui contient les limites des bins définis par les quantiles de yB_all.
        Returns:
            list: Une liste d'arrays, chacun contenant les éléments de yB_all pour un bin spécifique.
    """

    elements_par_bin = []

    for i in range(len(bins)-1):
        if i < len(bins)-2:
            mask = (yB_all >= bins[i]) & (yB_all < bins[i+1])
        else:
            # On inclu l'extreme supérieur dans le dernier bin
            mask = (yB_all >= bins[i]) & (yB_all <= bins[i+1])

        elements_par_bin.append(yB_all[mask])

    return elements_par_bin


def graph_params_yA (dict_fit, xlabel, ylabel, titre):
    """Génère un graphique des paramètres mu et sigma de la distribution gamma 
    en fonction de yA à partir du dictionnaire dict_fit qui contient les 
    paramètres de la distribution gamma pour chaque yA"""

    yA_values = sorted(dict_fit.keys())
    mu_values = [dict_fit[yA]['mu'] for yA in yA_values]
    sigma_values = [dict_fit[yA]['sigma'] for yA in yA_values]

    plt.figure(figsize=(10, 5))
    plt.plot(yA_values, mu_values, marker='o', label='Mu')
    plt.plot(yA_values, sigma_values, marker='o', label='Sigma')
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

