"""OBSOLET"""

"""Ce fichier contient les fonctions qui vont
nous aider à trouver la meilleure approximation
de distribution pour nos données."""

import math
from scipy.special import lambertw

def ect_adapte(loc, scale_base, arg_mode, val_mode):
    """Trouve le coefficient par lequel on 
    multiplie scale afin d'arriver à la distribution
    qui nous concerne.
    
    Pour cela on doit utiliser la fonction W
    de Lambert."""
    
    aux = - math.log(2*math.pi*val_mode) - (arg_mode - loc)
    w_aux = lambertw(aux)
    print("w_aux:", w_aux)
    scale = math.exp(0.5 * w_aux)
    print("scale:", scale)
    coef = scale/scale_base
    print("coef:", coef)

    return coef



