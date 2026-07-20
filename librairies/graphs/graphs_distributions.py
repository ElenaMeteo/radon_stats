"""Ce document contient les fonctions concernées par les graphiques"""

import numpy as np
import math
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec

from ..constantes import *
from ..exe_analyse.fitting import fit
from ..eval.scores import diff_best, recap_stats_scores

rng = np.random.default_rng()

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


# Fonctions d'évaluation des distributions
##########################################

def graph_eval(dict_by_quantiles, titre, xlabel, ylabel, type, eval, x=None, dep = None):
    """Fais graphique évalué (ou pas) sur une liste de distributions théoriques
     avec souplesse: courbe, histogramme ou scatter

    Args:
        dict_by_quantiles (dict): Contient les données classées par quantile
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        type (string): type de graphique
        eval (string): est-ce qu'on réalise l'évaluation?
    """

    compteur_dist = {nom: 0 for nom in DIST.keys()}
    diff_aic = {nom: [] for nom in DIST.keys()}
    diff_bic = {nom: [] for nom in DIST.keys()}

    for info in dict_by_quantiles.values():
        
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


def graph_eval_all_peaks(y, titre, xlabel, ylabel, eval):
    """Fais graphique évalué (ou pas) sur une liste de distributions théoriques
     avec souplesse: courbe, histogramme ou scatter. Adapté au document
     regroupant les pics de toutes les stations.
    Args:
        y (list or array): Contient les données à analyser
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        eval (string): est-ce qu'on réalise l'évaluation
    Returns:
        resultats (list): Liste des résultats du fitting si eval est EVAL, sinon None
    """
    
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
        resultats = {}
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

    return resultats

