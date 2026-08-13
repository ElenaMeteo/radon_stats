##############
# Constantes #
##############

from datetime import datetime
from scipy import stats
from pathlib import Path


# Paramètres à ajuster
######################

FILTRE_EAU_ALT = True # True si on veut filtrer les données par eau et altitude, False sinon
DELTA = 90 # Delta du maillage en km
N_QUANTILES = 10 # Nombre de quantiles pour la séparation des données
FILTRE_PIC_RADON = True # True si on veut filtrer les données par pics, False sinon

# DELTA_LIST = [30, 40, 50, 60, 70, 80, 90]
DELTA_LIST = [35, 45, 55, 65, 75, 85, 95]

# JSON
######

DATA_ALL_BD = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/structure_bd/dict_all_bd.json"
DATA_EAU_ALT = "/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/structure_bd/dict_eau_alt_bd.json"

# Adresses aux produits 
MAILLES = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/mailles")
STRUCTURE_BD = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/structure_bd")
YAYB = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json/yAyB")
JSON = Path("/Users/elena/Documents/These/GitHub/These_MF/radon_stats/json")    

# Adresses graphiques
# Toutes stations de mesure
GRAPH_3EVAL_FILTRE = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/all_data/yAyB_{N_QUANTILES}q/3eval/avec_filtre"
GRAPH_3EVAL_NFILTRE = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/all_data/yAyB_{N_QUANTILES}q/3eval/sans_filtre"

GRAPH_NEVAL_FILTRE = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/all_data/yAyB_{N_QUANTILES}q/sans_eval/avec_filtre"
GRAPH_NEVAL_NFILTRE = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/all_data/yAyB_{N_QUANTILES}q/sans_eval/sans_filtre"

# Filtre eau et altitude
GRAPH_3EVAL_FILTRE_EA = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/eau_alt/yAyB_{N_QUANTILES}q/3eval/avec_filtre"
GRAPH_3EVAL_NFILTRE_EA = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/eau_alt/yAyB_{N_QUANTILES}q/3eval/sans_filtre"

GRAPH_NEVAL_FILTRE_EA = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/eau_alt/yAyB_{N_QUANTILES}q/sans_eval/avec_filtre"
GRAPH_NEVAL_NFILTRE_EA = f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/aprox_dist/eau_alt/yAyB_{N_QUANTILES}q/sans_eval/sans_filtre"

# Adresses stats résultats
RESULTS_STATS = f"/Users/elena/Documents/These/GitHub/These_MF/radon_stats/docs/result_{N_QUANTILES}q"

# Adresse graphiques régression
REG_FILTRE = Path(f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/regression_params/regre_{N_QUANTILES}q/avec_filtre")
REG_NFILTRE = Path(f"/Users/elena/Documents/These/Graphiques/analyse_radon/delta_{DELTA}km/regression_params/regre_{N_QUANTILES}q/sans_filtre")

REG_ALPHA_BETA = Path("/Users/elena/Documents/These/Graphiques/analyse_radon/regression_alpha_beta")

# Adresses stats résultats
RESULTS_STATS = f"/Users/elena/Documents/These/GitHub/These_MF/radon_stats/docs/result_{N_QUANTILES}q"

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

# VALOBS = "Observed gamma dose rate (nSv/h)"
# VALSIMU = "Simulated gamma dose rate (nSv/h)"
# VALPRECIP_23 = "Precipitations (mm/h)"
# VALPRECIP_24 = "rain_val"

NOBS = 721

COORD_X = "latitude"
COORD_Y = "longitude"
EAU = "sea_coverage"
ALT = "altitude"

# Seuil des pics
PIC = 10
RAIN_MIN = 0.1
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

