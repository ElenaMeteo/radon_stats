########
# Main #
########

"""Ce fichier contient le main du projet d'erreur de représentativité du 
radon qui fait l'étude des yB vs. yA et calcule l'erreur quadratique moyenne totale.
Il peut aussi tracer la grille de la France avec les stations de mesure et 
le graphique yA vs yB pour les mailles avec au moins 5 stations de mesure."""

from librairies.constantes import *
from librairies.maillage_et_stations.maille import maille_exe, dict_min5, dict_yA_yB, MSE_all, MSE
from librairies.documents.fichiers_erreur import lecture_json, coord_obt
from librairies.graphs.graphs_yA import graph_yA_yB, graph_maille_france

def main():
    """Execute main script."""
    # Données des stations de mesure
    data = lecture_json()
    coords, ad_all = coord_obt(data)
    
    maille = maille_exe(coords)

    # On filtre par stations pertinentes
    dict_maille = dict_min5(maille, coords, ad_all)

    # On détérmine les groupes yB et yA
    dict_yAyB = dict_yA_yB(dict_maille)
    
    # On dessine la maille de France avec les stations de mesure
    titre_maille = "Maille de France avec stations de mesure"
    graph_maille_france(maille, coords, titre_maille)

    # On fait le graphique yA vs yB
    titre_yA_yB = f"yA vs yB pour les mailles avec\n au moins {MIN_STAT} stations de mesure\n (delta={DELTA} km)"
    # graph_yA_yB(dict_yAyB, xlabel="yA", ylabel="yB", titre=titre_yA_yB)
    
    # Calcul de l'erreur quadratique moyenne totale
    mse = []
    for key, value in dict_yAyB.items():
        yA = value['yA']
        yB = value['yB']
        mse.append(MSE(yA, yB))            
    mse_total = MSE_all(mse)
    print(f"Erreur quadratique moyenne totale: {mse_total:.4f}")

if __name__ == "__main__":
    main()