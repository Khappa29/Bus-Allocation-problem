# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:52:02 2020

@author: vinch
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

##### Corps #####

Nb_arrets = 7

Arrets = []
for i in range(Nb_arrets):
    Arrets.append(Arret())

r_m = rd.choice(Arrets)     # Arrêt principal
D = D_build(Arrets)         # Matrice des distances entre les arrêts i et j
v = 7                       # Vitesse moyenne des bus (m/s)
f = 10                      # Fréquence des bus (bus/heure)
c = 2                       # Temps nécessaire pour changer de bus (correspondance), en minutes

##### Affichage #####

def display_arret(a):
    plt.plot(a.x,a.y, 'o')

def display_track(track):
    X = [track[i].x for i in range(len(track))]
    Y = [track[i].y for i in range(len(track))]
    plt.plot(X,Y)



for a in test:
    display_arret(a)

display_track(Arrets)


plt.grid()
plt.show()
