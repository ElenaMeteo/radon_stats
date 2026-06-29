""" Ce fichier contient l'éxecution de la lecture et structure des données qu'on va utiliser.
Le but est d'écrire les données structurées dans un document pour pouvoir les réutiliser facilement 
dans les différentes étapes de l'analyse. 
Les données écrites sont filtrées, passées au bon format et organisées par station."""

from librairies.constantes import *

from librairies.documents.fichiers import lecture_json
from librairies.documents.docs import docs_dict_to_json

from librairies.exe_analyse.gamma_data import dict_simu_vs_obs, combiner_dicts

dossier = Path(__file__).parent
dossier_json = dossier / "json"

def main():
    """Execute main script"""
    
    # Structure des données
    #######################

    # Lecture des documents json (adresses) 
    data23 = lecture_json(NOM_DATA_23)
    data24 = lecture_json(NOM_DATA_24)
    print("Fin lecture des documents json")

    # Dictionnaires qui contiennent les données par station
    dict23 = dict_simu_vs_obs(data23)
    dict24 = dict_simu_vs_obs(data24)
    print("Fin de la création des dictionnaires des données par station")

    # On garde seulement les references communes 
    common_keys = set(dict23.keys()) & set(dict24.keys())
    dict23 = {k: dict23[k] for k in common_keys}
    dict24 = {k: dict24[k] for k in common_keys}
    print("Fin de la filtration par références communes")

    # Concatenation des années (pas besoin de faire la différence)
    dict_all = combiner_dicts(dict23, dict24)
    print("Fin de la concatenation des années")
    
    # Enregistrement des données structurées
    ad_json = dossier_json / "dict_23_24.json"
    docs_dict_to_json(dict_all, ad_json)

if __name__ == "__main__":
    main()