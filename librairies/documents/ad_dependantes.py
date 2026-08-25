""" Ce document contient les fonctions qui vont
attribuer la bonne adresse à chaque cas en fonction 
des paramètres établis """

from ..constantes import *


def loc_bd():
    """ Cette fonction va attribuer la bonne adresse
    à chaque base de données en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:
        ad_bd = DATA_EAU_ALT
    else:
        ad_bd = DATA_ALL_BD

    return ad_bd

def loc_json_structure_bd():
    """ Cette fonction va attribuer la bonne adresse
    à chaque json de structure_bd en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:
        ad_structure_bd = STRUCTURE_BD / "eau_alt"
    else:
        ad_structure_bd = STRUCTURE_BD / "all_bd"

    return ad_structure_bd

def loc_graphs_regression ():
    """ Cette fonction va attribuer la bonne adresse
    à chaque graphique de regression en fonction des
    paramètres établis """

    if N_QUANTILES==10:
        if FILTRE_PIC_RADON==True:
            ad_moy_ect = REG_FILTRE 
        else:
            ad_moy_ect = REG_NFILTRE 

    if N_QUANTILES==20:
        if FILTRE_PIC_RADON==True:
            ad_moy_ect = REG_FILTRE 
        else:
            ad_moy_ect = REG_NFILTRE 

    else:
        print("Erreur loc_graphs_regression: le nombre de quantiles n'est pas encore défini")

    return ad_moy_ect

def loc_graphs_fitting ():
    """ Cette fonction va attribuer la bonne adresse
    à chaque graphique de fitting en fonction des
    paramètres établis """

    if FILTRE_EAU_ALT==True:

        if FILTRE_PIC_RADON==True:
            ad_dist = GRAPH_NEVAL_FILTRE_EA
            ad_eval = GRAPH_3EVAL_FILTRE_EA
        else:
            ad_dist = GRAPH_NEVAL_NFILTRE_EA
            ad_eval = GRAPH_3EVAL_NFILTRE_EA

    else:

        if FILTRE_PIC_RADON==True:
            ad_dist = GRAPH_NEVAL_FILTRE
            ad_eval = GRAPH_3EVAL_FILTRE
        else:
            ad_dist = GRAPH_NEVAL_NFILTRE
            ad_eval = GRAPH_3EVAL_NFILTRE

    return ad_dist, ad_eval

def loc_res_mu_sigma ():

    if FILTRE_PIC_RADON == True:
        ad_resultats = JSON / "mu_sigma" / "avec_filtre"

    else:
        ad_resultats = JSON / "mu_sigma" / "sans_filtre"
    return ad_resultats


def loc_graph_reg_alpha_beta():

    if FILTRE_PIC_RADON == True:
        ad_reg = REG_ALPHA_BETA / "avec_filtre"

    else: 
        ad_reg = REG_ALPHA_BETA / "sans_filtre"

    return ad_reg
