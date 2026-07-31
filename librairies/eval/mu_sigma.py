"""Ce fichier contient les fonctions qui vont participer
à déterminer les régressions pour les valeurs de tous
les paramètres"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

from ..constantes import *

def plot_regression(x, y, xlabel, ylabel, titre, ad_graph, nom_doc):
    """
    Ajusta una regresión lineal entre dos vectores y dibuja el resultado.

    Args:
        x (array-like): variable independiente.
        y (array-like): variable dependiente.
        xlabel (str): etiqueta eje x.
        ylabel (str): etiqueta eje y.
        title (str): título del gráfico.

    Returns:
        dict con los parámetros de la regresión.
    """

    x = np.asarray(x)
    y = np.asarray(y)

    # Elimine les possibles NaN
    mask = np.isfinite(x) & np.isfinite(y)
    x = x[mask]
    y = y[mask]

    # Regréssion linéaire
    reg = linregress(x, y)

    pente = reg.slope
    intercept = reg.intercept
    r = reg.rvalue
    r2 = r**2

    # Droite ajustée
    x_fit = np.linspace(x.min(), x.max(), 200)
    y_fit = pente * x_fit + intercept

    # Graphique
    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, label="Données")
    plt.plot(
        x_fit,
        y_fit,
        "r",
        label=f"y = {pente:.4f}x + {intercept:.4f}\n$R^2$ = {r2:.4f}"
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titre)
    plt.grid(True)
    plt.legend()
    plt.savefig(f'{ad_graph}/regression_{nom_doc}.png', dpi=150, bbox_inches='tight')

    print(f"Equation : y = {pente:.6f} x + {intercept:.6f}")
    print(f"R² = {r2:.6f}")
    print(f"r = {r:.6f}")
    print(f"p-value = {reg.pvalue:.3e}")

    return {
        "slope": pente,
        "intercept": intercept,
        "r2": r2,
        "r": r,
        "pvalue": reg.pvalue,
        "stderr": reg.stderr,
    }


def extract_mean_std(resultats_all_q, methode, nom_dist):
    """
    Extrae la media y la desviación típica (raíz de la varianza)
    para una distribución y un método dados, recorriendo todos los cuantiles.

    Args:
        resultats_all_q (dict): diccionario con todos los cuantiles.
        methode (str): "simple_auto", "simple_manuel" o "double".
        nom_dist (str): "gamma", "norm", "lognorm", ...

    Returns:
        mu (list): media para cada cuantil.
        sigma (list): desviación típica para cada cuantil.
        weights_list (list): pesos (o None) para cada cuantil.
    """

    mu = []
    sigma = []
    weights_list = []

    dist = DIST[nom_dist]

    for quantile, res_quantile in resultats_all_q.items():

        res = res_quantile[nom_dist][methode]

        if res is None:
            mu.append(np.nan)
            sigma.append(np.nan)
            weights_list.append(None)
            continue

        params = res["params"]

        # Distribution simple
        if methode != "double":

            shapes = params["shapes"]
            loc = params["loc"]
            scale = params["scale"]

            # NOTE: antes esta línea era "mu = dist.mean(...)", lo cual
            # SOBREESCRIBÍA la lista mu con un escalar en cada iteración.
            # Ahora usamos una variable local "moy" y la añadimos con append.
            moy = dist.mean(*shapes, loc=loc, scale=scale)
            var = dist.var(*shapes, loc=loc, scale=scale)
            ect = np.sqrt(var)

            weights_list.append(None)

        # Distribution double
        else:
            weights = np.asarray(params["weights"])
            shapes = params["shapes"]
            locs = params["locs"]
            scales = params["scales"]

            moy_comp = np.array([
                dist.mean(*shapes[i], loc=locs[i], scale=scales[i])
                for i in range(len(weights))
            ])

            ect_comp = np.array([
                np.sqrt(dist.var(*shapes[i], loc=locs[i], scale=scales[i]))
                for i in range(len(weights))
            ])

            # NOTE: antes se calculaba una media/varianza "combinada" de la
            # mezcla (np.sum(weights * ...)), lo que daba un escalar. Pero
            # regression_params espera un array por componente en cada
            # quantile (mu1 = [m[0] for m in mu_double], mu2 = [m[1] ...]),
            # así que aquí guardamos moy_comp y ect_comp tal cual, sin
            # combinarlos entre componentes.
            moy = moy_comp
            ect = ect_comp

            weights_list.append(weights)

        mu.append(moy)
        sigma.append(ect)

    return mu, sigma, weights_list

def regression_params(resultats_all_q, yA_abscisses):
    """Cette fonction trace la regression des paramètres
    concernés par la distribution et ses résultats"""

    yA_abscisses = np.array(yA_abscisses)
    yA_sqrt_abscisses = np.sqrt(yA_abscisses)

    # Titre régressions
    xlabel = "yA moyen des quantiles"

    ylabel_mu = "Moyenne de la distribution optimisée"
    ylabel_sigma = "Écart-type de la distribution optimisée"
    ylabel_weights = "Poids de la double distribution optimisés"

    titre_mu_simple = "Régression linéaire des moyennes par quantile\nMéthode simple"
    titre_sigma_simple = "Régression linéaire des écart-types par quantile\nMéthode simple"

    titre_mu1_double = "Régression linéaire des moyennes par quantile\nMéthode double - 1ère partie"
    titre_mu2_double = "Régression linéaire des moyennes par quantile\nMéthode double - 2ème partie"

    titre_sigma1_double = "Régression linéaire des écart-types par quantile\nMéthode double - 1ère partie"
    titre_sigma2_double = "Régression linéaire des écart-types par quantile\nMéthode double - 2ème partie"
    titre_weights = "Régression linéaire des poids de la méthode double"

    # Distribution log-norm pour fitting simple
    mu_simple, sigma_simple, _ = extract_mean_std(resultats_all_q, "simple_manuel", "log-norm")

    plot_regression(
        yA_abscisses, 
        mu_simple, 
        xlabel, 
        ylabel_mu, 
        titre_mu_simple, 
        REG_10Q_FILTRE, 
        nom_doc="mu_simple")
    
    plot_regression(
        yA_sqrt_abscisses, 
        sigma_simple, 
        xlabel, 
        ylabel_sigma, 
        titre_mu_simple,
        REG_10Q_FILTRE,
        nom_doc="sigma_simple")

    # Distribution gamma pour fitting double
    mu_double, sigma_double, weights = extract_mean_std(resultats_all_q, "double", "gamma")

    mu1 = [m[0] for m in mu_double]
    mu2 = [m[1] for m in mu_double]

    sigma1 = [s[0] for s in sigma_double]
    sigma2 = [s[1] for s in sigma_double]

    w1 = [w[0] for w in weights]

    # Plot premier mu
    plot_regression(
        yA_abscisses,
        mu1,
        xlabel,
        ylabel_mu,
        titre_mu1_double,
        REG_10Q_FILTRE,
        nom_doc="mu1"
    )
    # Plot deuxième mu
    plot_regression(
        yA_abscisses,
        mu2,
        xlabel,
        ylabel_mu,
        titre_mu2_double,
        REG_10Q_FILTRE,
        nom_doc="mu2"
    )
    # Plot premier sigma
    plot_regression(
        yA_sqrt_abscisses,
        sigma1,
        xlabel,
        ylabel_sigma,
        titre_sigma1_double,
        REG_10Q_FILTRE,
        nom_doc="sigma1"
    )
    # Plot deuxième sigma
    plot_regression(
        yA_sqrt_abscisses,
        sigma2,
        xlabel,
        ylabel_sigma,
        titre_sigma2_double,
        REG_10Q_FILTRE,
        nom_doc="sigma2"
    )
    # Plot weights
    plot_regression(
        yA_abscisses,
        w1,
        xlabel,
        ylabel_weights,
        titre_weights,
        REG_10Q_FILTRE,
        nom_doc="weights"
    )