##############
# Graphiques #
##############

"""Ce document contient les fonctions qui genèrent 
des graphiques relatifs à la carte de la France"""

from ..constantes import *

import pandas as pd
import geopandas as gpd
import matplotlib as plt

def graph_maille_france(maille, coords, titre):
    """Dibuja la malla de Francia y las estaciones de medida en un mapa

    Args:
        maille (list): Lista de listas con los puntos de la malla. 
                      Cada punto es un tuple (latitude, longitude).
        coords (numpy.ndarray): Array de coordenadas de las estaciones. 
                               Shape (n_stations, 2) con [lat, lon].
        titre (str): Título del gráfico.
    
    Returns:
        None
    """
    plt.figure(figsize=(12, 10))
    
    # Dibujar la malla
    for i in range(len(maille)):
        for j in range(len(maille[0])):
            lat, lon = maille[i][j]
            plt.plot(lon, lat, 'b.', markersize=3)
            
            # Dibujar líneas de la malla
            if j < len(maille[0]) - 1:
                lat_next, lon_next = maille[i][j + 1]
                plt.plot([lon, lon_next], [lat, lat_next], 'b-', linewidth=0.5, alpha=0.5)
            
            if i < len(maille) - 1:
                lat_next, lon_next = maille[i + 1][j]
                plt.plot([lon, lon_next], [lat, lat_next], 'b-', linewidth=0.5, alpha=0.5)
    
    # Dibujar las estaciones de medida
    lats = coords[:, 0]
    lons = coords[:, 1]
    plt.scatter(lons, lats, color='red', s=50, marker='X', label='Estaciones de medida', zorder=5)
    
    # Configurar el gráfico
    plt.title(titre, fontsize=14)
    plt.xlabel('Longitud', fontsize=12)
    plt.ylabel('Latitud', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

def graph_carte(lat, lon, val, scores):
    """Donne une carte de la France avec
    les stations de mesure et montre la quantité
    de pics/evenements de chaque endroit"""
    
    # Format des données en DataFrame et GeoDataFrame
    data = pd.DataFrame({
        'lat':lat,
        'lon':lon,
        'val':val,
        'scores':scores
        })
    
    gdf = gpd.GeoDataFrame(
        data, 
        geometry=gpd.points_from_xy(data.lon, data.lat),
        crs = "EPSG:4326" # Code du format GPS lon lat
    )
    
    # Carte de France
    world = gpd.read_file(NOM_CARTE)
    france = world[world["NAME"] == "France"]
    
    # Plot
    fig, ax = plt.subplots(figsize=(8,8))
    france.plot(ax=ax, color="lightgrey")
    
    gdf.plot(
        ax=ax,
        # color="red",
        column='scores',
        cmap='rainbow',
        markersize=40,
        # markersize=gdf['val'],
        legend=True
    )
    
    # Limites continentales de la France
    xmin, xmax = -5.0, 10.0
    ymin, ymax = 41.0, 52.0
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    
    plt.show()