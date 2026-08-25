"""Ce document contient les fonctions
qui vont évaluer nos données avec des scores"""

import numpy as np
from pathlib import Path

from ..constantes import *

def brier(prev, obs):
    """ - Brier Score: note notre efficacité"""
    
    fp = 0
    fn = 0

    seuil_prev = prev > PIC
    seuil_prev_bin = seuil_prev.astype(int) 

    seuil_obs = obs > PIC 
    seuil_obs_bin = seuil_obs.astype(int) 

    # tp = np.sum((seuil_prev_bin==1) & (seuil_obs_bin==1))
    # tn = np.sum((seuil_prev_bin==0) & (seuil_obs_bin==0))
    fp = np.sum((seuil_prev_bin==1) & (seuil_obs_bin==0))
    fn = np.sum((seuil_prev_bin==0) & (seuil_obs_bin==1))
    
    brier_score = np.sum((seuil_obs_bin-seuil_prev_bin)**2)/len(obs)

    return brier_score, fp, fn

# ---------------------------------------------------

def llog_pdf(pdf_vals: np.ndarray, eps: float = 1e-8) -> float:
    """ Vraisemblence a partir de valeurs de pdf déjà évalués."""
    return np.sum(np.log(pdf_vals + eps))

def llog(dist, params:np.ndarray, data, eps:float=1e-8) -> float:
    """ Vraisemblence à partir de la distribution et ses paramètres """
    pdf_vals = dist.pdf(data, *params)
    return np.sum(np.log(pdf_vals + eps))

def aic(ll, k) -> float:
    return 2*k - 2*ll

def bic(ll, k, n) -> float:
    return k*np.log(n) - 2*ll

# ---------------------------------------------------


def diff_best(best_aic, best_bic, diff_aic, diff_bic, resultats_methode):
    """
    resultats_methode =
    {
        "gamma": {...},
        "norm": {...},
        "lognorm": {...}
    }
    """
    for nom, res in resultats_methode.items():

        if best_aic != 0:
            diff_pct_aic = (res["aic"] - best_aic) / abs(best_aic) * 100
            diff_aic[nom].append(diff_pct_aic)

        if best_bic != 0:
            diff_pct_bic = (res["bic"] - best_bic) / abs(best_bic) * 100
            diff_bic[nom].append(diff_pct_bic)


def stats_scores_fittings(resultats, ruta_txt):

    methodes = ["simple_auto", "simple_manuel", "double"]

    recap = {}

    with open(ruta_txt, "w", encoding="utf-8") as f:

        f.write("STATISTIQUES DES FITTINGS\n")
        f.write("=" * 60 + "\n\n")

        for methode in methodes:

            compteur_aic = {nom: 0 for nom in DIST.keys()}
            compteur_bic = {nom: 0 for nom in DIST.keys()}

            diff_aic = {nom: [] for nom in DIST.keys()}
            diff_bic = {nom: [] for nom in DIST.keys()}

            # --- NUEVO: listas para guardar los valores brutos de AIC/BIC ---
            valeurs_aic = {nom: [] for nom in DIST.keys()}
            valeurs_bic = {nom: [] for nom in DIST.keys()}

            for quantile, res_quantile in resultats.items():

                res_methode = {
                    nom: res_quantile[nom][methode]
                    for nom in DIST.keys()
                }

                # --- NUEVO: acumular AIC/BIC de cada distribución en este cuantil ---
                for nom, res in res_methode.items():
                    valeurs_aic[nom].append(res["aic"])
                    valeurs_bic[nom].append(res["bic"])

                best_nom_aic = min(
                    res_methode,
                    key=lambda d: res_methode[d]["aic"]
                )

                best_nom_bic = min(
                    res_methode,
                    key=lambda d: res_methode[d]["bic"]
                )

                compteur_aic[best_nom_aic] += 1
                compteur_bic[best_nom_bic] += 1

                best_aic = res_methode[best_nom_aic]["aic"]
                best_bic = res_methode[best_nom_bic]["bic"]

                diff_best(
                    best_aic,
                    best_bic,
                    diff_aic,
                    diff_bic,
                    res_methode
                )

            recap[methode] = recap_stats_scores(
                compteur_aic,
                compteur_bic,
                diff_aic,
                diff_bic,
                valeurs_aic,      # <-- NUEVO
                valeurs_bic,      # <-- NUEVO
                f,
                methode
            )

    return recap


def recap_stats_scores(compteur_aic,
                        compteur_bic,
                        diff_aic,
                        diff_bic,
                        valeurs_aic,   # <-- NUEVO
                        valeurs_bic,   # <-- NUEVO
                        fichier,
                        methode):

    mean_diff_aic = {
        k: np.mean(v) if len(v) else np.nan
        for k, v in diff_aic.items()
    }

    mean_diff_bic = {
        k: np.mean(v) if len(v) else np.nan
        for k, v in diff_bic.items()
    }

    # --- NUEVO: media absoluta de AIC/BIC por distribución ---
    mean_aic = {
        k: np.mean(v) if len(v) else np.nan
        for k, v in valeurs_aic.items()
    }

    mean_bic = {
        k: np.mean(v) if len(v) else np.nan
        for k, v in valeurs_bic.items()
    }

    # -------- Affichage terminal --------

    print(f"\n========== {methode.upper()} ==========\n")

    print("Victoires AIC")
    print(compteur_aic)

    print("\nVictoires BIC")
    print(compteur_bic)

    print("\nMoyenne AIC")
    print(mean_aic)

    print("\nMoyenne BIC")
    print(mean_bic)

    print("\nDifférence moyenne (%) AIC")
    print(mean_diff_aic)

    print("\nDifférence moyenne (%) BIC")
    print(mean_diff_bic)

    # -------- Écriture fichier --------

    fichier.write(f"========== {methode.upper()} ==========\n\n")

    fichier.write("Victoires AIC\n")
    for dist, n in compteur_aic.items():
        fichier.write(f"    {dist:<12} : {n}\n")

    fichier.write("\nVictoires BIC\n")
    for dist, n in compteur_bic.items():
        fichier.write(f"    {dist:<12} : {n}\n")

    fichier.write("\nMoyenne AIC\n")
    for dist, val in mean_aic.items():
        fichier.write(f"    {dist:<12} : {val:.3f}\n")

    fichier.write("\nMoyenne BIC\n")
    for dist, val in mean_bic.items():
        fichier.write(f"    {dist:<12} : {val:.3f}\n")

    fichier.write("\nDifférence moyenne (%) AIC\n")
    for dist, val in mean_diff_aic.items():
        fichier.write(f"    {dist:<12} : {val:.3f}\n")

    fichier.write("\nDifférence moyenne (%) BIC\n")
    for dist, val in mean_diff_bic.items():
        fichier.write(f"    {dist:<12} : {val:.3f}\n")

    fichier.write("\n")
    fichier.write("-" * 60)
    fichier.write("\n\n")

    return {
        "wins_aic": compteur_aic,
        "wins_bic": compteur_bic,
        "mean_aic": mean_aic,          # <-- NUEVO
        "mean_bic": mean_bic,          # <-- NUEVO
        "mean_diff_aic": mean_diff_aic,
        "mean_diff_bic": mean_diff_bic,
    }

