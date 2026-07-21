""" Dans ce fichier, on fait le fitting des distributions simples et doubles.
Pour la simple on utilise deux méthodes: un automatique qui se base sur le fit 
de scipy.stats et un manuel qui se base sur l'optimisation de la vraisemblance.

Une partie importante du code est de maintenir une stucture de lecture des 
résultats des paramètres optimisés pour pouvoir utiliser les fonctions de 
graphiques et/ou de statistiques de manière libre. 

Chaque classe correspond à un type différent de fitting."""

import numpy as np
from scipy.optimize import minimize
from scipy.special import softmax
from scipy.stats import kstest

from ..constantes import *
from ..eval.scores import llog_pdf, llog, aic, bic, stats_scores_fittings
from ..documents.docs import docs_dict_params

# Là on va garder nos résultats .csv
dossier = Path(__file__).parent.parent
dossier_docs = dossier / "docs"
dossier_json = dossier / "json"


#-------------- Fitting simple (une distribution) --------------
################################################################

class FittingSimple:
    """ Classe de fitting pour les distributions simples.
    On fait un fitting avec une seule distribution.
    ("manuel" et "automatique") """

    def __init__(self, data:np.ndarray, dist) -> None:
        # Données
        self.data = data
        # Distribution théorique à ajuster
        self.dist = dist
        # Nombre de paramètres de la distribution
        self.n_shapes = dist.numargs 
        # Paramètres ajustés
        self.fitted_params_simple_auto = None
        self.fitted_params_simple_manuel = None

    def fit_simple_auto(self) -> None:
        """ Fait le fitting pour les distributions simples en utilisant
        la librairie scipy.stats.density.fit. """
        try:
            # Calcul des paramètres ajustés pour le fitting automatique
            params = self.dist.fit(self.data)
            # self.fitted_params_simple_auto = params

            # Structure de lecture pour les graphiques
            shapes = params[:self.n_shapes]
            loc = params[self.n_shapes]
            scale = params[self.n_shapes + 1]

            self.fitted_params_simple_auto = {
                "shapes": list(shapes),
                "loc": loc,
                "scale": scale
            }
        except Exception as exc:
            print(f"Fit simple auto failed: {exc}")
        
    def fit_simple_manuel(self, fit_loc=True) -> None:
        """ Fait le fitting pour les distributions simples avec des paramètres
        manuels en optimizant la vraisemblance. 

        Args: 
            fit_loc (bool): Paramètre qui détermine si on prend en compte 
            la moyenne dans le fitting. De base on va toujours le prendre en compte 
            sauf demande du contraire."""

        # Nombre de paramètres de la distribution
        n = self.n_shapes

        # Fonction qui décompose les paramètres en formes, loc et scale
        def unpack(params:np.ndarray):
            """ Décomposition des paramètres obtenus pour avoir un format
            adapté pour la lecture. """
            shapes = params[:n]
            loc = params[n] if fit_loc else 0
            scale = params[-1]
            return shapes, loc, scale
        
        # Fonction de vraisemblance négative pour l'optimisation
        def log_likelihood(params:np.ndarray) -> float:
            eps = 1e-8
            shapes, loc, scale = unpack(params)
            mixture = self.dist.pdf(self.data, *shapes, loc=loc, scale=scale)
            return -np.log(mixture+eps).mean()

        # Paramètres initiaux
        data_min = np.min(self.data)
        data_std = np.std(self.data)

        initial_shapes = np.ones(n)  # init shapes
        initial_loc = data_min - 0.1 * data_std if fit_loc else 0
        # initial_loc = data_min - 1e-3 if fit_loc else 0  # init loc en dessous du minimum
        initial_scale = data_std if data_std > 0 else 1.0 # init scale

        if fit_loc:
            initial_params = np.concatenate([initial_shapes, [initial_loc, initial_scale]])
        else:
            initial_params = np.concatenate([initial_shapes, [initial_scale]])

        # Bornes pour l'optimisation
        bounds = [(1e-3, None)] * n  # shapes > 0
        if fit_loc:
            bounds += [(None, data_min - 1e-6)] 
        bounds += [(1e-3, None)]  # scale > 0

        # Optimisation des paramètres
        result = minimize(
            log_likelihood, initial_params, bounds=bounds, method='L-BFGS-B',
            options={'maxiter':1000, 'ftol':1e-12, 'gtol':1e-8})

        # Structure de lecture pour les graphiques
        if result.success:
            shapes, loc, scale = unpack(result.x)
            self.fitted_params_simple_manuel = {"shapes": list(shapes), "loc": loc, "scale": scale}
        else:
            print(f"Erreur fitting simple manuel pour {self.dist.name}: {result.message}")
            self.fitted_params_simple_manuel = None

    def get_fitted_params(self) -> dict:
        """Retourne les paramètres ajustés pour les 
        différents types de fitting. """
        return {
            "auto": self.fitted_params_simple_auto,
            "manuel": self.fitted_params_simple_manuel
        }


