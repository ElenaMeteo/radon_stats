"""Ce document contient les fonctions
qui vont évaluer nos données avec des scores"""

import numpy as np

from ..constantes import *

def brier(prev, obs):
    """ - Brier Score: note notre efficacité"""
    
    fp = 0
    fn = 0

    seuil_prev = prev > PIC
    seuil_prev_bin = seuil_prev.astype(int) 

    seuil_obs = obs > PIC 
    seuil_obs_bin = seuil_obs.astype(int) 

    tp = np.sum((seuil_prev_bin==1) & (seuil_obs_bin==1))
    tn = np.sum((seuil_prev_bin==0) & (seuil_obs_bin==0))
    fp = np.sum((seuil_prev_bin==1) & (seuil_obs_bin==0))
    fn = np.sum((seuil_prev_bin==0) & (seuil_obs_bin==1))
    
    brier_score = np.sum((seuil_obs_bin-seuil_prev_bin)**2)/len(obs)
    # if ((tp+fn != 0) & (fp+tn != 0)):
    #     h_val = tp/(tp+fn)
    #     f_val = fp/(fp+tn)

    # else:
    #     print("\nDivision par 0!\n")
    #     exit(1)

    return brier_score, fp, fn

# ---------------------------------------------------

def llog_pdf(pdf_vals: np.ndarray, eps: float = 1e-8) -> float:
    """ Vraisemblence a partir de valeurs de pdf déjà évalués."""
    return np.sum(np.log(pdf_vals + eps))

def llog(dist, params:np.ndarray, data, eps:float=1e-8) -> float:
    """ Vraisemblence à partir de la distribution et ses paramètres """
    pdf_vals = dist.pdf(data, *params)
    return np.sum(np.log(pdf_vals + eps))

def aic(ll, k) -> float:
    return 2*k - 2*ll

def bic(ll, k, n) -> float:
    return k*np.log(n) - 2*ll

# ---------------------------------------------------

def diff_best (best_aic, best_bic, diff_aic, diff_bic, resultats):
    """Calcule les différences en pourcentage entre les scores AIC et BIC 
    de chaque distribution et les meilleurs scores.
    
    Args:
        best_aic (float): le meilleur score AIC trouvé.
        best_bic (float): le meilleur score BIC trouvé.
        diff_aic (dict): dictionnaire où on stocke les différences en pourcentage 
            pour l'AIC, indexé par le nom de la distribution.
        diff_bic (dict): dictionnaire où on stocke les différences en pourcentage 
            pour le BIC, indexé par le nom de la distribution.
        resultats (list): liste de dictionnaires contenant les résultats du fitting 
            pour chaque distribution.
    
    Returns:
        None: modifie en place les dictionnaires diff_aic et diff_bic.
    """
    for res in resultats:
        nom = res["nom"]
                
                # Eviter division par 0
        if best_aic != 0:
            diff_pct_aic = (res["aic"] - best_aic) / abs(best_aic) * 100
            diff_aic[nom].append(diff_pct_aic)

        if best_bic != 0:
            diff_pct_bic = (res["bic"] - best_bic) / abs(best_bic) * 100
            diff_bic[nom].append(diff_pct_bic)

# ---------------------------------------------------

def stats_scores_fittings(resultats):
    """ Calcule les scores AIC et BIC pour chaque distribution et
    détermine la meilleure distribution selon ces scores. Fais une
    statistique sur les comparaisons relatives entre les distributions. 
    Args:
        resultats (list): Liste de dictionnaires contenant les résultats 
        du fitting pour chaque distribution 
        
    Returns:
        best (dict): Dictionnaire contenant le recapitulatif de la meilleure 
        distribution"""

    compteur_dist = {nom: 0 for nom in DIST.keys()}
    diff_aic = {nom: [] for nom in DIST.keys()}
    diff_bic = {nom: [] for nom in DIST.keys()}

    best = min(resultats, key=lambda x: x['bic'])
    # compteur_dist[best['nom']] += 1
    best_aic = best['aic']
    best_bic = best['bic']

    diff_best(best_aic, best_bic, diff_aic, diff_bic, resultats)
    recap_stats_scores(diff_aic, diff_bic)
    # recap_stats_scores(compteur_dist, diff_aic, diff_bic)

    return best

def recap_stats_scores(diff_aic, diff_bic, compteur_dist=None):
    # print("\n\nMeilleures distributions:", dict(compteur_dist))

    mean_diff_aic = {k: np.mean(v) for k, v in diff_aic.items()}
    mean_diff_bic = {k: np.mean(v) for k, v in diff_bic.items()}

    print("Moyenne (%) difference AIC:")
    print(mean_diff_aic)

    print("\nMoyenne (%) difference BIC:")
    print(mean_diff_bic)
    return
   

