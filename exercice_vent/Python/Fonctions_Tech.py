############################
### Fonctions Techniques ###
############################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, truncnorm, gamma
from These_MF.exercice_vent.Python.Variables import *

" Fonctions techniques pour la 1ere partie: analyse statistique "

# Sort la liste de probabilités de l'évenement E chaque jour
def prob(cond_prev, k):
    if k == 1:
        prob = cond_prev.astype(int)
    else:
        prob = np.sum(cond_prev, axis=1)/k
    return prob

# Sort une liste des probabilités prévues et ses fréquences de prévision
def Np(prob):
    vals, counts = np.unique(prob, return_counts=True)
    return np.vstack([vals, counts]).T

# Sort une liste des probabilités prévues et ses fréquences réelles

def pPrime(cond_obs, prob, Np):
    cond_obs= np.asarray(cond_obs, dtype=int)
    prob = np.asarray(prob)
    Np = np.asarray(Np)
    # On prend le vecteur de probas
    pVals = Np[:,0]
    # On créé une matrice booléenne qui indique les jours qui ont une proba p
        # Il s'agit de comparer toutes les probas avec les resultats de TOUS les jours
        # mask[j,i] = True sii prob[j] == pVals[i]
    mask = prob[:, None] == pVals[None,:] 
    # Pour chaque p, on additionne les cond_obs des jours où prob(jour) = p
        # mask et cond_obs agissent comme des indicatrices de p et epsilon 
        # en les mutipliant on obtient la double condition: evenement produit et p prévu
    sums = mask.T @ cond_obs 
    # On divise entre les fréquences Np
    p_prime = sums/Np[:,1]
    return np.column_stack([pVals, p_prime])

# Sort une liste des fréquences de prévision correctes (alarmes legitimes)
def H(cond_obs, prob, k):
    cond_obs = np.asarray(cond_obs, dtype=int)
    prob = np.asarray(prob)
    
    pCats = np.arange(k+1)/k
    N1 = cond_obs.sum()
    
    mask = prob[:, None] >= pCats[None, :]
    Hvals = (mask * cond_obs[:, None]).sum(axis=0) / N1
    return Hvals

# Sort une liste des fréquences de prévision incorrectes (fausses alarmes) 
def F(cond_obs, prob, k):
    cond_obs = np.asarray(cond_obs, dtype=int)
    prob = np.asarray(prob)
    
    indC = 1 - cond_obs
    pCats = np.arange(k+1)/k
    N0 = indC.sum()
    
    mask = prob[:, None] >= pCats[None, :]
    Fvals = (mask * indC[:, None]).sum(axis=0) / N0
    return Fvals

# Sort la probabilité climatologique de l'évenement
def pC(cond_obs, N):
    return np.mean (cond_obs)

# SCORES 
########

# Score de Brier
def BrierFiab(Np, pPrime, N): 
    Np = np.asarray(Np)
    pPrime = np.asarray(pPrime)
    return np.sum(Np[:,1] * (Np[:,0] - pPrime[:,1])**2) / N

def BrierRes(Np, pPrime, N, pc):
    Np = np.asarray(Np)
    pPrime = np.asarray(pPrime)
    return np.sum(Np[:,1] * (pPrime[:,1] - pc)**2) / N

def Brier(Np, pPrime, N, pc):
    return BrierFiab(Np, pPrime, N) - BrierRes(Np, pPrime, N, pc) + pc * (1-pc)

def BSS(Np, pPrime, N, pc):
    bf = BrierFiab(Np, pPrime, N)
    br = BrierRes(Np, pPrime, N, pc)
    bi = pc * (1-pc)
    return (br - bf)/bi

# Catégorie de probabilité optimale
def pointROC (dictionnaire, k):
    titres = list(dictionnaire.keys())
    matrices = list(dictionnaire.values())
    pCats = np.arange(k+1)/k

    print("Les catégories de probabilité optimale sont:\n")
    for i, mat in enumerate(matrices):
        dist = np.sqrt((mat[:,0])**2 + (mat[:,1] - 1)**2)
        for idx in pCats:
            idx = np.argmin(dist)
        
        print(f"{titres[i]}:\n", pCats[idx])    

    return

# Données d'exemple pour vérifier la validité des fonctions

obs = [True, False, False, True, True, False, True, False, False, False]
prob_vector = [5./6, 1./6, 2./6, 4./6, 3./6, 4./6, 5./6, 5./6, 3./6, 3./6]
# Np_vector = [[1./6, 1], [2./6, 1], [3./6, 3], [4./6, 2], [5./6, 3]]
Np_vector = Np(prob_vector)
pPrime_vector = pPrime(obs, prob_vector, Np_vector)

" Jusqu'à maintenant nous avons réalisé une analyse ststistique des   "
" données par rapport à des observations et analyses en définissant   "
" des événements pour les percentiles 50% et 90%. Maintenant, on va   "
" réaliser la même analyse, mais cette fois ci, en prennant en compte "
" les erreurs de représentativité. "

" Fonctions techniques pour la 2eme partie: analyse des perturbations "

# def CRPS (dist, obs, N):
    
#     X = np.random.dist(N)

#     # Utilise N^2 paires (X,obs) et (X,X') 
#     aux = np.mean(np.abs(X[:, None] - obs[None, :]))
#     aux -= 0.5 * np.mean(np.abs(X[:, None] - X[None, :]))