#-------------- Fitting double (deux distributions) --------------
##################################################################

class FittingDouble:
    """Classe de fitting pour les distributions doubles. 
    On va créer des méthodes pour chaque type de fitting. """

    def __init__(self, data:np.ndarray, dist, n_components:int) -> None:
        # Données
        self.data = data
        # Nombre de composantes pour le mélange de distributions
        self.n_components = n_components
        # Distribution théorique à ajuster
        self.dist = dist  # On peut changer la distribution si nécessaire
        # Nombre de paramètres de la distribution 
        self.n_shapes = dist.numargs
        # Paramètres ajustés
        self.weights = np.ones(n_components) / n_components
        self.shapes = np.ones((n_components, self.n_shapes)) # Matrice en fonction du nombre de dist et de shapes
        self.locs = np.zeros(n_components)
        self.scales = np.ones(n_components)
        # Paramètres ajustés
        self.fitted_params_double = None

    # Fonction qui met en place le format dont on a besoin pour la lecture
    def _unpack(self, params: np.ndarray):
        n_c, n_s = self.n_components, self.n_shapes
        logits = params[:n_c]
        shapes = params[n_c : n_c + n_c*n_s].reshape(n_c, n_s)
        locs   = params[n_c + n_c*n_s : n_c + n_c*n_s + n_c]
        scales = params[n_c + n_c*n_s + n_c :]
        return softmax(logits), shapes, locs, scales
    
    # Mélange des deux pdf's en fonction des poids
    def _pdf(self, x:np.ndarray) -> np.ndarray:
        mixture = np.zeros_like(x, dtype=float)
        for i in range(self.n_components):
            # Sans loc sur la pdf
            mixture += self.weights[i] * self.dist.pdf(x, *self.shapes[i], scale=self.scales[i])
            # Avec loc sur la pdf
            # mixture += self.weights[i] * self.dist.pdf(x, *self.shapes[i], loc=self.locs[i], scale=self.scales[i])
        return mixture

    # Calcul de la vraisemblance pour optimisation
    def _negative_log_likelihood(self, params: np.ndarray, data: np.ndarray) -> float:
        self.weights, self.shapes, self.locs, self.scales = self._unpack(params)
        eps = 1e-8
        return -np.log(self._pdf(data) + eps).mean()

    def fit_double(self) : # -> paramètres
        """Fait le fitting pour les distributions doubles. """
        n_c, n_s = self.n_components, self.n_shapes
        initial_params = np.concatenate([
            np.log(self.weights), # weights
            (np.ones(n_c * n_s) + np.random.uniform(0, 0.01, n_c * n_s)), # shapes
            np.zeros(n_c) + np.random.uniform(-0.01, 0.01, n_c), # les locs commencent proches de 0
            np.ones(n_c) + np.random.uniform(0, 0.01, n_c), # scales
        ])

        bounds = (
        [(None, None)] * n_c            # logits
        + [(1e-3, None)] * (n_c*n_s)    # shapes > 0
        + [(None, None)] * n_c          # locs libres
        + [(1e-3, None)] * n_c          # scales > 0
        )

        # result['x'] contient les parametres optimisés dans le même ordre que "initial_params"
        result = minimize(self._negative_log_likelihood, initial_params, 
                          args=(self.data,), bounds=bounds)
        print('Success?', result['success'])

        self.weights, self.shapes, self.locs, self.scales = self._unpack(result['x'])
        return self.weights, self.shapes, self.locs, self.scales

    def get_fitted_params(self) -> dict:
        """Retourne les paramètres ajustés pour le 
        fitting double. """
        self.fitted_params_double = {
            "weights": self.weights,
            "shapes": self.shapes,   # array (n_components, n_shapes)
            "locs": self.locs,
            "scales": self.scales,
        }
        return self.fitted_params_double

    # def _negative_log_likelihood(self, params: np.ndarray, data: np.ndarray) -> float:    # construction du logarithme de la vraisemblance
    #     logits, self.alphas, self.scales = np.split(params, [self.n_components, 2*self.n_components])
    #     self.weights = softmax(logits)

    #     eps = 1e-8
    #     neg_log_likelihood = -np.log(self._pdf(data) + eps).mean()
    #     return neg_log_likelihood

    # def fit_double(self):
    #     initial_params = np.concatenate([
    #         np.log(self.weights),
    #         np.ones(2*self.n_components) + np.random.uniform(0, 0.01, 2*self.n_components) #break symmetry
    #     ])

    #     bounds = [(None, None)]*self.n_components + [(0, None)] * (2*self.n_components)
    #     result = minimize(
    #         self._negative_log_likelihood,
    #         initial_params, args=(self.data,), bounds=bounds
    #     )
    #     print('Success?', result['success'])

    #     logits, self.alphas, self.scales = np.split(result['x'], [self.n_components, 2*self.n_components])
    #     self.weights = softmax(logits)

    #     return self.weights, self.alphas, self.scales


