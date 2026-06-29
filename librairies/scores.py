"""Ce document contient les fonctions
qui vont évaluer nos données avec des scores"""

import numpy as np

from .constantes import *

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

def llog(dist, params, data):
    return np.sum(dist.logpdf(data, *params))

def aic(ll, k):
    return 2*k - 2*ll

def bic(ll, k, n):
    return k*np.log(n) - 2*ll

def recap_stats_scores(compteur_dist, diff_aic, diff_bic):
    print("\n\nMeilleures distributions:", dict(compteur_dist))

    mean_diff_aic = {k: np.mean(v) for k, v in diff_aic.items()}
    mean_diff_bic = {k: np.mean(v) for k, v in diff_bic.items()}

    print("Moyenne (%) difference AIC:")
    print(mean_diff_aic)

    print("\nMoyenne (%) difference BIC:")
    print(mean_diff_bic)
    return
   

