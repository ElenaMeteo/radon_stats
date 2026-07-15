""" Dans ce fichier, on fait le fitting des distributions simples et doubles. 
Le but est de changer un peu la structure du code pour que ce soit plus clair 
et plus facile à maintenir. On va créér une classe pour les différents types
de fitting. """

import numpy as np
from scipy.optimize import minimize
from scipy.special import softmax


from ..constantes import *

#-------------- Fitting simple (une distribution) --------------
################################################################

class FittingSimple:
    """Classe de fitting pour les distributions simples 
    ("manuel" et "automatique")"""

    def __init__(self, data, dist):
        # Données
        self.data = data
        # Distribution théorique à ajuster
        self.dist = dist
        # Paramètres ajustés
        self.fitted_params_simple_auto = None
        self.fitted_params_simple_manuel = None
        self.fitted_params_double = None

    def fit_simple_auto(self):
        """Fait le fitting pour les distributions simples en utilisant
        la librairie scipy.stats.density.fit. """
        try:
            params = self.dist.fit(self.data)
            self.fitted_params_simple_auto = params
        except Exception as exc:
            print(f"Fit simple auto failed: {exc}")
        
    def fit_simple_manuel(self):
        """Fait le fitting pour les distributions simples avec des paramètres manuels. """

        def log_likelihood(params):
            eps = 1e-8
            a1, scale1 = params
            mixture = self.dist.pdf(self.data, a1, scale=scale1)
            return -np.log(mixture+eps).mean()

        initial_params = [2.0, 2.0]
        bounds = [(0, None), (0, None)]
        result = minimize(log_likelihood, initial_params, bounds=bounds, method='L-BFGS-B')
        if result.success:
            self.fitted_params_simple_manuel = result.x
        else:
            raise RuntimeError("Fit simple manuel failed: Optimization failed")

    def get_fitted_params(self):
        """Retourne les paramètres ajustés pour les 
        différents types de fitting. """
        return {
            "simple_auto": self.fitted_params_simple_auto,
            "simple_manuel": self.fitted_params_simple_manuel,
            "double": self.fitted_params_double
        }


#-------------- Fitting double (deux distributions) --------------
##################################################################

class FittingDouble:
    """Classe de fitting pour les distributions doubles. 
    On va créer des méthodes pour chaque type de fitting. """

    def __init__(self, data, dist, n_components):
        # Données
        self.data = data
        # Nombre de composantes pour le mélange de distributions
        self.n_components = n_components
        # Distribution théorique à ajuster
        self.dist = dist  # On peut changer la distribution si nécessaire
        # Paramères ajustés
        self.weights = np.ones(n_components) / n_components
        self.alphas = np.ones(n_components)
        self.scales = np.ones(n_components)
        # Paramètres ajustés
        self.fitted_params_double = None

    def _negative_log_likelihood(self, params: np.ndarray, data: np.ndarray) -> float:    # construction du logarithme de la vraisemblance
        logits, self.alphas, self.scales = np.split(params, [self.n_components, 2*self.n_components])
        self.weights = softmax(logits)

        eps = 1e-8
        neg_log_likelihood = -np.log(self._pdf(data) + eps).mean()
        return neg_log_likelihood

    def _pdf(self, x: np.ndarray) -> np.ndarray:   # définition de la pdf qui est une somme de N fonctions gamma
        mixture = np.vstack([
            self.weights[i] * self.dist.pdf(x, self.alphas[i], scale=self.scales[i])
            for i in range(self.n_components)
        ]).sum(axis=0)

        return mixture

    def fit_double(self):
        """Fait le fitting pour les distributions doubles. """
        initial_params = np.concatenate([
            np.log(self.weights),
            np.ones(2*self.n_components) + np.random.uniform(0, 0.01, 2*self.n_components) #break symmetry
        ])

        bounds = [(None, None)]*self.n_components + [(0, None)] * (2*self.n_components)
        result = minimize(
            self._negative_log_likelihood,
            initial_params, args=(self.data,), bounds=bounds
        )
        print('Success?', result['success'])

        logits, self.alphas, self.scales = np.split(result['x'], [self.n_components, 2*self.n_components])
        self.weights = softmax(logits)

        return self.weights, self.alphas, self.scales

    def get_fitted_params(self):
        """Retourne les paramètres ajustés pour le 
        fitting double. """
        self.fitted_params_double = {
            "weights": self.weights,
            "alphas": self.alphas,
            "scales": self.scales
        }
        return self.fitted_params_double


#-------------- Fonctions Adjaçantes aux Classes --------------
###############################################################
def fitting_simple_et_double(data):
    """Fait le fitting pour les distributions simples et doubles. 
    Args:
        data (numpy array): un tableau numpy qui contient les valeurs de yB 
        extraites du dictionnaire dict_yAyB, après suppression des NaN.
    Returns:
        dict: un dictionnaire contenant les paramètres ajustés pour les 
        différents types de fitting.
    """
    # Fitting simple
    params = {}

    for nom_dist, dist in DIST.items():

        fitting_simple = FittingSimple(data, dist)
        fitting_double = FittingDouble(data, dist, N_DIST)

        fitting_simple.fit_simple_auto()
        fitting_simple.fit_simple_manuel()
        fitting_double.fit_double()

        aux_params = {}

        aux_params.update(fitting_simple.get_fitted_params())
        aux_params.update(fitting_double.get_fitted_params())
        
        params[nom_dist] = aux_params

    return params
