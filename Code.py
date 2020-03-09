# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:52:02 2020

@author: vinch
"""

import random as rd
import numpy as nd

Nb_arrets = 7

class Arret:
    def __init__(self):
        self.x = rd.uniform(-10,10)
        self.y = rd.uniform(-10,10)

Arrets = []
for i in range(Nb_arrets):
    Arrets.append(Arret())

Gare_centrale = rd.choice(Arrets)

def D_build(Arrets):
    D = np.zeros([Nb_arrets, Nb_arrets])
    for i in range(Nb_arrets):
        for j in range(i, Nb_arrets):
            D[i,j] = np.sqrt(abs(Arrets[i].x - Arrets[j].x)**2 + abs(Arrets[i].y - Arrets[j].y)**2)
            D[j,i] = D[i,j]
    return D

D = D_build(Arrets)