class Scores:
    """ Classe qui calcule les scores de chaque fitting
    afin d'avoir une étude statistique"""

    def __init__(self, data: np.ndarray, dist, nom_dist: str, params: dict) -> None:
        self.data = data
        self.dist = dist
        self.nom_dist = nom_dist
        self.params = params

        self.ll_val = None
        self.aic_val = None
        self.bic_val = None
        self.p = None

        self.stats_simple_auto = None
        self.stats_simple_manuel = None
        self.stats_double = None

        self.all_stats = None

    # Éxecution des calculs
    def _calcul_scores_simple (self, parametres: dict, fit_loc=True) -> dict:
        """ Processus de calcul des scores commun
        à toutes les méthodes """

        flat_params = (*parametres["shapes"], parametres["loc"] if fit_loc==True else None, parametres["scale"]) # format de parametres en liste
        n_params = len(flat_params)

        self.ll_val = llog(self.dist, flat_params, self.data, eps=1e-8)
        self.aic_val = aic(self.ll_val, n_params)
        self.bic_val = bic(self.ll_val, n_params, len(self.data))
        try:
            _, self.p = kstest(self.data, lambda x: self.dist.cdf(x, 
                                                             *parametres["shapes"], 
                                                             loc=parametres["loc"], 
                                                             scale=parametres["scale"]))
        except Exception as exc:
            print(f"Kstest sauté pour {self.nom_dist}: {exc}")
            self.p = None

        resultats_stats = {"dist": self.dist,
            "params": parametres,
            "aic": self.aic_val,
            "bic": self.bic_val,
            "p-value": self.p}
        
        return resultats_stats
    
    def _calcul_scores_double(self) -> dict:
        """ Lance l'algo pour la partie double """
        parametres = self.params["double"]
        weights, shapes, locs, scales = (
            parametres["weights"], parametres["shapes"], 
            parametres["locs"], parametres["scales"]
        )

        def mixture_pdf(x):
            return sum(
                # pdf sans loc
                weights[i] * self.dist.pdf(x, *shapes[i], scale=scales[i])
                # pdf avec loc
                # weights[i] * self.dist.pdf(x, *shapes[i], loc=locs[i], scale=scales[i])
                for i in range(len(weights))
            )

        def mixture_cdf(x):
            return sum(
                # cdf sans loc
                weights[i] * self.dist.cdf(x, *shapes[i], scale=scales[i])
                # cdf avec loc
                # weights[i] * self.dist.cdf(x, *shapes[i], loc=locs[i], scale=scales[i])
                for i in range(len(weights))
            )
        
        self.ll_val = llog_pdf(mixture_pdf(self.data))

        # n_params sans loc
        n_params = len(weights) - 1 + shapes.size + len(scales)
        # n_params avec loc
        # n_params = len(weights) - 1 + shapes.size + len(locs) + len(scales)
        self.aic_val = aic(self.ll_val, n_params)
        self.bic_val = bic(self.ll_val, n_params, len(self.data))

        try:
            _, self.p = kstest(self.data, mixture_cdf)
        except Exception as exc:
            print(f"Kstest sauté pour {self.nom_dist} (double): {exc}")
            self.p = None

        resultats_stats = {
            "dist": self.dist,
            "params": parametres,
            "aic": self.aic_val,
            "bic": self.bic_val,
            "p-value": self.p,
        }

        return resultats_stats
        
    def scores_simple_auto (self) -> None:
        """ Lance l'algo pour la partie simple automatique """
        # Séléction des paramètres correspondants
        parametres = self.params["simple"]["auto"]
        # On lance le calcul
        self.stats_simple_auto = self._calcul_scores_simple(parametres)

    def scores_simple_manuel (self) -> None:
        """ Lance l'algo pour la partie simple manuelle """
        # Séléction des paramètres correspondants
        parametres = self.params["simple"]["manuel"]
        # On lance le calcul
        self.stats_simple_manuel = self._calcul_scores_simple(parametres)

    def scores_double (self) -> None:
        """ Lance l'algo pour la partie double """
        # On lance le calcul (les paramètres sont dans la fonction)
        self.stats_double = self._calcul_scores_double()

    def get_eval (self) -> dict:
        """ Donne les résultats en doctionnaire
        prêt à la lecture"""
        self.all_stats = {"simple_auto": self.stats_simple_auto,
                          "simple_manuel": self.stats_simple_manuel,
                          "double": self.stats_double}
        
        return self.all_stats

