""" Ce fichier contient la classe et les 
fonctions qui vons nous permettre de faire
les plots de nos distributions théoriques et
de nos données expérimentales."""

import numpy as np
import matplotlib.pyplot as plt

from ..constantes import *
from securite import check_vecteur_vide, check_vecteur_nan
from librairies.eval.scores import stats_scores_fittings

class Graphs: 

    """ Classe pour la création de graphiques de distributions. """

    def __init__(self, yB, yA_range, quantile, n_methodes=3):
        # Données par quantile
        self.yB = yB
        self.yA_range = yA_range
        self.quantile = quantile
        # Titres et labels pour les graphiques
        self.titre = "Comparaison du fitting des distributions simples et doubles"
        self.titre_simple_auto = "Fitting automatique simple"
        self.titre_simple_manuel = "Fitting manuel simple"
        self.titre_double = "Fitting double"
        self.xlabel = "Valeurs de yB"
        self.ylabel = "Densité"
        # Couleurs pour les différentes distributions
        self.colors = ['blue', 'red', 'green', 'purple', 'black', 'brown', 'cyan']
        # Paramètre pour le nombre de méthodes de fitting à comparer
        self.n_methodes = n_methodes

    def graph_dist(self):
        """ Trace un histogramme simple qui sert 
        de visualisation d'une distribution. """

        if isinstance(self.yB, list):
            yB = np.concatenate([np.asarray(v) for v in self.yB if len(v) > 0]) if len(self.yB) > 0 else np.array([])
        else:
            yB = np.asarray(yB)

        plt.figure()
        plt.hist(yB, bins=BINS, weights=np.ones_like(self.yB)/len(self.yB), color='orange')
        plt.title(f"yB pour yA_range={self.yA_range} ({self.quantile})")
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.grid()
        plt.show()

    def graph_eval_n_methodes(self, resultats_fitting):
        """Fais les graphiques évalués sur une liste de distributions théoriques.
        On met en paralléle les graphiques qui sont évalués avec
        les différentes méthodes de fitting (simple auto, simple manuel, double).
        Pour chaque fenêtre on a donc 3 distributions évaluées
        avec toutes les distributions de test (gamma, lognorm, norm,...)

        Pour pouvoir faire des graphiques qui contiennent
        plusieurs évaluations, on doit pouvoir gèrer l'information
        transmise par toutes les évaluations. La partie paramètres
        est donc divisée aussi en plusieurs dictionnaires: correspondant
        à chaque méthode de fitting pour le quantile correspondant.
        """
        # Vérification de nos données
        check_vecteur_vide(self.yB, "yB")
        check_vecteur_nan(self.yB, "yB")

        # Grille de graphiques
        fig, axes = plt.subplots(1, self.n_methodes, figsize=(15, 5)) # 1 quantile, n méthodes par fenêtre
        axes_flat = axes.flatten()

        for i in range (self.n_methodes):
            ax = axes_flat[i]

            # Histogramme des données expérimentales
            if self.yB.size > 0:
                ax.hist(self.yB, bins=BINS, density=True, color='orange')            
            else:
                ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')

            # Comparaison des distributions théoriques ajustées
            best = stats_scores_fittings(resultats_fitting[i])

            # Intervalle pour le tracé des pdf
            abs_axe = np.linspace(min(self.yB), max(self.yB), len(self.yB))

            # Graphique des distributions théoriques ajustées
            for nom_dist, res in resultats_fitting[i].items():
                dist = res['dist']
                params = res['params'][i]
                try:
                    pdf = dist.pdf(abs_axe, *params)
                    if res == best:
                        label = r"$\bf{" + res['nom'].replace(' ', r'\ ') + \
                                f"\ (BIC={res['bic']:.2f})" + "}$"
                    else:
                        label = f"{res['nom']} (BIC={res['bic']:.2f})"
                    ax.plot(abs_axe, pdf, color=self.colors[j % len(self.colors)], label=label)
                except Exception as e:
                    print(f"Erreur avec {nom_dist}: {e}")

            # Paramètres du plot

            ax.set_xlabel(self.xlabel)
            ax.set_ylabel(self.ylabel)
            ax.grid(True)
            ax.legend()

        axes_flat[0].set_title(self.titre_simple_auto)
        axes_flat[1].set_title(self.titre_simple_manuel)
        axes_flat[2].set_title(self.titre_double)

        fig.suptitle(f'{self.titre},\n q={self.quantile} et rang yA = {self.yA_range}')
        fig.savefig(f'graph_eval_{self.n_methodes}_methodes_q{self.quantile}.png', dpi=150, bbox_inches='tight')




def graphs_eval_simple_et_double (yB, resultats_fitting, n_methodes=3):
    """Fais les graphiques évalués sur une liste de distributions théoriques.
    On met en paralléle les graphiques qui sont évalués avec
    les différentes méthodes de fitting (simple auto, simple manuel, double).
    Pour chaque fenêtre on a donc 3 distributions évaluées
    avec toutes les distributions de test (gamma, lognorm, norm,...)
    Args:
        dict_by_quantiles (dict): Contient les données classées par quantile
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        type (string): type de graphique"""
    

    

    