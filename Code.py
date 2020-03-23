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
        self.r_m = False              # Par défaut, pas la gare centrale
        
    def __str__(self):
        return "(Arret : X = " + str(self.x) + ' ; Y = '+ str(self.y) + ")"
    
    def set_Gare_Centrale(self):
        self.r_m = True
        
    def set_coor (self,x,y):
        self.x = x
        self.y = y


class Ligne:
    def __init__(self, arrets_ligne):
        self.arrets = arrets_ligne
        self.Nb_arrets = len(self.arrets)
        self.Tab_dist = D_build(self.arrets)    # Tableau des distances entre chaque arrêts
        
    def __str__(self):
        print("Ligne -", self.Nb_arrets, 'arrêts')
        print("Ses arrêts sont ")
        for arret in self.arrets :
            if arret.r_m == True :
                print(arret, "(Gare Centrale)")
            else :
                print(arret)
        return ""
    
    def ajout_arret(self, arret):
        self.arrets.append(arret)
        print("On vient d'ajouter l'arrêt", arret, "à cette ligne.")

    def suppr_arret(self, arret):
        if arret not in self.arrets :
            print(arret,"n'est pas dans les arrêts de cette ligne.")
        else :
            self.arrets.remove(arret)
            print("On vient de supprimer l'arrêt", arret, "de cette ligne.")        
    
    def ordonner_arrets(self):
        Distance_totale = 1000
        Ordre = []
        #print()
        #for i in self.Tab_dist:
        #    print(i)
        #print()
        for Pt_depart in range(1,self.Nb_arrets+1):
            #print("On commence avec", Pt_depart)
            Element = [Pt_depart]
            Tab_dist_MST = []
            #print()
            while len(Element) != self.Nb_arrets:
                Distance_minimale = 100
                i = Element[-1]
                #print()
                #print("On se place sur le point", i)
                for j in self.Tab_dist[i-1]:
                    #print("On considère la distance", j)
                    if j < Distance_minimale and j != 0 and self.Tab_dist[i-1].index(j)+1 not in Element:
                        Distance_minimale = j
                        Plus_proche_voisin = self.Tab_dist[i-1].index(j)+1
                        #print("Benef, le voisin est :", self.Tab_dist[i-1].index(j)+1)
                    else :
                        #print("Pas benef")
                        pass
                Element.append(Plus_proche_voisin)
                #print("Element :", Element)
                Tab_dist_MST.append(Distance_minimale)
                #print(Tab_dist_MST)
                #print("La distance est de :", sum(Tab_dist_MST))
            #print("On a la liste d'idx :", Element, "pour une distance totale de",sum(Tab_dist_MST))
            
            if sum(Tab_dist_MST) < Distance_totale :
                #print("On remplace")
                Distance_totale = sum(Tab_dist_MST)
                Ordre = Element
        
        arrets_ord = []
        for i in Ordre:
            arrets_ord.append(self.arrets[i-1])
        self.arrets = arrets_ord


def D_build(Arrets):
    Nb_arrets = len(Arrets)
    D = np.zeros([Nb_arrets, Nb_arrets])
    for i in range(Nb_arrets):
        for j in range(i, Nb_arrets):
            D[i,j] = np.sqrt(abs(Arrets[i].x - Arrets[j].x)**2 + abs(Arrets[i].y - Arrets[j].y)**2)
            D[j,i] = D[i,j]
    D = np.array(D).tolist()
    return D

def T_build(Arrets):
    T = np.zeros([Nb_arrets, Nb_arrets])
    for i in range(Nb_arrets):
        for j in range(Nb_arrets):
            if i != j :
                T[i,j] = int(rd.uniform(0,11))
    return T

##### Arrêts #####

Arrets = []
Arrets_dispo = []

Nb_arrets = rd.randint(5,10)
print("On choisi de créer",Nb_arrets,"arrêts.")
for i in range(Nb_arrets):
    arret = Arret()
    Arrets.append(arret)
    Arrets_dispo.append(arret)

r_m = rd.choice(Arrets)     # Arrêt principal
r_m.set_Gare_Centrale()


##### Corps #####


Nb_arrets = 7

Arrets = []
for i in range(Nb_arrets):
    Arrets.append(Arret())

r_m = rd.choice(Arrets)     # Arrêt principal
D = D_build(Arrets)         # Matrice des distances entre les arrêts i et j
v = 7                       # Vitesse moyenne des bus (m/s)
=======
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

##### Lignes #####

Nb_lignes = rd.randint(2,Nb_arrets-1)     # On veut au moins deux arrêts par lignes, sachant que toutes doivent passer par la gare centrale
print("On choisi de créer",Nb_lignes,"lignes.")

Lignes = []
Arrets_dispo.remove(r_m)
Nb_arrets_dispo = len(Arrets_dispo)

for i in range(1,Nb_lignes+1):
    print()
    print("--- Construction d'une ligne ---")
    if i != Nb_lignes :
        Nb_arrets_ligne = rd.randint(1,Nb_arrets_dispo-(Nb_lignes-i))
        arrets_ligne = [r_m]                        # On ajoute forcement la gare centrale
        for j in range(Nb_arrets_ligne):
            arret = rd.choice(Arrets_dispo)
            Arrets_dispo.remove(arret)
            arrets_ligne.append(arret)
    else : 
        arrets_ligne = [r_m] + Arrets_dispo         # On fait la dernière ligne avec les arrêts restants
        
    Lignes.append(Ligne(arrets_ligne))
        
    print("La ligne créée est :", Lignes[i-1])
    Nb_arrets_dispo = len(Arrets_dispo)
    Lignes[i-1].ordonner_arrets()
    print("Après arrangement, on a la ligne :", Lignes[i-1])

##### Affichage #####


def display_arrets(arrets):
    X = [arrets[i].x for i in range(len(arrets))]
    Y = [arrets[i].y for i in range(len(arrets))]
    plt.plot(X,Y)





display_arrets(Arrets)


plt.grid()
plt.show()
