##############
# Graphiques #
##############

"""Ce document contient les cfonctions concernées par les graphiques"""

import numpy as np
import math
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec

from ..constantes import *
from .fitting import fit, diff_best

rng = np.random.default_rng()

def graph_eval(y, titre, dep, compteur_dist, diff_aic, diff_bic, xlabel, ylabel, type, eval, x=None):
    """ Trace un graphique simple. 
    Une courbe ou un histogramme."""
    
    plt.figure()
    if (type==COURBE):
        plt.plot(x, y, color='blue')
        plt.xlim(0, 20)
        
    if (type==HIST):
        print("\n\ndep:", dep)
        print("moyenne y:", np.mean(y))
        print(f"ect y:{np.std(y)}")

        q = np.percentile(y, 99)
        y_bis = y[y <= q] # Les grandes valeurs altèrent les resultats.
        n, bins, _ = plt.hist(y_bis, bins=BINS, density=True, color='orange')
    
        plt.xlim(0, 20)

        # Mise en place des approximations théoriques
        
        if (eval == EVAL):
            # Vecteur de résultats pour comparer dist
            resultats = []
            # Évaluation par distribution
            resultats = fit(resultats, y_bis, dep)

            best = min(resultats, key=lambda x: x["bic"])  # o "p-value", "bic"
            compteur_dist[best["nom"]] += 1
            best_aic = best["aic"]
            best_bic = best["bic"]

            diff_best(best_aic, best_bic, diff_aic, diff_bic, resultats)

            abs_axe = np.linspace(min(y_bis), max(y_bis), len(y_bis))
            colors = ['blue', 'red', 'green', 'purple', 'black', 'brown', 'cyan']

            for i, res in enumerate(resultats):
                dist = res["dist"]
                params = res["params"]
                nom = res["nom"]
                
                try:
                    pdf = dist.pdf(abs_axe, *params)
                    if res == best:
                        label = r"$\bf{" + res["nom"].replace(" ", r"\ ") + \
                                f"\ (BIC={res['bic']:.2f})" + "}$"
                    else:
                        label = f"{res['nom']} (BIC={res['bic']:.2f})"
                    plt.plot(abs_axe, pdf, color=colors[i % len(colors)], label=label)

                except Exception as e:
                    print(f"Erreur avec {nom}: {e}")

            plt.title(f"Données et son approximation")

        else:
            plt.title(titre)
    
    if (type == SCT):
        plt.scatter(x, y, color='red')
        plt.plot(x, x, color='black')
    
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()

def graph_multi(x, y, titre, titres, xlabel, ylabel, n, type):
    """
    Genere une fênetre de graphiques dynamique en fonction 
    des stations de mesure qu'on regarde. Pair ou impair, 
    toujours centré et à la même échelle.
    """
    # n = nombre d'axes
    lig = np.where(n<3, 1, 2).item() # nombre de lignes
    if (lig==1):
        col = n
    else:
        col = math.floor((n+1)/2) # nombre de colonnes
        # a = 5*nCol, b = 2*nFilas
    fig = plt.figure(figsize=(5*col, 5*lig))
    gs = GridSpec(lig, 2*col)
    
    axs = []
    for l in range(lig):
        for c in range(col):
            if ((c+1)*(l+1) <= n):
                if (l==1 & n%2==1):
                    ax = fig.add_subplot(gs[l, 2*c+1:2*(c+1)+1])
                else: 
                    ax = fig.add_subplot(gs[l, 2*c:2*(c+1)])
                axs.append(ax)
                            
    for i, ax in enumerate(axs):
        if (type==COURBE):
            #ax.set_xlim(DEBUT, FIN)
            ax.set_ylim(0, YMAX_C)
            ax.plot(x[:,i], y[:,i])
            ax.tick_params(axis='x', rotation=80)
        if (type==HIST):
            ax.set_xlim(0, XMAX_H)
            ax.set_ylim(0, YMAX_H)
            ax.hist(y[:,i], bins=BINS)
        ax.set_title(titres[i])
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
    fig.suptitle(titre)
    plt.tight_layout()
    plt.show()
    
