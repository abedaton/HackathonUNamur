# -*- coding: utf-8 -*-
"""
Created on Fri Oct 26 19:45:01 2018

"""

import math

PosCommercant1 = (345,6789)
PosCommercant2 = (4567,89)
PosCommercant3 = (1234,2341)
PosCommercant4 = (45,89)
PosCommercant5 = (0,0)
PosCommercant6 = (-4,-9)
PosCommercant7 = (-5678,-123)
PosCommercant8 = (-123,-5678)
PosCommercant9 = (-6396,-3643)
PosCommercant10 = (-4567,4567)
PosCommercant11 = (-56,34)
liste_commercant = []
liste_commercant.append(PosCommercant1)
liste_commercant.append(PosCommercant2)
liste_commercant.append(PosCommercant3)
liste_commercant.append(PosCommercant4)
liste_commercant.append(PosCommercant5)
liste_commercant.append(PosCommercant6)
liste_commercant.append(PosCommercant7)
liste_commercant.append(PosCommercant8)
liste_commercant.append(PosCommercant9)
liste_commercant.append(PosCommercant10)
liste_commercant.append(PosCommercant11)
PosClient = (500,1500)

def recherche_plus_proche_(position_client,liste_commercant):
    """
    Renvoie le commerçant le plus proche à vol d'oiseau
    """
    minimum = (None,None)
    for commercant in liste_commercant:
        position_commercant = commercant    # Récupération de l'adresse du commercant
        if minimum==(None,None):
            minimum = (commercant,distance_entre_deux_points(position_client,position_commercant))
        else:
            distance = distance_entre_deux_points(position_client,position_commercant)
            if minimum[1]>distance:
                minimum = (commercant,distance)
    if minimum==(None,None):
        minimum = None
    return minimum        
        
        
        

def distance_entre_deux_points(couple_points_1,couple_points_2):
    """
    Renvoie la distance entre 2 points
    """
    Xa = couple_points_1[0]
    Xb = couple_points_2[0]
    Ya = couple_points_1[1]
    Yb = couple_points_2[1]
    return math.sqrt( ( (Xb-Xa)**2) + ( (Yb-Ya)**2) )

print(recherche_plus_proche_(PosClient,liste_commercant))
    
    