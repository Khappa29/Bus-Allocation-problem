# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 15:24:21 2020

@author: vinch
"""

import numpy as np

def get_connected_arcs(arret,arcs):
    connected_arcs = []
    for arc in arcs:
        if arret in arc:
            connected_arcs.append(arc)
    return connected_arcs

def Dijkstra(arrets, lignes, arret_deb, D):
    dist = [np.inf for a in arrets]
    dist[arrets.index(arret_deb)] = 0
    arrets.remove(arret_deb)
    #Création des arcs
    arcs = []
    for l in lignes:
        for i in range(len(l.arrets)-1):
            #Création d'un arc avec le numéro de chaque arrêt et la distance entre les deux
            arcs.append((l.arrets[i],l.arrets[i+1],D[l.arrets[i].num,l.arrets[i+1].num]))
            
    
    mini = np.inf
    sommet_min = -1
    a = arret_deb
    while len(arrets) != 0:
        connected_arcs = get_connected_arcs(a,arcs) #On récupère les arcs connectés à cet arrêt
        for arc in connected_arcs:
            if arc[2] < mini:
                mini = arc[2]
                if arc[0] == a:
                    sommet_min = arc[1]
                else:
                    sommet_min = arc[0]
        
        
        if dist[sommet_min.num] > dist[a.num] + D[sommet_min.num,a.num]:
            dist[sommet_min.num] = dist[a.num] + D[sommet_min.num,a.num]
            
        a = sommet_min
        arrets.remove(sommet_min)
    #Donc là on a trouvé le sommet connecté à l'arrêt qui est le plus proche.
