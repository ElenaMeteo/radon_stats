############
# Stations #
############

"""Ce fichier contient les fonctions qui gèrent les 
stations d'une zone donnée"""

from librairies.documents.fichiers_erreur import coord

def cont_stat(p1, p2, p3, p4, dict_coords):
    """
    Compte le nombre de stations dans une zone définie par les points p1, p2, p3 et p4.

    Args:
        p1, p2, p3, p4: points définissant les coins de la zone (sous forme de tuples (x, y)).
        dict_coords (dict): dictionnaire {ref: [lat, lon]} des stations à vérifier.

    Retourne:
        int (cont): Nombre de stations à l'intérieur de la zone.
        list (stat_dans_zone): Liste des coordonnées des stations dans la zone.
        list (ad_stat_zone): Liste des références (ref) des stations dans la zone.
    """
    polygone = [p1, p2, p3, p4]
    stat_dans_zone = []
    ad_stat_zone = []
    cont = 0

    for ref, point in dict_coords.items():
        if point_dans_polygone(point, polygone):
            cont += 1
            stat_dans_zone.append(point)
            ad_stat_zone.append(ref)

    return cont, stat_dans_zone, ad_stat_zone

def point_dans_polygone(point, polygone):
    """
    Vérifie si un point est à l'intérieur d'un polygone défini par une liste de points
    avec la méthode du ray-casting.  
    Args:        point: Tuple (x, y) représentant le point à vérifier.
                 polygone: Liste de tuples (x, y) représentant les coins du polygone.
    Retourne:    bool: True si le point est à l'intérieur du polygone, False sinon.
    """ 
    x, y = point
    n = len(polygone)

    # Variable qui va nous dire si le point est à l'intérieur ou à l'extérieur du polygone
    interieur = False
    p1x, p1y = polygone[0]

    for i in range(1, n + 1):
        p2x, p2y = polygone[i % n] # Permet de boucler sur les points du polygone

        # Vérifie si la demie-droite horizontale peut traverser le segment défini par p1 et p2
        if y >= min(p1y, p2y): 
            if y <= max(p1y, p2y):

                # Vérifie si le point est à gauche du segment 
                # (puisque la demie-droite part du point vers la droite) 
                if x <= max(p1x, p2x):

                    # Parce que si le segment est horizontal, il n'y a pas d'intersection
                    # print("cond 4: p1y, p2y:", p1y, p2y)
                    if p1y != p2y:
                        # Calcul de l'intersection du segment avec la ligne horizontale passant par le point
                        # Correspond à la formule de l'intersection d'une droite avec une ligne horizontale
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x

                        # On fait seulement compter les intersections à droite du point
                        if x < xinters:
                            interieur = not interieur

                        # Si le point est sur le segment, on considère qu'il est à l'intérieur du polygone
                        if x == xinters:
                            return True
        p1x, p1y = p2x, p2y
    return interieur
 

def dict_coord_stats(data):
    """Sort un dictionnaire qui contient les 
    informations des coordonnes sur chaque station
    ayant cette-là en clé afin de la pouvoir localiser
    
    Args: 
        data (tableau): la totalité des adresses à toutes
        les stations
    Returns: 
        dict_coord (dict): dictionnaire qui organise les 
        coordonnées par station en utilisant l'adresse comme référence"""
    
    dict = {}

    for bloc in data["adresses"]:

        for ref, adresse in bloc.items():
            if ref == "dep":
                continue

            lat, lon = coord(adresse)
            dict[ref] = [lat, lon]

    return dict
