##############
# Graphiques #
##############


""" Ce fichier contient les fonctions de génération 
de graphiques pour l'analyse des données de représentativité 
du radon """

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


def graph_vector(values, xlabel='Index', ylabel='Valor', titre='Serie de valores', marker='o', color='blue', figsize=(10, 5)):
    """Dibuja un gráfico de línea simple a partir de un vector de valores.

    Args:
        values (iterable): Vector o lista de valores numéricos.
        xlabel (str): Etiqueta del eje x.
        ylabel (str): Etiqueta del eje y.
        titre (str): Título del gráfico.
        marker (str): Símbolo de marcador para cada punto.
        color (str): Color de la línea.
        figsize (tuple): Tamaño de la figura (ancho, alto).

    Returns:
        None
    """
    valores = np.asarray(values)
    plt.figure(figsize=figsize)
    plt.plot(valores, marker=marker, color=color)
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def graph_maille_france(maille, coords, titre):
    """Dibuja la malla de Francia y las estaciones de medida en un mapa

    Args:
        maille (list): Lista de listas con los puntos de la malla. 
                      Cada punto es un tuple (latitude, longitude).
        coords (numpy.ndarray): Array de coordenadas de las estaciones. 
                               Shape (n_stations, 2) con [lat, lon].
        titre (str): Título del gráfico.
    
    Returns:
        None
    """
    plt.figure(figsize=(12, 10))
    
    # Dibujar la malla
    for i in range(len(maille)):
        for j in range(len(maille[0])):
            lat, lon = maille[i][j]
            plt.plot(lon, lat, 'b.', markersize=3)
            
            # Dibujar líneas de la malla
            if j < len(maille[0]) - 1:
                lat_next, lon_next = maille[i][j + 1]
                plt.plot([lon, lon_next], [lat, lat_next], 'b-', linewidth=0.5, alpha=0.5)
            
            if i < len(maille) - 1:
                lat_next, lon_next = maille[i + 1][j]
                plt.plot([lon, lon_next], [lat, lat_next], 'b-', linewidth=0.5, alpha=0.5)
    
    # Dibujar las estaciones de medida
    lats = coords[:, 0]
    lons = coords[:, 1]
    plt.scatter(lons, lats, color='red', s=50, marker='X', label='Estaciones de medida', zorder=5)
    
    # Configurar el gráfico
    plt.title(titre, fontsize=14)
    plt.xlabel('Longitud', fontsize=12)
    plt.ylabel('Latitud', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


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

