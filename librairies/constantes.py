##############
# Constantes #
##############

from datetime import datetime
from scipy import stats
from pathlib import Path

# Data json
NOM_DATA_23 = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/json/ad_all23/adresses_mac.json"
NOM_DATA_24 = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/json/ad_all24/adresses_mac.json"
NOM_DATA_2324 = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/json/dict_23_24.json"
NOM_DATA_06_25 = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/json/ad_juin25/adresses_mac_min5.json"
# NOM_DATA = "/home/solacavae/Documents/Thèse/GitHub/These_MF/ASNR/analyse_radon/json/adresses.json"
AD_DATA_JSON = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/json"

# Data geopandas
NOM_CARTE = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/ne_110m_admin_0_countries.shp"
# NOM_CARTE = "/home/solacavae/Documents/Thèse/GitHub/These_MF/ASNR/analyse_radon/ne_110m_admin_0_countries.shp"

# Data summary_all_peaks
NOM_SUMMARY = "/Users/elena/Documents/These/GitHub/These_MF/analyse_radon/data/Summary_all_peaks.csv"

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
    "weibull_min": stats.weibull_min,
    # "weibull_max": stats.weibull_max,
    # "gamma": stats.gamma,
    # "beta": stats.beta,
    "log-norm": stats.lognorm
}

# Distance entre 2 points
R = 6371 # Rayon de la terre

##########
# ERREUR #
##########

DELTA = 40 # delta du maillage en km
MIN_STAT = 5 # nombre minimum de stations dans une maille pour qu'elle soit considérée comme représentative
N_VALS = 3 # Une valeur par heure pendant un jour pour chaque yA

# Constantes pour les graphiques
XLIM = 100
YLIM = 100

N_QUANTILES = 20 # Nombre de quantiles pour la séparation des données
N_DIST = 2 # Nombre de distributions pour le fitting multiple