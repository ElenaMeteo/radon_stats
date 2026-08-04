""" Ce document contient les fonctions
relatives à l'organisation du main."""

from pathlib import Path
import json

from librairies.documents.fichiers import lecture_json

def lecture_ou_calcul(adresse: Path, fonction_calcul: callable, element: str, force=False) -> dict:
    """ Cette fonction nous permet de choisir """

    # Si le n'exisite pas ou on force le calcul, on execute la fonction
    if not adresse.exists() or force:
        print(f"\nLe fichier {element} n'existe pas encore ou a été forcé.")
        fonction_calcul()
        print(f"Le fichier {element} a été créé avec succès.")

    dict = lecture_json(adresse)
    print(f"Le fichier {element} a été lu avec succès.")

    return dict
