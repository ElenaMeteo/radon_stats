""" Ce fichier contient l'éxecution de la lecture et structure des données qu'on va utiliser.
Le but est d'écrire les données structurées dans un document pour pouvoir les réutiliser facilement 
dans les différentes étapes de l'analyse. 
Les données écrites sont filtrées, passées au bon format et organisées par station."""

import numpy as np
import json

from librairies.constantes import *

from librairies.documents.fichiers import lecture_json, lecture_col, lecture_csv
from librairies.documents.docs import docs_dict_to_json_generique

from librairies.exe_analyse.gamma_data import dict_simu_vs_obs, combiner_n_dicts

dossier = Path(__file__).parent.parent
dossier_json = dossier / "json"

class Structure:
    def __init__(self, ad_data):
        self.ad_data = ad_data
        self.data = None
        self.dict_adresses = {}
        self.dict_coords = {}
        self.dict_vals = {}

    def _lecture_data(self):
        self.data = lecture_json(self.ad_data)

    def _coords(self, adresse):
        """Lit les coordonnées des 
        stations de mesure afin de les
        mettre sur la carte."""

        # Lecture du fichier entier
        data = lecture_csv(adresse)

        # Recherche des colonnes selon nos intérêts
        lat = data[COORD_X].iloc[0]
        lon = data[COORD_Y].iloc[0]
        
        return lat, lon

    def all_info(self):
        """ Actualise les dictionnaires d'informations
        relatives aux adresses, coordonnées et
         valeurs (simu/obs) avec ses valeurs correspondentes.

        On fait 3 dictionnaires plutot que 1 parce qu'on veut 
        rassambler les valeurs de plusieurs bases de donées
        """
        self._lecture_data()

        for bloc in self.data["adresses"]:
            for ref, adresse in bloc.items():
                if ref == "dep":
                    continue

                # Adresses
                self.dict_adresses[ref] = adresse 

                # Coordonnées
                lat, lon = self._coords(adresse)
                self.dict_coords[ref] = [lat, lon]

                # Valeurs
                obs = lecture_col(adresse, VALOBS)
                simu = lecture_col(adresse, VALSIMU)
                # On va comparer les vecteurs, donc il faut qu'ils aient du sens
                if (len(simu) != len(obs)):
                    mask = np.isfinite(obs) & np.isfinite(simu)
                    obs = obs[mask]
                    simu = simu[mask]

                self.dict_vals[ref] = [simu, obs]
   
    def get_ad(self) -> dict:
        """ Transmet le dictionnaire organisant les adresses """
        return self.dict_adresses

    def get_coords(self) -> dict:
        """ Transmet le dictionnaire organisant les coordonnées """
        return self.dict_coords

    def get_vals(self) -> dict:
        """ Transmet le dictionnaire organisant les valeurs """
        return self.dict_vals
        

def structure_donnees (ad_dict_bd:str) -> dict:
    """ Utilise la classe structure pour structurer les donnees
    de façon à que ce soit unifié. 

    Il y a 3 dictionnaires résultants:

    adresses:
    --------
    dict_adresses = {
        bd1: {
            ref1: adresse1,
            ref2: adresse2,
            ...
            refN: adresseN
        }
        bd2: {
            ref1: adresse1,
            ref2: adresse2,
            ...
            refN: adresseN
        }
    }

    coordonnées: (supposant les mêmes stats pour toutes les bd)
    -----------
    dict_coords = {
        ref1: coords1,
        ref2: coords2,
        ...
        refN: coordsN
    }

    valeurs:
    -------
    dict_vals_all = {
        ref1: vals1 (all bd),
        ref2: vals2 (all bd),
        ...
        refN: valsN (all bd)
    }
    """
    # On extrait les données json
    data_bd = lecture_json(ad_dict_bd)

    dict_adresses = {}
    dict_vals = {} # Séparées par bd


    for i, (ref_bd, ad_bd) in enumerate(data_bd.items()):

        # Initialisation de la classe
        structure_data = Structure(ad_bd)

        # Organisation de l'information
        structure_data.all_info()

        # Réception des adresses
        dict_adresses[ref_bd] = structure_data.get_ad()

        # Réception des coordonnées (mêmes pour toutes les bd)
        if (i==0):
            dict_coords = structure_data.get_coords()

        # Réception des valeurs
        dict_vals[ref_bd] = structure_data.get_vals()

    # On garde seulement les références communes 
    common_keys = set.intersection(*[set(d.keys()) for d in dict_vals.values()])

    dict_coords_comm = {k: dict_coords[k] for k in common_keys}

    dict_vals_comm = { # Filtré par refs communes
        ref_bd: {k: vals[k] for k in common_keys}
        for ref_bd, vals in dict_vals.items()
    }

    # Combinaison des dictionnaires de données en 1
    dict_vals_all = combiner_n_dicts(*dict_vals_comm.values())

    # Écriture des dictionnaires dans des archives json
    ad_dict_ad = dossier_json / "structure_bd" / "dict_adresses_all_bd.json"
    ad_dict_coords = dossier_json / "structure_bd" / "dict_coords_all_bd.json"
    ad_dict_vals_diff_bd = dossier_json / "structure_bd" / "dict_vals_diff_bd.json"
    ad_dict_vals_all_bd = dossier_json / "structure_bd" / "dict_vals_all_bd.json"

    docs_dict_to_json_generique(dict_adresses, ad_dict_ad)
    docs_dict_to_json_generique(dict_coords_comm, ad_dict_coords)
    docs_dict_to_json_generique(dict_vals, ad_dict_vals_diff_bd)
    docs_dict_to_json_generique(dict_vals_comm, ad_dict_vals_all_bd)

    return dict_adresses, dict_coords_comm, dict_vals_all




# def main():
#     """Execute main script"""
    
#     # Structure des données
#     #######################

#     # Lecture des documents json (adresses) 
#     data23 = lecture_json(NOM_DATA_23)
#     data24 = lecture_json(NOM_DATA_24)
#     print("Fin lecture des documents json")

#     # Dictionnaires qui contiennent les données par station
#     dict23 = dict_simu_vs_obs(data23)
#     dict24 = dict_simu_vs_obs(data24)
#     print("Fin de la création des dictionnaires des données par station")

#     # On garde seulement les references communes 
#     common_keys = set(dict23.keys()) & set(dict24.keys())
#     dict23 = {k: dict23[k] for k in common_keys}
#     dict24 = {k: dict24[k] for k in common_keys}
#     print("Fin de la filtration par références communes")

#     # Concatenation des années (pas besoin de faire la différence)
#     dict_all = combiner_dicts(dict23, dict24)
#     print("Fin de la concatenation des années")
    
#     # Enregistrement des données structurées
#     ad_json = dossier_json / "dict_23_24.json"
#     docs_dict_to_json(dict_all, ad_json)