#     return aux bb

" Fonctions pour le vent à 10m "

def param_vent (maille, y):
    # Ici delta c'est le pas du maillage
    moy_y = y.sum()/(len(y))
    alpha0 = -0.02*maille
    alpha1 = 1 + 0.002*maille
    beta1 = -0.04*maille + 0.17*maille**(0.75)

    mu = alpha0 + alpha1*moy_y
    sigma_repre = beta1 * np.sqrt(moy_y) + epsilon

    return mu, sigma_repre

def conv_vent (y, nVal, obs, maille):
    y = y.copy()
    mu, sigma_repre = param_vent(maille, y)

    sigma_mesure = np.maximum(0.2, 0.05*obs)
    sigma = np.sqrt(sigma_mesure**2 + sigma_repre**2)

    # Paramètres pour la cut-off à 0
    a1 = (0 - mu) / sigma_repre
    a2 = (0 - mu) / sigma
    b = np.inf

    # Distribution de l'erreur 
    dist1 = truncnorm(a1, b, loc=mu, scale=sigma_repre)
    dist2 = truncnorm(a2, b, loc=mu, scale=sigma)
    samples = dist2.rvs(size=nVal) # Prend nVal valeurs aléatoires suivant dist
    moy_samples = np.mean(samples)
    var_samples = np.var(samples)
    y += samples - moy_samples

    # return y, var_samples
    return y

def sigmaMean (bd, obs, delta):
    beta = -0.04*delta + 0.17*delta**(0.75)
    moy_y = bd.mean(axis=1)
    sigma_repre = beta * np.sqrt(moy_y) + epsilon
    sigma_mesure = np.maximum(0.2, 0.05 * obs)
    sigma_mean = np.sqrt(sigma_mesure**2 + sigma_repre**2).mean()

    return sigma_mean

def RMSEcheck (prev, obs):
    rmse = s0(prev, obs)
    prev_mean = prev.mean(axis=1)
    rmse = np.sqrt(np.mean((prev_mean - obs)**2))
    var = np.sqrt(np.mean(prev.var(axis=1)))
    return rmse, var

" Fonctions techniques pour la 3eme partie: analyse des perturbations 2 "

# On prend le score RMSE comme score de base
def s0 (prob, OBS):
    brier = ((prob-OBS)**2).sum()/len(prob)
    return brier

# Score modifié basé sur l'article
def s (prob, OBSval, erreur):
    # Probabilité de rater
    denom = 1 - erreur[0] - erreur[1]

    print("Denominateur = ", denom)
    print("s0(prob, OBSval) = ", s0(prob, OBSval))
    print("s0(prob, 1-OBSval) = ", s0(prob, 1-OBSval))

    score0 = s0(prob, OBSval)
    score0 +=  (erreur[0] * (s0(prob, OBSval) - s0(prob, 1-OBSval))) / denom

    score1 = s0(prob, OBSval)
    score1 +=  (erreur[1] * (s0(prob, OBSval) - s0(prob, 1-OBSval))) / denom
    
    return score0, score1

def r (reel, obs, cond):
    erreur = [0.0, 0.0]
    print("Verification obs/reel: ", np.array_equal(obs, reel))

    OBS = obs > cond
    OBSval = OBS.astype(int)
    
    REEL = reel > cond
    REELval = np.array(REEL.astype(int))

    print("Verification OBS/REEL: ", np.array_equal(OBS, REEL))

    # Nombre de fois où on oberve 0
    idx0 = np.where(OBSval == 0)[0]
    idx1 = np.where(OBSval == 1)[0]

    # Pour chaque fois ou reel = 0, combien on a prévu 1?
        # On va conter avec z0
    z0 = 0
    for idx in idx0:
        if REELval[idx] == 1:
            z0+=1
    if len(idx0) > 0:
        erreur[0] = z0/len(idx0)
    else:
        print("Pas de 0's dans le reel\n")

        # On va conter avec z1
    z1 = 0
    for idx in idx1:
        if REELval[idx] == 0:
            z1+=1

    print("z0, z1 = ", z0, z1)
    if len(idx1) > 0:
        erreur[1] = z1/len(idx1)
    else:
        print("Pas de 1's dans le reel\n")

    print("r0, r1 = ", erreur)
    return erreur, OBSval

def conv_obs (obs, mu, sigma_repre):
    obs_mod = np.array(obs.copy())
    sigma_mesure = np.maximum(0.2, 0.05*np.mean(obs))
    print("sigma_mesure.shape", sigma_mesure.shape)
    sigma = np.sqrt(sigma_mesure**2 + sigma_repre**2)


    # Paramètres pour la cut-off à 0
    a1 = (0 - mu) / sigma_repre
    a2 = (0 - mu) / sigma
    b = np.inf

    # Distribution de l'erreur 
    # dist1 = truncnorm(a1, b, loc=mu, scale=sigma_repre)
    print("mu, sigma =", mu, sigma)
    dist2 = truncnorm(a2, b, loc=mu, scale=sigma+5)
    samples = dist2.rvs(size=len(obs)) # Prend nVal valeurs aléatoires suivant dist
    moy_samples = np.mean(samples)
    var_samples = np.var(samples)
    # obs += samples - moy_samples
    obs_mod += samples 
    print("Verification obs: ", np.array_equal(obs, obs_mod))

    # return y, var_samples
    return obs_mod