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
from .scores import recap_stats_scores

rng = np.random.default_rng()

def graph_eval(dict_by_quantiles, titre, xlabel, ylabel, type, eval, x=None, dep = None):
    """ Trace un graphique simple. 
    Une courbe ou un histogramme."""

    compteur_dist = {nom: 0 for nom in DIST.keys()}
    diff_aic = {nom: [] for nom in DIST.keys()}
    diff_bic = {nom: [] for nom in DIST.keys()}

    for quantile, info in dict_by_quantiles.items():
        
        yB_q = info["yB"]
        if isinstance(yB_q, list):
            yB_q = np.concatenate([np.asarray(v) for v in yB_q if len(v) > 0]) if len(yB_q) > 0 else np.array([])
        else:
            yB_q = np.asarray(yB_q)


        plt.figure()
        if (type==COURBE):
            plt.plot(x, yB_q, color='blue')
            plt.xlim(0, 20)
            
        if (type==HIST):

            plt.hist(yB_q, bins=BINS, density=True, color='orange')

            # Mise en place des approximations théoriques
            
            if (eval == EVAL):
                # Vecteur de résultats pour comparer dist
                resultats = []
                # Évaluation par distribution
                resultats = fit(resultats, yB_q)

                best = min(resultats, key=lambda x: x["bic"])  # o "p-value", "bic"
                compteur_dist[best["nom"]] += 1
                best_aic = best["aic"]
                best_bic = best["bic"]

                diff_best(best_aic, best_bic, diff_aic, diff_bic, resultats)

                abs_axe = np.linspace(min(yB_q), max(yB_q), len(yB_q))
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

    # Recap des statistiques concernant les distributions
    recap_stats_scores(compteur_dist, diff_aic, diff_bic)


def graph_eval_tout_en_1(dict_by_quantiles, titre, xlabel, ylabel, type, eval, x=None, dep=None):
    """Trace tous les quantiles de graph_eval dans une seule fenêtre."""

    n_plots = len(dict_by_quantiles)
    if n_plots == 0:
        print("Aucun quantile à tracer.")
        return

    n_cols = int(np.ceil(np.sqrt(n_plots)))
    n_rows = int(np.ceil(n_plots / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 5, n_rows * 4), squeeze=False)
    axes_flat = axes.flatten()

    compteur_dist = {nom: 0 for nom in DIST.keys()}
    diff_aic = {nom: [] for nom in DIST.keys()}
    diff_bic = {nom: [] for nom in DIST.keys()}
    colors = ['blue', 'red', 'green', 'purple', 'black', 'brown', 'cyan']

    dict_fit = {}
    
    for i, (quantile, info) in enumerate(dict_by_quantiles.items()):
        yB_q = info['yB']
        if isinstance(yB_q, list):
            yB_q = np.concatenate([np.asarray(v) for v in yB_q if len(v) > 0]) if len(yB_q) > 0 else np.array([])
        else:
            yB_q = np.asarray(yB_q)

        ax = axes_flat[i]
        if type == COURBE:
            if x is not None:
                ax.plot(x, yB_q, color='blue')
            else:
                ax.plot(yB_q, color='blue')
            ax.set_xlim(0, 20)

        if type == HIST:
            if yB_q.size > 0:
                ax.hist(yB_q, bins=BINS, density=True, color='orange')
            else:
                ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')

            if eval == EVAL and yB_q.size > 0:
                resultats = []
                resultats = fit(resultats, yB_q)

                if len(resultats) > 0:
                    best = min(resultats, key=lambda x: x['bic'])
                    compteur_dist[best['nom']] += 1
                    best_aic = best['aic']
                    best_bic = best['bic']
                    diff_best(best_aic, best_bic, diff_aic, diff_bic, resultats)

                    abs_axe = np.linspace(min(yB_q), max(yB_q), len(yB_q))
                    for j, res in enumerate(resultats):
                        dist = res['dist']
                        params = res['params']
                        nom = res['nom']
                        try:
                            pdf = dist.pdf(abs_axe, *params)
                            if res == best:
                                label = r"$\bf{" + res['nom'].replace(' ', r'\ ') + \
                                        f"\ (BIC={res['bic']:.2f})" + "}$"
                            else:
                                label = f"{res['nom']} (BIC={res['bic']:.2f})"
                            ax.plot(abs_axe, pdf, color=colors[j % len(colors)], label=label)
                        except Exception as e:
                            print(f"Erreur avec {nom}: {e}")

        if type == SCT:
            ax.scatter(x, yB_q, color='red')
            ax.plot(x, x, color='black')

        yA_range = info.get('yA_range', '')
        ax.set_title(f"q={quantile} {yA_range}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)
        ax.legend()

    for ax in axes_flat[n_plots:]:
        ax.set_visible(False)

    fig.suptitle(titre)
    fig.tight_layout(rect=[0, 0, 1, 0.96])

    fig.savefig('graph_eval_tout_en_1.png', dpi=150, bbox_inches='tight')
    plt.show()

    recap_stats_scores(compteur_dist, diff_aic, diff_bic)

    return dict_fit

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

def graph_dist_tout_en_1(dict_by_quantiles, titre, xlabel, ylabel):
    """Trace tous les histogrammes de graph_dist dans une même fenêtre."""

    n_plots = len(dict_by_quantiles)
    if n_plots == 0:
        print("Aucun quantile à tracer.")
        return

    n_cols = int(np.ceil(np.sqrt(n_plots)))
    n_rows = int(np.ceil(n_plots / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(n_cols * 4, n_rows * 3), squeeze=False)
    axes_flat = axes.flatten()

    for ax in axes_flat[n_plots:]:
        ax.set_visible(False)

    for i, (quantile, info) in enumerate(dict_by_quantiles.items()):
        yB = info.get('yB', [])
        if isinstance(yB, list):
            yB = np.concatenate([np.asarray(v) for v in yB if len(v) > 0]) if len(yB) > 0 else np.array([])
        else:
            yB = np.asarray(yB)

        ax = axes_flat[i]
        if yB.size > 0:
            ax.hist(yB, bins=BINS, weights=np.ones_like(yB)/len(yB), color='orange')
        else:
            ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')

        yA_range = info.get('yA_range', '')
        ax.set_title(f"q={quantile} {yA_range}")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(True)

    fig.suptitle(titre)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
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