#-------------- Fonctions Adjaçantes aux Classes --------------
###############################################################

def fitting_simple_et_double(yB:np.ndarray, dossier_json) -> dict:
    """ Fait le fitting pour les distributions simples et doubles
    pour un quantile donné. On retourne un dictionnaire avec les 
    paramètres ajustés pour les différents types de fitting.
    Args:
        yB (numpy array): un tableau numpy qui contient les valeurs de yB 
        extraites du dictionnaire dict_yAyB, après suppression des NaN.
    Returns:
        dict: un dictionnaire contenant les paramètres ajustés pour les 
        différents types de fitting.
    """
    # Fitting simple
    resultats_fitting = {}

    print("Dans la boucle\n")

    for nom_dist, dist in DIST.items():

        print(f"Essai pour {nom_dist}\n")

        # Fitting simple et double
        fitting_simple = FittingSimple(yB, dist)
        print("Init fitting simple fini")
        fitting_double = FittingDouble(yB, dist, N_DIST)
        print("Init fitting double fini")


        fitting_simple.fit_simple_auto()
        print("Fitting simple automatique fini")
        # fit_loc = (nom_dist != "weibull_min") # La méthode manuelle ne marche pas avec loc et weibull
        fitting_simple.fit_simple_manuel()
        # fitting_simple.fit_simple_manuel(fit_loc=fit_loc)
        print("Fitting simple manuel fini")
        fitting_double.fit_double()
        print("Fitting double fin")

        # Structure des paramètres ajustés
        params = {}

        params["simple"] = fitting_simple.get_fitted_params()
        print("Obtention paramètres simples")
        params["double"] = fitting_double.get_fitted_params()
        print("Obtention paramètres doubles")

        # Enregistrement du dictionnaire

        ad_dict_params = dossier_json / "dict_params_dist_et_quant" 
        docs_dict_params(params, ad_dict_params) #! fonction pas encore écrite
        
        # Évaluation des distributions

        stats_du_fit = Scores(yB, dist, nom_dist, params)
        print("Init scores fini")

        stats_du_fit.scores_simple_auto()
        print("Scores simple automatique fini")
        stats_du_fit.scores_simple_manuel()
        print("Scores simple manuel fini")
        stats_du_fit.scores_double()
        print("Scores double fini")


        # Recap du fitting et evaluation
        resultats_fitting[nom_dist] = stats_du_fit.get_eval()
        """ La structure des résultats est la suivante:
        resultats_fitting = {
            "gamma":   {"simple_auto": {...},  "double": {...}}, 
            "lognorm": {"simple_auto": {...},  "double": {...}},
            "norm":    {"simple_auto": {...},  "double": {...}},
        } 
        Dictionnaire à parcourrir en prennant cela en compte """
        print("Résultats ajoutés au dictionnaire\n")
        

    print("Boucle finie!\n")
    print("Résultats:", resultats_fitting)
    # Statistiques sur nos résultats
    # stats_scores_fittings(resultats_fitting)  # On peut appeler cette fonction ici

    return resultats_fitting
