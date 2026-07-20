##############
# Graphiques #
##############

""" Ce fichier contient les fonctions concernées par
multiples graphiques qui doivent être dessinés dans la 
même fenêtre"""

import numpy as np
import matplotlib.pyplot as plt

from ..constantes import *
from ..exe_analyse.fitting import fit
from ..eval.scores import diff_best, recap_stats_scores

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

def graph_eval_tout_en_1(dict_by_quantiles, titre, xlabel, ylabel, type, eval, x=None, dep=None):
    """Fais les graphiques évalué (ou pas) sur une liste de distributions théoriques
    avec souplesse: courbe, histogramme ou scatter. Les trace tous sur la même fenêtre.
    Args:
        dict_by_quantiles (dict): Contient les données classées par quantile
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        type (string): type de graphique
        eval (string): est-ce qu'on réalise l'évaluation?
    """

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


####################

def graph_eval_double_tout_en_1 (dict_by_quantiles, titre, xlabel, ylabel, type):
    """ Trace les graphiques doublement évalués sur une liste de distributions 
    théoriques de tous les quantiles dans une même fenêtre. 
    Args:
        dict_by_quantiles (dict): Contient les données classées par quantile
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        type (string): type de graphique
    Returns:
        dict_fit (dict): Contient les résultats du fitting pour chaque quantile
    """
