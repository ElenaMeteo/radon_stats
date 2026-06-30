"""Gráficos para análisis de vectores relacionados con delta."""

import numpy as np
import matplotlib.pyplot as plt

def plot_vector(values, xlabel='Índice', ylabel='Valor', title='Gráfico del vector', marker='o', color='blue', figsize=(10, 5)):
    """Dibuja un gráfico de línea a partir de un vector de valores.

    Args:
        values (iterable): Vector o lista de valores numéricos.
        xlabel (str): Etiqueta del eje x.
        ylabel (str): Etiqueta del eje y.
        title (str): Título del gráfico.
        marker (str): Símbolo de marcador para cada punto.
        color (str): Color de la línea y los marcadores.
        figsize (tuple): Tamaño de la figura (ancho, alto).

    Returns:
        matplotlib.figure.Figure: Figura generada.
        matplotlib.axes.Axes: Ejes del gráfico.
    """
    values = [2.7719, 1.7384, 1.5907, 1.6199, 1.5388, 1.6077, 1.5522, 1.7179, 1.7266, 1.8285, 1.6561]
    x = [20, 30, 40, 45, 50, 55, 60, 70, 80, 90, 100]
    y = np.asarray(values)

    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(x, y, marker=marker, color=color, linestyle='-')
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()
    plt.show()

    return fig, ax

values = []
plot_vector(values, xlabel='Delta (km)', ylabel='MSE moyen', title='MSE vs Delta')
