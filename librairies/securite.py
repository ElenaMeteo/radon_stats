""" Ce fichier contient les fonctions qu'on va 
utiliser pour vérifier que les formats de nos objets
sont correctes et cohérents avec nos fonctions."""
#! WARNINGS

import numpy as np

def check_vecteur_vide (v, ref=None):
    """Sécurité vecteur yB: met un warning si le vecteur est vide ou contient des NaN"""
    if len(v)==0:
        if ref != None: 
            print(f"Warning: le vecteur {ref} est vide")
        else:
            print("Warning: le vecteur est vide")
        raise ValueError("Le vecteur est vide. Vérifiez vos données.")
    return

def check_vecteur_nan (v, ref=None):
    """Sécurité vecteur yB: met un warning si le vecteur contient des NaN"""
    if any(np.isnan(v)):
        if ref != None: 
            print(f"Warning: le vecteur {ref} contient des NaN")
        else:
            print("Warning: le vecteur est vide")
        raise ValueError("Le vecteur contient des NaN. Vérifiez vos données.")
    return