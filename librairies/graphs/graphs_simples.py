##############
# Graphiques #
##############

""" Ce fichier contient les fonctions qui tracent
des graphiques très simples"""

import matplotlib as plt
import numpy as np

def graph_vecteur(values, xlabel='Index', ylabel='Valor', titre='Serie de valores', marker='o', color='blue', figsize=(10, 5)):
    """Dibuja un gráfico de línea simple a partir de un vector de valores.

    Args:
        values (iterable): Vector o lista de valores numéricos.
        xlabel (str): Etiqueta del eje x.
        ylabel (str): Etiqueta del eje y.
        titre (str): Título del gráfico.
        marker (str): Símbolo de marcador para cada punto.
        color (str): Color de la línea.
        figsize (tuple): Tamaño de la figura (ancho, alto).

    Returns:
        None
    """
    valores = np.asarray(values)
    plt.figure(figsize=figsize)
    plt.plot(valores, marker=marker, color=color)
    plt.title(titre)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
