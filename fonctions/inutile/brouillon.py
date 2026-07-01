# Adresses des documents
# AD_REF_620 = "/Users/elena/Documents/ASNR/codes/eval/analyse_radon/données/ARRAS_62_AGG_CP_gamma.csv"
# AD_REF_621 = "/Users/elena/Documents/ASNR/codes/eval/analyse_radon/données/ARDRES_62_AGG_CP_gamma.csv"
# AD_REF_622 = "/Users/elena/Documents/ASNR/codes/eval/analyse_radon/données/CALAIS_62_AGG_CP_gamma.csv"
# AD_REF_623 = "/Users/elena/Documents/ASNR/codes/eval/analyse_radon/données/LUMBRES_62_AGG_CP_gamma.csv"
# AD_REF_624 = "/Users/elena/Documents/ASNR/codes/eval/analyse_radon/données/MARQUISE_62_AGG_CP_gamma.csv"

# AD_REF_330 = "/home/solacavae/Documents/naTech/data/reference/prod/Timeseries/GammaDoseRate_sheets/BLAYE_33_AGG_CP_gamma.csv"
# AD_REF_331 = "/home/solacavae/Documents/naTech/data/reference/prod/Timeseries/GammaDoseRate_sheets/LACANAU_33_AGG_CP_gamma.csv"
# AD_REF_332 = "/home/solacavae/Documents/naTech/data/reference/prod/Timeseries/GammaDoseRate_sheets/BOURG-SUR-GIRONDE_33_AGG_CP_gamma.csv"
# AD_REF_333 = "/home/solacavae/Documents/naTech/data/reference/prod/Timeseries/GammaDoseRate_sheets/ST-LAURENT-MEDOC_33_AGG_CP_gamma.csv"

# # Noms des stations par ville
# VILLE_ARRAS = "ARRAS"
# VILLE_ARDRES = "ARDRES"
# VILLE_CALAIS = "CALAIS"
# VILLE_LUMBRES = "LUMBRES"
# VILLE_MARQUISE = "MARQUISE"

# VILLE_BLAYE = "BLAYE"
# VILLE_LACANAU = "LACANAU"
# VILLE_GIRONDE = "GIRONDE"
# VILLE_MEDOC = "MEDOC"

# # Départements étudiés
# DEP_33 = 33
# DEP_62 = 62

    # Titres pour les graphiques par ville
    ######################################
    # ad = [a for k, a in adresses.items() if k.startswith("AD_")]
    # ad = [a for k, a in globals().items() if k.startswith("AD_")]
    # villes = [v for k, v in globals().items() if k.startswith("VILLE_")]
    # dep = [v for k, v in globals().items() if k.startswith("DEP_")]
    
    # Observation gamma
    # titres_gamma = [f"Gamma observé à {v}" for v in (villes)]
    # titre_gamma = "Signal gamma en fonction du temps par ville"
    # xlabel_gamma = "Temps (j)"
    # ylabel_gamma = "Signal gamma observé (nSv/h)"
    
    # # Densité d'observation gamma par ville
    # titres_dist = [f"Distribution observations gamma à {v}" for v in (villes)]
    # titre_dist = "Distribution observations signal gamma par ville"

        # # Distributions par département
        # ###############################
        # deps = [v for k, v in globals().items() if k.startswith("DEP_")]
        # # Dep 33
        # dict_gamma_33 = dict_dep(dict_gamma, DEP_33)
        # gamma_all_33 = np.array(list(dict_gamma_33.values())).T.flatten()    
        # # Dep 62
        # dict_gamma_62 = dict_dep(dict_gamma, DEP_62)
        # gamma_all_62 = np.array(list(dict_gamma_62.values())).T.flatten()
        
        # gamma_dep = completer_vect(gamma_all_62)
        
        # # Graphiques
        # ############    
        # graph_multi(temps_all, gamma_all, titre_gamma, titres_gamma, xlabel_gamma, ylabel_gamma, 5, COURBE)
        # # graph_simple(temps, gamma, titre, xlabel, ylabel)
        
        # # pic_gamma(gamma_dep[:,0], DEP_33)   
        # pic_gamma(gamma_dep[:,0], DEP_62)   

# ESTIMATION PDF
# a = 0
# b = 30
# loc = 2.17
# scale = 1.64 * 0.7
# a_bis, b_bis = (a-loc)/scale, (b-loc)/scale
# print("a_bis", a_bis)
# print("b_bis", b_bis)
# print("loc", loc)
# print("scale", scale)

# val_dist_ref = dist.rvs(a, b, loc=loc, scale=scale, size=len(y), random_state=rng)
# plt.hist(val_dist_ref,bins=BINS, density=True, color='black', rwidth=0.5)
# bounds = [(a, a),  # a
#     (b, b),    # b
#     (loc, loc),  # loc libre
#     (scale, scale)   # scale positivo
# ]
# res = stats.fit(dist, y, bounds)
# res.plot()

# high = norm.pdf(abs, loc=loc, scale=scale)
# loc = (loc + arg_mode)/2
# coef = ect_adapte(loc, scale, arg_mode, val_mode)
# scale = scale*coef

# if nom == "norm":
#     loc, scale = params
#     pdf = best[dist].pdf(abs, loc=loc, scale=scale)
# else:
#     a, loc, scale = params
#     pdf = best[dist].pdf(abs, a, loc=loc, scale=scale)


# def roc(prev, obs):

#     prev = np.asarray(prev)
#     obs = np.asarray(obs)

#     seuil_obs_bin = (obs > PIC).astype(int)

#     refs = np.sort(prev)

#     n1 = np.sum(seuil_obs_bin) # Total vrais positifs
#     n0 = (1-seuil_obs_bin).sum() # Total vrais négatifs
    
#     h = []
#     f = []

#     for r in refs:
#         seuil_pred_bin = (prev >= r).astype(int)

#         tp = np.sum((seuil_pred_bin == 1) & (seuil_obs_bin == 1))
#         fp = np.sum((seuil_pred_bin == 1) & (seuil_obs_bin == 0))

#         h.append(tp / n1)
#         f.append(fp / n0)

#     return np.array(h), np.array(f)