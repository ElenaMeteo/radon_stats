""" Ce fichier contient la classe et les 
fonctions qui vons nous permettre de faire
les plots de nos distributions théoriques et
de nos données expérimentales."""

import numpy as np
import matplotlib.pyplot as plt

from ..constantes import *
from ..securite import check_vecteur_vide, check_vecteur_nan
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
        self.titres_meths = {
            "simple_auto": "Fitting automatique simple",
            "simple_manuel": "Fitting manuel simple",
            "double": "Fitting double",
        }
        self.xlabel = "Valeurs de yB"
        self.ylabel = "Densité"
        # Couleurs pour les différentes distributions
        self.colors = ['blue', 'red', 'green', 'purple', 'black', 'brown', 'cyan']
        # Paramètre pour le nombre de méthodes de fitting à comparer
        self.n_methodes = n_methodes

    def _pdf_par_methode (self, dist, res:dict, x):
        """ Attribue une pdf adapté à la situation: en cas de fitting simple, 
        commande normale. En cas de fitting double on fait une combinaison
        de commendes normales
        
        Args: 
            - dist: correspond à la distribution à travers laquelle on a fait le fitting
            - res (dict): regroupe les résultats de la distribution en incluant les paramètres 
            et les valeurs des correspondantes évaluations (calculé en _calcul_scores_(simple/double)) 
            - x (list): donne l'intervalle de définition de la distribuion au niveau des abscisses """
        
        parametres = res["params"]

        # En cas de fitting double (poids présents dans les paramètres)
        if "weights" in parametres:  
            weights, shapes, scales = parametres["weights"], parametres["shapes"], parametres["scales"]
            pdf = np.zeros_like(x, dtype=float)
            for k in range(len(weights)):
                pdf += weights[k] * dist.pdf(x, *shapes[k], scale=scales[k])
            return pdf
        # En cas de fitting simple
        else:  
            return dist.pdf(x, *parametres["shapes"], loc=parametres["loc"], scale=parametres["scale"])

    def graph_dist(self):
        """ Trace un histogramme simple qui sert 
        de visualisation d'une distribution. """

        if isinstance(self.yB, list):
            yB = np.concatenate([np.asarray(v) for v in self.yB if len(v) > 0]) if len(self.yB) > 0 else np.array([])
        else:
            yB = np.asarray(self.yB)

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

        # Méthodes de fitting à essayer
        meth = list(next(iter(resultats_fitting.values())).keys())

        # Grille de graphiques
        fig, axes = plt.subplots(1, self.n_methodes, figsize=(15, 5)) # 1 quantile, n méthodes par fenêtre
        axes_flat = np.atleast_1d(axes).flatten()

        # Intervalle pour le tracé des pdf
        abs_axe = np.linspace(min(self.yB), max(self.yB), len(self.yB)) if self.yB.size > 0 else None

        # Boucle qui traite chaque méthode
        for i, methode in enumerate(meth):
            ax = axes_flat[i]

            # Histogramme des données expérimentales
            if self.yB.size > 0:
                ax.hist(self.yB, bins=BINS, density=True, color='orange')            
            else:
                ax.text(0.5, 0.5, 'Aucune donnée', ha='center', va='center')
            
            # Regroupement de résultats par méthode (afin de parcourir le dictionnaire correctement)
            resultats_meth = {}

            for nom_dist, res_dist in resultats_fitting.items():
                resultat = res_dist[methode]
                if resultat is None:
                    continue  # des fois on n'obtient pas de résultats pertinents (simple_manuel)
                resultats_meth[nom_dist] = resultat # regroupe tous les résultats de cette méthode

            if len(resultats_meth) == 0:
                ax.text(0.5, 0.5, 'Aucun fit disponible', ha='center', va='center', transform=ax.transAxes)
                continue

            # Comparaison des distributions théoriques ajustées
            liste_dicts_res = [ # on fait une liste de  dictionnaires avec les resultats pour stats
                {**res, "nom": nom_dist}
                for nom_dist, res in resultats_meth.items()
            ]
            best_res = stats_scores_fittings(liste_dicts_res)
            best_nom = best_res['nom']

            # Boucle qui traite le graphique de chaque distribution pour chaque méthode
            for j, (nom_dist, res) in enumerate(resultats_meth.items()):
                dist = res['dist']
                try:
                    pdf = self._pdf_par_methode(dist, res, abs_axe)


                    if nom_dist == best_nom:
                        label = r"$\bf{" + nom_dist.replace(' ', r'\ ') + \
                                f"\ (BIC={res['bic']:.2f})" + "}$"
                    else:
                        label = f"{nom_dist} (BIC={res['bic']:.2f})"
                    ax.plot(abs_axe, pdf, color=self.colors[j % len(self.colors)], label=label)
                except Exception as e:
                    print(f"Erreur avec {nom_dist}: {e}")

            # Paramètres du plot
            ax.set_xlabel(self.xlabel)
            ax.set_ylabel(self.ylabel)
            ax.grid(True)
            ax.legend()
            ax.set_title(self.titres_meths.get(methode, methode))

        graphiques = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_20q/3eval/avec_filtre"
        fig.suptitle(f'{self.titre},\n q={self.quantile} et rang yA = {self.yA_range}')
        fig.savefig(f'{graphiques}/dist_yB_{self.n_methodes}eval_{self.quantile}.png', dpi=150, bbox_inches='tight')


def graphs_eval_simple_et_double (yB:np.ndarray, quantile:str, info_quantile:dict, resultats_fitting:dict, n_methodes:int=3):
    """ Fais les graphiques évalués sur une liste de distributions théoriques.
    On met en paralléle les graphiques qui sont évalués avec
    les différentes méthodes de fitting (simple auto, simple manuel, double).
    Pour chaque fenêtre on a donc 3 distributions évaluées
    avec toutes les distributions de test (gamma, lognorm, norm,...)

    Args:
        dict_by_quantiles (dict): Contient les données classées par quantile
        titre (string): titre du graphique
        xlabel (string): titre abscisses
        ylabel (string): titre ordonnées
        type (string): type de graphique """
    
    yA_range = info_quantile['yA_range']
    
    graphs_fitting = Graphs(yB, yA_range, quantile, n_methodes)
    graphs_fitting.graph_eval_n_methodes(resultats_fitting)
    
    

    