""" Ce fichier contient la classe et les 
fonctions qui vons nous permettre de faire
les plots de nos distributions théoriques et
de nos données expérimentales."""

import numpy as np
import matplotlib.pyplot as plt

from ..constantes import *

class Graphs: 
    def __init__(self, dict_by_quantiles):
        self.dict_by_quantiles = dict_by_quantiles
        # Titres et labels pour les graphiques
        self.titre = "Comparaison du fitting des distributions simples et doubles"
        self.titre_simple_auto = "Fitting automatique simple"
        self.titre_simple_manuel = "Fitting manuel simple"
        self.titre_double = "Fitting double"
        self.xlabel = "Valeurs de yB"
        self.ylabel = "Densité"

    def graph_dist(self, titre, xlabel, ylabel):
        """ Trace un histogramme simple qui sert 
        de visualisation d'une distribution. """
        for quantile, info in self.dict_by_quantiles.items():
            yB = info['yB']
            if isinstance(yB, list):
                yB = np.concatenate([np.asarray(v) for v in yB if len(v) > 0]) if len(yB) > 0 else np.array([])
            else:
                yB = np.asarray(yB)

            yA_range = info['yA_range']
            q = quantile
            plt.figure()
            plt.hist(yB, bins=BINS, weights=np.ones_like(yB)/len(yB), color='orange')
            plt.title(f"yB pour yA_range={yA_range} ({q})")
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid()
            plt.show()