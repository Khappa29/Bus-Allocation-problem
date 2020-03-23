# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:52:02 2020
@author: vinch
A faire: 
"""

import random as rd
import numpy as np
import matplotlib.pyplot as plt

#Hyperparamètres
v = 7                       # Vitesse moyenne des bus (m/s)
f = 10                      # Fréquence des bus (bus/heure)
c = 2

##### Définitions des classes et fonctions #####

class Arret:
    """Objet Arret qui contient ses coordonnées, si c'est la station principale ou non
    Une fonction de description __str__
    Un mutateur pour la déclarer comme gare principale
    Un mutateur pour modifier ses coordonnées"""
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
    """ Objet ligne qui comporte l'ensemble des arrêts, leur nombre ainsi que 
    la matrice des distances euclidiennes
    Un fonction descriptive
    Un mutateur pour ajouter un arrêt
    Un mutateur pour supprimer un arrêt
    Une fonction qui ordonne les arrêts"""
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
        self.Nb_arrets = len(self.arrets)
        print("On vient d'ajouter l'arrêt", arret, "à cette ligne.")

    def suppr_arret(self, arret):
        if arret not in self.arrets :
            print(arret,"n'est pas dans les arrêts de cette ligne.")
        else :
            self.arrets.remove(arret)
            print("On vient de supprimer l'arrêt", arret, "de cette ligne.")        
    
    def ordonner_arrets(self):
        """Fonction qui ordonnes les arrêts de la manière suivante:
        Choisit un point de départ au hasard. 
        A chaque itération va trouver la station la plus proche du dernier
        élément de la liste.
        A la fin mesure la longueur totale afin de garder la ligne la plus courte
        Donc en somme cette fonctionne ordonne les arrêts afin de minimiser
        la distance parcourue par le bus.
        """
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

##### Affichage #####

def display_arrets(arrets):
    X = [arrets[i].x for i in range(len(arrets))]
    Y = [arrets[i].y for i in range(len(arrets))]
    plt.plot(X,Y, 'or')
    
def display_lignes(lignes):
    for l in lignes:
        X = [a.x for a in l.arrets]
        Y = [a.y for a in l.arrets]
        plt.plot(X,Y)


class Reseau:
    
    def __init__(self, arrets, lignes):
        self.arrets = arrets
        self.lignes = lignes
        self.nb_arrets = len(self.arrets)
        self.nb_lignes = len(self.lignes)
    
    def __init__(self): #Inch allah le polymorphisme marche en python
        self.arrets = []
        self.lignes = []
        self.nb_arrets = rd.randint(5,10)
        print("On choisi de créer",Nb_arrets,"arrêts.")
        #Création aléatoire d'un certain nombre d'arrêts
        arrets_dispo = []
        for i in range(self.nb_arrets):
            arret = Arret()
            self.arrets.append(arret)
            arrets_dispo.append(arret)
        
        r_m = rd.choice(self.arrets)     # Arrêt principal
        r_m.set_Gare_Centrale()
        
        ##### Construction des tableaux et constantes #####
        
        self.D = D_build(self.arrets)         # Matrice des distances entre les arrêts i et j
        self.T = T_build(self.arrets)         # Matrice des nb de personnes en attente à l’arrêt i ayant l’arrêt j pour destination
        #print("D :", D)
        #print("T :", T)
        
        self.nb_lignes = rd.randint(2,self.nb_arrets-1)     # On veut au moins deux arrêts par lignes, sachant que toutes doivent passer par la gare centrale
        print("On choisi de créer",self.nb_lignes,"lignes.")
        self.lignes = []
        arrets_dispo.remove(r_m)
        nb_arrets_dispo = len(arrets_dispo)
        
        for i in range(1,self.nb_lignes+1):
            print()
            print("--- Construction d'une ligne ---")
            if i != self.nb_lignes :
                nb_arrets_ligne = rd.randint(1,nb_arrets_dispo-(self.nb_lignes-i))
                arrets_ligne = [r_m]                        # On ajoute forcement la gare centrale
                for j in range(nb_arrets_ligne):
                    arret = rd.choice(arrets_dispo)
                    arrets_dispo.remove(arret)
                    arrets_ligne.append(arret)
            else : 
                arrets_ligne = [r_m] + arrets_dispo         # On fait la dernière ligne avec les arrêts restants
                
            self.lignes.append(Ligne(arrets_ligne))
                
            print("La ligne créée est :", self.lignes[i-1])
            nb_arrets_dispo = len(arrets_dispo)
            self.lignes[i-1].ordonner_arrets()
            print("Après arrangement, on a la ligne :", self.lignes[i-1])
    
    def display(self):
        display_arrets(self.arrets)
        display_lignes(self.lignes)
        plt.grid()
        plt.show()


    def D_build(self):
        """
        Construction de la matrice des distance euclidiennes entre arrêts
        """
        nb_arrets = len(self.arrets)
        D = np.zeros([nb_arrets, nb_arrets])
        for i in range(nb_arrets):
            for j in range(i, nb_arrets):
                D[i,j] = np.sqrt(abs(self.arrets[i].x - self.arrets[j].x)**2 + abs(self.arrets[i].y - self.arrets[j].y)**2)
                D[j,i] = D[i,j]
        D = np.array(D).tolist()
        return D
    
    def T_build(self):
        """
        Construction d'une matrice aléatoire qui représente le nombre de personnnes
        présentes à chaque arrêt
        """
        nb_arrets = len(self.arrets)
        T = np.zeros([nb_arrets, nb_arrets])
        for i in range(nb_arrets):
            for j in range(nb_arrets):
                if i != j :
                    T[i,j] = int(rd.uniform(0,11))
        return T


### MAIN ###
    

Bus = Reseau()

Bus.display()
