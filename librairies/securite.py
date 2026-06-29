""" Ce fichier contient les fonctions qu'on va 
utiliser pour vérifier que les formats de nos objets
sont correctes et cohérents avec nos fonctions."""
#! WARNINGS

def secu_vect (vect, ref=None):
    """Sécurité vecteur vide: met un warning si le vecteur est vide"""
    if len(vect)==0:
        if ref != None: 
            print(f"Warning: le vecteur de {ref} est vide")
        else:
            print("Warning: le vecteur est vide")
    return