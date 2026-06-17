""" Ce fichier contient les fonctions qui 
contribuent au fitting de notre histogramme. """

import numpy as np
from scipy.stats import kstest, gamma

from ..constantes import *
from .scores import llog, aic, bic
from .parametres import parms_mu_sigma

def fit (resultats, y_bis, dep=None):
    """Fait le fitting pour chaque distribution
    dans la liste de possibilités DIST. Écrit un 
    dictionnaire rangé avec les caractéristiques
    de chaque choix. 
    Args:
        resultats (list): une liste qui va être remplie avec les résultats 
        du fitting pour chaque distribution.
        y_bis (numpy array): un tableau numpy qui contient les valeurs de yB 
        extraites du dictionnaire dict_yAyB, après suppression des NaN.
        dep (str, optional): le département correspondant aux données de y_bis. Par défaut, None.
    Returns:
        list: une liste de dictionnaires, chacun contenant les résultats du fitting pour une distribution 
        spécifique, y compris le nom de la distribution, les paramètres ajustés, les scores AIC et BIC, et 
        la p-value du test de Kolmogorov-Smirnov.
    """

    y_bis = np.asarray(y_bis)
    y_bis = y_bis[~np.isnan(y_bis)]
    if y_bis.size == 0:
        print("fit: pas de données valides après suppression des NaN.")
        return resultats

    for nom, dist in DIST.items():
        try:
            params = dist.fit(y_bis)
        except Exception as exc:
            print(f"Fit skipped for {nom}: {exc}")
            continue

        if np.any(np.isnan(params)):
            print(f"Fit skipped for {nom}: paramètres NaN retournés.")
            continue

        ll_val = llog(dist, params, y_bis)

        print("params best:", params)

        k = len(params)
        try:
            _, p = kstest(y_bis, lambda x: dist.cdf(x, *params))
        except Exception as exc:
            print(f"Kstest skipped for {nom}: {exc}")
            continue
                
        resultats.append({
            #"dep": dep,
            "nom": nom,
            "dist": dist,
            "params": params,
            "aic": aic(ll_val, k),
            "bic": bic(ll_val, k, len(y_bis)),
            "p-value": p
        })
    return resultats

def diff_best (best_aic, best_bic, diff_aic, diff_bic, resultats):
    for res in resultats:
        nom = res["nom"]
                
                # Eviter division par 0
        if best_aic != 0:
            diff_pct_aic = (res["aic"] - best_aic) / abs(best_aic) * 100
            diff_aic[nom].append(diff_pct_aic)

        if best_bic != 0:
            diff_pct_bic = (res["bic"] - best_bic) / abs(best_bic) * 100
            diff_bic[nom].append(diff_pct_bic)

def fit_yB(yB_q):
    """Fait un fitting des yB quantiles pour un yA donné
    dans l'histogramme et retourne les paramètres de la distribution gamma."""

    yB_q = np.asarray(yB_q, dtype=float)

    # On filtre les valeurs de yB_q pour ne garder que les valeurs strictement positives et finies
    yB_q = yB_q[np.isfinite(yB_q)]
    yB_q = yB_q[yB_q > 0]

    if yB_q.size < 2:
        raise ValueError("fit_yB: pas assez de valeurs strictement positives pour gamma.fit")

    params = gamma.fit(yB_q, floc=0)
    k, _, theta = params

    mu, sigma = parms_mu_sigma(k, theta)

    return mu, sigma


def dict_fit_yB(dict_by_quantiles):
    """ Fait un fitting des yB quantiles pour chaque yA dans bins
    et retourne un dictionnaire avec les paramètres de la distribution 
    gamma pour chaque yA
    Args:
        dict_by_quantiles (dict): un dictionnaire avec les quantiles comme clés et les informations correspondantes comme valeurs.
    Returns:
        dict: un dictionnaire avec les paramètres de la distribution gamma pour chaque yA"""
    dict_fit = {}   

    for quantile, info in dict_by_quantiles.items():
        yB_q = info["yB_q"]
        yA_q = info["yA_q"]

        if len(yB_q) > 0:
            try:
                mu, sigma = fit_yB(yB_q)
                dict_fit[yA_q] = {"mu": mu, "sigma": sigma}
            except ValueError as exc:
                print(f"Warning: bin {quantile} skipped: {exc}")
            except Exception as exc:
                print(f"Warning: fit_yB failed in bin {quantile}: {exc}")
        else:
            print(f"Warning: bin {quantile} is empty, skipping fit.")

    return dict_fit