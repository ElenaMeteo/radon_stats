""" Ce fichier contient les classes et fonctions nécessaires 
pour pouvoir réaliser la régression sur les paramètres alpha 
et beta en fonction de la liste de deltas """

from librairies.constantes import *

from librairies.eval.mu_sigma import plot_regression, plot_regression_poly2
from librairies.documents.fichiers import lecture_json
from librairies.documents. ad_dependantes import loc_res_mu_sigma, loc_graph_reg_alpha_beta


def main ():

    # Paramètres de mu
    a_mu = []
    b_mu = []

    # Paramètres de sigma
    a_sigma= []
    b_sigma = []
    c_sigma = []

    for delta in DELTA_LIST:
        # Lire dictionnaire
        ad_dict_params = loc_res_mu_sigma()
        ad_dict_params = ad_dict_params/ f"mu_sigma_delta{delta}km_{N_QUANTILES}q.json"
        dict_params = lecture_json(ad_dict_params)

        # Classifier en vecteurs par paramètre
        a_mu.append(dict_params["mu"]["a"])
        b_mu.append(dict_params["mu"]["b"])

        a_sigma.append(dict_params["sigma"]["a"])
        b_sigma.append(dict_params["sigma"]["b"])
        c_sigma.append(dict_params["sigma"]["c"])

    xlabel = "delta"
    ylabel_a_mu = "a_mu"
    ylabel_b_mu = "b_mu"
    ylabel_a_sigma = "a_sigma"
    ylabel_b_sigma = "b_sigma"
    ylabel_c_sigma = "c_sigma"

    titre = "Regression paramètres alpha et beta\n en fonction de delta"

    # Régression a_mu
    ad_reg_alpha_beta = loc_graph_reg_alpha_beta()
    nom_doc = "regression_a_mu"
    plot_regression(DELTA_LIST, 
                    a_mu, 
                    xlabel,
                    ylabel_a_mu, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression b_mu
    nom_doc = "regression_b_mu"
    plot_regression(DELTA_LIST, 
                    b_mu, 
                    xlabel,
                    ylabel_b_mu, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)
    
    # Régression a_sigma
    nom_doc = "regression_a_sigma"
    plot_regression(DELTA_LIST, 
                    a_sigma, 
                    xlabel,
                    ylabel_a_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression b_sigma
    nom_doc = "regression_b_sigma"
    plot_regression(DELTA_LIST, 
                    b_sigma, 
                    xlabel,
                    ylabel_b_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression c_sigma
    nom_doc = "regression_c_sigma"
    plot_regression(DELTA_LIST, 
                    c_sigma, 
                    xlabel,
                    ylabel_c_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression a_mu
    ad_reg_alpha_beta = loc_graph_reg_alpha_beta()
    nom_doc = "regression_a_mu2"
    plot_regression_poly2(DELTA_LIST, 
                    a_mu, 
                    xlabel,
                    ylabel_a_mu, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression b_mu
    nom_doc = "regression_b_mu2"
    plot_regression_poly2(DELTA_LIST, 
                    b_mu, 
                    xlabel,
                    ylabel_b_mu, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)
    
    # Régression a_sigma
    nom_doc = "regression_a_sigma2"
    plot_regression_poly2(DELTA_LIST, 
                    a_sigma, 
                    xlabel,
                    ylabel_a_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression b_sigma
    nom_doc = "regression_b_sigma2"
    plot_regression_poly2(DELTA_LIST, 
                    b_sigma, 
                    xlabel,
                    ylabel_b_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)

    # Régression c_sigma
    nom_doc = "regression_c_sigma2"
    plot_regression_poly2(DELTA_LIST, 
                    c_sigma, 
                    xlabel,
                    ylabel_c_sigma, 
                    titre,  
                    ad_reg_alpha_beta,
                    nom_doc)
    

if __name__ == "__main__":
    main()