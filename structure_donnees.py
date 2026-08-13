""" Ce fichier contient l'éxecution de la lecture et structure des données qu'on va utiliser.
Le but est d'écrire les données structurées dans un document pour pouvoir les réutiliser facilement 
dans les différentes étapes de l'analyse. 
Les données écrites sont filtrées, passées au bon format et organisées par station."""

import numpy as np

from librairies.constantes import *

from librairies.documents.fichiers import lecture_json, lecture_col, lecture_csv
from librairies.documents.docs import docs_dict_to_json_generique
from librairies.documents.ad_dependantes import loc_bd, loc_json_structure_bd

from librairies.exe_analyse.gamma_data import dict_simu_vs_obs, combiner_n_dicts

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

    def all_info(self, colonnes):
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

                # Valeurs : on lit chaque colonne indiquée dans `colonnes`
                valeurs = {
                    nom_val: lecture_col(adresse, nom_col)
                    for nom_val, nom_col in colonnes.items()
                }

                # On s'assure que tous les vecteurs sont comparables (même longueur / index valides)
                longueurs = {len(v) for v in valeurs.values()}
                if len(longueurs) > 1:
                    mask = np.logical_and.reduce(
                        [np.isfinite(v) for v in valeurs.values()]
                    )
                    valeurs = {nom_val: v[mask] for nom_val, v in valeurs.items()}

                self.dict_vals[ref] = valeurs

    def get_ad(self) -> dict:
        """ Transmet le dictionnaire organisant les adresses """
        return self.dict_adresses

    def get_coords(self) -> dict:
        """ Transmet le dictionnaire organisant les coordonnées """
        return self.dict_coords

    def get_vals(self) -> dict:
        """ Transmet le dictionnaire organisant les valeurs """
        return self.dict_vals
        

def structure_donnees () -> dict:
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
    ad_bd = loc_bd()
    ad_dict_bd = Path(ad_bd)

    # On extrait les données json
    data_bd = lecture_json(ad_dict_bd)

    dict_adresses = {}
    dict_vals = {} # Séparées par bd

    for i, (ref_bd, bd_info) in enumerate(data_bd.items()):

        bd = bd_info["path"]
        colonnes_bd = bd_info["colonnes"]

        # Initialisation de la classe
        structure_data = Structure(bd)

        # Organisation de l'information
        structure_data.all_info(colonnes_bd)

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
    ad_structure_bd = loc_json_structure_bd()

    ad_dict_ad = ad_structure_bd / "dict_adresses_all_bd.json"
    ad_dict_coords = ad_structure_bd / "dict_coords_all_bd.json"
    ad_dict_vals_diff_bd = ad_structure_bd / "dict_vals_diff_bd.json"
    ad_dict_vals_all_bd = ad_structure_bd / "dict_vals_all_bd.json"

    docs_dict_to_json_generique(dict_adresses, ad_dict_ad)
    docs_dict_to_json_generique(dict_coords_comm, ad_dict_coords)
    docs_dict_to_json_generique(dict_vals, ad_dict_vals_diff_bd)
    docs_dict_to_json_generique(dict_vals_all, ad_dict_vals_all_bd)

    # return dict_adresses, dict_coords_comm, dict_vals_all