def graph_carte(lat, lon, val, scores):
    """Donne une carte de la France avec
    les stations de mesure et montre la quantité
    de pics/evenements de chaque endroit"""
    
    # Format des données en DataFrame et GeoDataFrame
    data = pd.DataFrame({
        'lat':lat,
        'lon':lon,
        'val':val,
        'scores':scores
        })
    
    gdf = gpd.GeoDataFrame(
        data, 
        geometry=gpd.points_from_xy(data.lon, data.lat),
        crs = "EPSG:4326" # Code du format GPS lon lat
    )
    
    # Carte de France
    world = gpd.read_file(NOM_CARTE)
    france = world[world["NAME"] == "France"]
    
    # Plot
    fig, ax = plt.subplots(figsize=(8,8))
    france.plot(ax=ax, color="lightgrey")
    
    gdf.plot(
        ax=ax,
        # color="red",
        column='scores',
        cmap='rainbow',
        markersize=40,
        # markersize=gdf['val'],
        legend=True
    )
    
    # Limites continentales de la France
    xmin, xmax = -5.0, 10.0
    ymin, ymax = 41.0, 52.0
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    plt.show()

def graph_eval_all_peaks(y, titre, xlabel, ylabel, eval):
    """ Trace un graphique simple. 
    Une courbe ou un histogramme."""
    
    plt.figure()
    
    y = np.asarray(y)
    y = y[~np.isnan(y)]

    if y.size == 0:
        print("graph_eval_all_peaks: pas de données valides après suppression des NaN.")
        return

    print("summary all peaks")
    print("moyenne y:", np.mean(y))
    print(f"ect y:{np.std(y)}")

    q = np.percentile(y, 99)
    if np.isnan(q):
        print("graph_eval_all_peaks: percentile invalide, vérifiez les données.")
        return

    y_bis = y[y <= q] # Les grandes valeurs altèrent les resultats.
    if y_bis.size == 0:
        print("graph_eval_all_peaks: pas de données après filtrage par percentile.")
        return

    n, bins, _ = plt.hist(y_bis, bins=BINS, density=True, color='orange')
    
    # plt.xlim(0, 60)

    # Mise en place des approximations théoriques
        
    if (eval == EVAL):
        # Vecteur de résultats pour comparer dist
        resultats = []
        # Évaluation par distribution
        resultats = fit(resultats, y_bis)

        if len(resultats) == 0:
            print("graph_eval_all_peaks: aucune distribution valide après le fitting.")
            plt.title(titre)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid()
            plt.show()
            return

        best = min(resultats, key=lambda x: x["bic"])  # o "p-value", "bic"


        abs_axe = np.linspace(min(y_bis), max(y_bis), len(y_bis))
        colors = ['blue', 'red', 'green', 'purple', 'black', 'brown', 'cyan']

        for i, res in enumerate(resultats):
            dist = res["dist"]
            params = res["params"]
            nom = res["nom"]
                
            try:
                pdf = dist.pdf(abs_axe, *params)
                if res == best:
                    label = r"$\bf{" + res["nom"].replace(" ", r"\ ") + \
                            f"\ (BIC={res['bic']:.2f})" + "}$"
                else:
                    label = f"{res['nom']} (BIC={res['bic']:.2f})"
                plt.plot(abs_axe, pdf, color=colors[i % len(colors)], label=label)

            except Exception as e:
                print(f"Erreur avec {nom}: {e}")

        plt.title(f"Données et son approximation")

    else:
        plt.title(titre)
    
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid()
    plt.show()

def graph_dist(y, titre, xlabel, ylabel):
    """ Trace un histogramme simple qui sert 
    de visualisation d'une distribution. """

    plt.figure()
    plt.hist(y, bins=BINS, weights=np.ones_like(y)/len(y), color='orange')
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    plt.show()

def exec_graph_dist(dict_by_quantiles):
    """Execute graph_dist pour toutes les classes de yA concernées.
    Graphique de yB en fonction de yA à partir de l'histogramme
     Args:
        dict_by_quantiles (dict): Dictionnaire des éléments de yB pour chaque quantile
     Returns:
        None
     """
    for quantile, info in dict_by_quantiles.items():
        yB = info['yB']
        # Si yB est une liste de tableaux/itérables, convertir en un array 1D
        if isinstance(yB, list):
            yB = np.concatenate([np.asarray(v) for v in yB if len(v) > 0]) if len(yB) > 0 else np.array([])
        else:
            yB = np.asarray(yB)

        yA_range = info['yA_range']
        q = quantile
        graph_dist(yB, titre=f"yB pour yA_range={yA_range} ({q})", xlabel="yB", ylabel="Densité")


    # for i in range(len(par_bin)):
    #     yB_q = par_bin[i]
    #     yA_q = (bins[i] + bins[i+1]) / 2  # On prend le milieu du bin comme yA_q
