""" Ce fichier contient les fonctions qui trouvent et 
gèrent les paramètres relatifs à la distribution choisie
(distribution gamma dans notre cas). """

import numpy as np
from ..constantes import *
from scipy.stats import gamma

def parms_k_theta(mu, sigma):
    """ Calcule les paramètres k et theta 
    de la distribution gamma à partir de la 
    moyenne (mu) et de l'écart-type (sigma). """

    k = (mu/sigma)**2
    theta = sigma**2/mu

    return k, theta

def parms_mu_sigma(k, theta):
    """ Calcule les paramètres mu et sigma 
    de la distribution gamma à partir de la 
    moyenne (mu) et de l'écart-type (sigma). """
    
    mu = k * theta
    sigma = np.sqrt(k) * theta

    return mu, sigma

def gamma_mod(k, theta, y):
    """ Calcule la valeur de la fonction de densité de probabilité 
    de la distribution gamma pour les paramètres k et theta à un point y donné. """

    if y < 0:
        return 0  # La distribution gamma n'est définie que pour y >= 0
    else:
        return gamma.pdf(y/theta, a=k, scale=theta)
    
def mu_yA(alpha0, alpha1, yA):
    """ Calcule la moyenne µ de la distribution gamma à partir des 
    paramètres alpha0 et alpha1 et d'une valeur yA. """

    return alpha0 + alpha1 * yA

def sigma_yA(beta0, beta1, yA):
    """ Calcule l'écart-type sigma de la distribution gamma à partir des 
    paramètres beta0 et beta1 et d'une valeur yA. """

    return beta0 + beta1 * yA
    