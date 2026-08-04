""" Ce document contient les fonctions qui vont
attribuer la bonne adresse à chaque cas en fonction 
des paramètres établis """

from ..constantes import *

def loc_bd():
    """ Cette fonction va attribuer la bonne adresse
    à chaque base de données en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:
        AD_BD = DATA_EAU_ALT
    else:
        AD_BD = DATA_ALL_BD

    return AD_BD

def loc_json_structure_bd():
    """ Cette fonction va attribuer la bonne adresse
    à chaque json de structure_bd en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:
        AD_STRUCTURE_BD = STRUCTURE_BD / "eau_alt"
    else:
        AD_STRUCTURE_BD = STRUCTURE_BD / "all_bd"

    return AD_STRUCTURE_BD

def loc_graphs_regression ():
    """ Cette fonction va attribuer la bonne adresse
    à chaque graphique de regression en fonction des
    paramètres établis """

    if N_QUANTILES==10:
        if FILTRE_PIC_RADON==True:
            AD_MOY = REG_10Q_FILTRE_MOY
            AD_ECT = REG_10Q_FILTRE_ECT
        else:
            AD_MOY = REG_10Q_NFILTRE_MOY
            AD_ECT = REG_10Q_NFILTRE_ECT
    if N_QUANTILES==20:
        if FILTRE_PIC_RADON==True:
            AD_MOY = REG_20Q_FILTRE_MOY
            AD_ECT = REG_20Q_FILTRE_ECT
        else:
            AD_MOY = REG_20Q_NFILTRE_MOY
            AD_ECT = REG_20Q_NFILTRE_ECT

    else:
        print("Erreur loc_graphs_regression: le nombre de quantiles n'est pas encore défini")

    return AD_MOY, AD_ECT

def loc_graphs_fitting ():
    """ Cette fonction va attribuer la bonne adresse
    à chaque graphique de fitting en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:

        if N_QUANTILES==10:
            if FILTRE_PIC_RADON==True:
                AD_DIST = GRAPH_10Q_NEVAL_FILTRE_EA
                AD_EVAL = GRAPH_10Q_3EVAL_FILTRE_EA
            else:
                AD_DIST = GRAPH_10Q_NEVAL_NFILTRE_EA
                AD_EVAL = GRAPH_10Q_3EVAL_NFILTRE_EA

        if N_QUANTILES==20:
            if FILTRE_PIC_RADON==True:
                AD_DIST = GRAPH_20Q_NEVAL_FILTRE_EA
                AD_EVAL = GRAPH_20Q_3EVAL_FILTRE_EA
            else:
                AD_DIST = GRAPH_20Q_NEVAL_NFILTRE_EA
                AD_EVAL = GRAPH_20Q_3EVAL_NFILTRE_EA

        else:
            print("Erreur loc_graphs_fitting: le nombre de quantiles n'est pas encore défini")

    else:

        if N_QUANTILES==10:
            if FILTRE_PIC_RADON==True:
                AD_DIST = GRAPH_10Q_NEVAL_FILTRE
                AD_EVAL = GRAPH_10Q_3EVAL_FILTRE
            else:
                AD_DIST = GRAPH_10Q_NEVAL_NFILTRE
                AD_EVAL = GRAPH_10Q_3EVAL_NFILTRE

        if N_QUANTILES==20:
            if FILTRE_PIC_RADON==True:
                AD_DIST = GRAPH_20Q_NEVAL_FILTRE
                AD_EVAL = GRAPH_20Q_3EVAL_FILTRE
            else:
                AD_DIST = GRAPH_20Q_NEVAL_NFILTRE
                AD_EVAL = GRAPH_20Q_3EVAL_NFILTRE

        else:
            print("Erreur loc_graphs_fitting: le nombre de quantiles n'est pas encore défini")

    return AD_DIST, AD_EVAL