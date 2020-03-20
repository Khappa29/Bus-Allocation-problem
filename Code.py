# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:52:02 2020

@author: vinch

A faire: 


"""

import random as rd
import numpy as np
import matplotlib.pyplot as plt

##### Définitions des classes et fonctions #####

class Arret:
    def __init__(self):
        self.x = rd.uniform(-10,10)
        self.y = rd.uniform(-10,10)

def D_build(Arrets):
    D = np.zeros([Nb_arrets, Nb_arrets])
    for i in range(Nb_arrets):
        for j in range(i, Nb_arrets):
            D[i,j] = np.sqrt(abs(Arrets[i].x - Arrets[j].x)**2 + abs(Arrets[i].y - Arrets[j].y)**2)
            D[j,i] = D[i,j]
    return D

def T_build(Arrets):
    T = np.zeros([Nb_arrets, Nb_arrets])
    for i in range(Nb_arrets):
        for j in range(Nb_arrets):
            if i != j :
                T[i,j] = int(rd.uniform(0,11))
    return T

##### Construction des tableaux et constantes #####

D = D_build(Arrets)         # Matrice des distances entre les arrêts i et j
T = T_build(Arrets)         # Matrice des nb de personnes en attente à l’arrêt i ayant l’arrêt j pour destination
#print("D :", D)
#print("T :", T)

v = 7                       # Vitesse moyenne des bus (m/s)
f = 10                      # Fréquence des bus (bus/heure)
c = 2                       # Temps nécessaire pour changer de bus (correspondance), en minutes

##### Affichage #####


def display_arrets(arrets):
    X = [arrets[i].x for i in range(len(arrets))]
    Y = [arrets[i].y for i in range(len(arrets))]
    plt.plot(X,Y)





display_arrets(Arrets)


plt.grid()
plt.show()
