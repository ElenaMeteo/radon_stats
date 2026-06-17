############################
### Fonctions Graphiques ###
############################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, truncnorm, gamma

from These_MF.exercice_vent.Python.Variables import *

" En voyant le nombre de fois où nous allons repeter les mêmes  "
" lignes de code, on va faire des fonctions principales pour    "
" l'écriture de graphiques afin de mieux ranger notre code      "

    
def graphic_plt_id (dictionnaire, nPer, nVar, pc, PC, titre, titre_variable, xlabel, ylabel, SCT, savepath):
    DEUX=False
    nFig, axs = plt.subplots(nPer, nVar, figsize=(20,14))
    axs = np.atleast_2d(axs)
    
    nFig.suptitle(titre, fontsize=16)
    titres = list(dictionnaire.keys())
    matrices = list(dictionnaire.values())

    for i, mat in enumerate(matrices):
        row = (i) % nPer
        col = int(i/nPer)

        vect0 = mat[:,0]
        vect1 = mat[:,1]
        
        if mat.shape[1] > 2:
            vect2 = mat[:,2]
            vect3 = mat[:,3]
        # Cela voudrait dire qu'on veut plus d'une courbe dans chaque graphique
        axs[row,col].plot(vect0, vect0, label="identité", color='blue', linewidth=3.5)
        if SCT == True:
            axs[row,col].scatter(vect0, vect1, label=titre_variable, color='red')
            if mat.shape[1] > 2:
                axs[row,col].scatter(vect2, vect3, label="avec erreur obs", color='gray')
        else:
            axs[row,col].plot(vect0, vect1, label=titre_variable, color='red', linewidth=3.5)
            if mat.shape[1] > 2:
                axs[row,col].plot(vect2, vect3, label="sans erreur obs", color='gray', linewidth=3.5)
        if PC == True:
            axs[row,col].plot(vect0, np.full((len(mat),), pc[i]), label="pC", color='green', linewidth=2.5)
        axs[row,col].set_title(titres[i])
        axs[row,col].set_xlabel(xlabel, fontsize=20)
        axs[row,col].set_ylabel(ylabel, fontsize=20)
        axs[row,col].legend(
            fontsize=16,        # tamaño del texto
            title_fontsize=20,  # si usas título en la leyenda
            frameon=False) 
        axs[row,col].grid(False)

        # for spine in axs.spines.values():
        #     spine.set_linewidth(2)

        # # Ticks (marques + chiffres)
        # axs.tick_params(
        #     axis="both",
        #     which="both",
        #     width=2,
        #     length=7,
        #     labelsize=12
        # )

        # # Fond transparent
        # nFig.patch.set_alpha(0)
        # for ax in axs.flat:
        #     ax.patch.set_alpha(0)
        
        if savepath is not None:
            nFig.savefig(
                savepath,
                dpi=300,
                bbox_inches="tight",
                transparent=True
            )

    plt.tight_layout()
    plt.show()


def graphic_bar (dictionnaire, nPer, nVar, titre, titre_variable, xlabel, ylabel):
    """_summary_

    Args:
        dictionnaire (_type_): _description_
        nPer (_type_): _description_
        nVar (_type_): _description_
        titre (_type_): _description_
        titre_variable (_type_): _description_
        xlabel (_type_): _description_
        ylabel (_type_): _description_
    """
    nFig, axs = plt.subplots(nPer, nVar, figsize=(20,14))
    axs = np.atleast_2d(axs)

    nFig.suptitle(titre, fontsize=16)
    titres = list(dictionnaire.keys())
    matrices = list(dictionnaire.values())

    for i, (mat) in enumerate(matrices):
        row = (i) % nPer
        col = int(i/nPer)

        vect1 = mat[:,0]
        vect2 = mat[:,1]

        axs[row,col].bar(vect1, vect2, label=titre_variable)
        axs[row,col].set_title(titres[i])
        axs[row,col].set_xlabel(xlabel)
        axs[row,col].set_ylabel(ylabel)
        axs[row,col].legend() 
        axs[row,col].grid(True)

    plt.tight_layout()
    plt.show()

# Fonction pour tracer des distributions

def graphic_pdf_cdf (dictionnaire, nPer, nVar, titre, titre_variable, xlabel, ylabel, CDF):

    nFig, axs = plt.subplots(nPer, nVar)
    axs = np.atleast_2d(axs)

    nFig.suptitle(titre, fontsize=16)
    titres = list(dictionnaire.keys())
    series = list(dictionnaire.values())

    for i, ser in enumerate(series):
        if nPer == 1:
            row = 0
            col = i
        else:
            row = (i) % nPer
            col = int(i/nPer)
    
        if CDF==True:
            n = len(ser)
            valeurs_cdf = np.sort(ser)
            cdf = np.arange(1, n+1) / n
            axs[row, col].plot(valeurs_cdf, cdf, label=titre_variable, color='red')

        else:
            axs[row,col].hist(ser,
                bins=50,
                density=True,
                alpha=0.7,
                color='red',
                label=titre_variable
            )
        axs[row,col].set_title(titres[i])
        axs[row,col].set_xlabel(xlabel)
        axs[row,col].set_ylabel(ylabel)
        axs[row,col].legend() 
        axs[row,col].grid(True)

    plt.tight_layout()
    plt.show()


def graph_simple(x, y, titre_variable, xlabel, ylabel):
    plt.figure()
    plt.plot(x, y, '-', color='blue')
    plt.plot(x, y, 'x', color='black')

    plt.title(titre_variable)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True)

    plt.show()
