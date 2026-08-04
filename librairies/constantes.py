##############
# Constantes #
##############

from datetime import datetime
from scipy import stats
from pathlib import Path

# Paramètres à ajuster
######################

DATA_ALL_BD = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/structure_bd/dict_all_bd.json"
DELTA = 40 # Delta du maillage en km
N_QUANTILES = 10 # Nombre de quantiles pour la séparation des données
FILTRE = False # True si on veut filtrer les données par pics, False sinon


# JSON
######

# Adresses aux données
DATA_23 = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/ad_all23/adresses_mac_min5.json"
DATA_24 = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/ad_all24/adresses_mac_min5.json"
DATA_06_25 = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/ad_juin25/adresses_mac_min5.json"
# DATA = "/home/solacavae/Documents/Thèse/GitHub/These_MF/ASNR/radon_stats/json/adresses.json"

# Adresses aux produits 
MAILLES = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/mailles")
STRUCTURE_BD = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/structure_bd")
YAYB = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/yAyB")
JSON = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json")    

# Adresses graphiques
GRAPH_10Q_3EVAL_FILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_10q/3eval/avec_filtre"
GRAPH_10Q_3EVAL_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_10q/3eval/sans_filtre"

GRAPH_10Q_NEVAL_FILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_10q/sans_eval/avec_filtre"
GRAPH_10Q_NEVAL_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_10q/sans_eval/sans_filtre"

GRAPH_20Q_3EVAL_FILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_20q/3eval/avec_filtre"
GRAPH_20Q_3EVAL_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_20q/3eval/sans_filtre"

GRAPH_20Q_NEVAL_FILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_20q/sans_eval/avec_filtre"
GRAPH_20Q_NEVAL_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/aprox_dist/yAyB_20q/sans_eval/sans_filtre"

# Adresses stats résultats
RESUT_10Q = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/docs/result_10q"
RESUT_20Q = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/docs/result_20q"

# Adresse graphiques régression
REG_10Q_FILTRE_MOY = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_10q/avec_filtre/mu"
REG_10Q_FILTRE_ECT = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_10q/avec_filtre/sigma"
REG_10Q_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_10q/sans_filtre"

REG_20Q_FILTRE_SQRT = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_20q/avec_filtre/sqrt_yA"
REG_20Q_FILTRE_LOG = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_20q/avec_filtre/log_yA"
REG_20Q_NFILTRE = "/Users/elena/Documents/These/Graphiques/analyse_radon/regression_params/regre_20q/sans_filtre"

# Data geopandas
NOM_CARTE = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/ne_110m_admin_0_countries.shp"
# NOM_CARTE = "/home/solacavae/Documents/Thèse/GitHub/These_MF/ASNR/radon_stats/ne_110m_admin_0_countries.shp"

# Data summary_all_peaks
NOM_SUMMARY = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/data/Summary_all_peaks.csv"

# Chemins généraux
BASE_DIR = Path(__file__).resolve().parent
# Dossier graphiques



###########
# ANALYSE #
###########

# Noms des colonnes du df
DATE = "date"
VALOBS = "Observed gamma dose rate (nSv/h)"
VALSIMU = "Simulated gamma dose rate (nSv/h)"
NOBS = 721
COORD_X = "latitude"
COORD_Y = "longitude"

# Seuil des pics
PIC = 10
TOL_OBS = 3
TOL_SIMU = 2

# Seuil distance
TOL_DIST = 5

# Types de graphiques
COURBE = "courbe"
HIST = "histogramme"
SCT = "scatter"
EVAL = "avec evaluation"
NEVAL = "sans evaluation"

# Paramètres graphiques
DEBUT = datetime(2026, 6, 1)
FIN = datetime(2026, 7, 1)
# Courbes
YMAX_C = 40
# Histogrammes
XMAX_H = 30
YMAX_H = 1000
BINS = 50
BINS_ALL_PEAKS = 20
# Titres
XLABEL_DIST = "Signal gamma observé (nSv/h)"
YLABEL_DIST = "Fréquence (%)"
XLABEL_ROC = "Taux de fausses alarmes (F)"
YLABEL_ROC = "Taux de hit rates (H(F))"

# Distributions possibles
DIST = {
    "norm": stats.norm,
    # "weibull_min": stats.weibull_min,
    # "weibull_max": stats.weibull_max,
    "gamma": stats.gamma,
    # "beta": stats.beta,
    "log-norm": stats.lognorm
}

# Distance entre 2 points
R = 6371 # Rayon de la terre

##########
# ERREUR #
##########
MIN_STAT = 5 # nombre minimum de stations dans une maille pour qu'elle soit considérée comme représentative
N_VALS = 3 # Une valeur par heure pendant un jour pour chaque yA

# Constantes pour les graphiques
XLIM = 100
YLIM = 100

N_DIST = 2 # Nombre de distributions pour le fitting multiple