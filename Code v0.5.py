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
v = 10                     # Vitesse moyenne des bus (m/s)
f = 6/3600                    # Fréquence des bus (bus/s)
c = 2 # ??

taille_map = 1000 # (x,y) app à [-taille_map,+taille_map]²
distance_minimale = 200 # Pour éviter que des arrêts ne soient trop prêts


##### Définitions des classes et fonctions #####

def ligneInit(Graphe,depart) :
    """ Renvoie la première ligne du tableau """
    L = []
    # nombre de lignes de Graphe donc nombre de sommets
    n = len(Graphe)
    for j in range(n) :
        poids = Graphe[depart][j]
        if poids :
            # si l’arête est présente
            L.append([ poids, depart ])
        else :
            L.append(False)
    return [L]


def SommetSuivant(T, S_marques) :
    """ En considérant un tableau et un ensemble de sommets marqués,
    détermine le prochain sommet marqué. """
    L = T[-1]
    n = len(L)
    # minimum des longueurs, initialisation
    min = False
    #print("ERROR",S_marques)
    for i in range(n) :
        if not(i in S_marques) :
            # si le sommet d’indice i n’est pas marqué
            if L[i]:
                if not(min) or L[i][0] < min :
                    # on trouve un nouveau minimum
                    # ou si le minimum n’est pas défini
                    min = L[i][0]
                    marque = i
        
    return (marque)
    
    
def ajout_ligne(T,S_marques,Graphe) :
    """ Ajoute une ligne supplémentaire au tableau """
    L = T[-1]
    n = len(L)
    # La prochaine ligne est une copie de la précédente,
    # dont on va modifier quelques valeurs.
    Lnew = L.copy()
    # sommet dont on va étudier les voisins
    S = S_marques[-1]
    # la longueur du (plus court) chemin associé
    long = L[S][0]
    for j in range(n) :
        if j not in S_marques:
            poids = Graphe[S][j]
            if poids :
                # si l’arète (S,j) est présente
                if not(L[j]) : # L[j] = False
                    Lnew[j] = [ long + poids, S ]
                else :
                    if long + poids < L[j][0] :
                        Lnew[j] = [ long + poids, S ]
    T.append(Lnew)
    # Calcul du prochain sommet marqué
    S_marques.append(SommetSuivant(T, S_marques))
    return T, S_marques


def calcule_tableau(Graphe, depart) :
    """ Calcule le tableau de l’algorithme de Dijkstra """
    n = len(Graphe)
    # Initialisation de la première ligne du tableau
    # Avec ces valeurs, le premier appel à ajout_ligne
    # fera le vrai travail d’initialisation
    T=[[False] *n]
    T[0][depart] = [depart, 0]
    
    # liste de sommets marques
    S_marques = [ depart ]
    
    while len(S_marques) < n :
        T, S_marques = ajout_ligne(T, S_marques, Graphe)
        
    return T


def plus_court_chemin(Graphe, depart, arrivee) :
    """ Détermine le plus court chemin entre depart et arrivee dans
    le Graphe"""
    n = len(Graphe)
    # calcul du tableau de Dijkstra
    Truc = calcule_tableau (Graphe,depart)
    # liste qui contiendra le chemin le plus court, on place l’arrivée
    C = [ arrivee ]
    while C[-1] != depart :
        C.append( Truc[-1][ C[-1] ][1] )
        # Renverse C, pour qu’elle soit plus lisible
    C.reverse()
    return C


    
class Arret:
    """Objet Arret qui contient ses coordonnées, si c'est la station principale ou non
    Une fonction de description __str__
    Un mutateur pour la déclarer comme gare principale
    Un mutateur pour modifier ses coordonnées"""
    def __init__(self,num):
        self.x = rd.uniform(-taille_map,taille_map)
        self.y = rd.uniform(-taille_map,taille_map)
        self.r_m = False              # Par défaut, pas la gare centrale
        self.num = num
        self.ligne = 0
        
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
    def __init__(self, arrets_ligne,num):
        self.arrets = arrets_ligne
        self.Nb_arrets = len(self.arrets)
        self.Tab_dist = self.D_build()    # Tableau des distances entre chaque arrêts
        self.num = num
        
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
            
    def D_build(self):
        """
        Construction de la matrice des distance euclidiennes entre arrêts
        """
        nb_arrets = len(self.arrets)
        self.D = np.zeros([nb_arrets, nb_arrets])
        for i in range(nb_arrets):
            for j in range(i, nb_arrets):
                self.D[i,j] = np.sqrt(abs(self.arrets[i].x - self.arrets[j].x)**2 + abs(self.arrets[i].y - self.arrets[j].y)**2)
                self.D[j,i] = self.D[i,j]
        self.D = np.array(self.D).tolist()
        return self.D
    
    def ordonner_arrets(self):
        """Fonction qui ordonnes les arrêts de la manière suivante:
        Choisit un point de départ au hasard. 
        A chaque itération va trouver la station la plus proche du dernier
        élément de la liste.
        A la fin mesure la longueur totale afin de garder la ligne la plus courte
        Donc en somme cette fonctionne ordonne les arrêts afin de minimiser
        la distance parcourue par le bus.
        """
        Distance_totale = 100000
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
                Distance_minimale = 10000
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
    for i in range(len(arrets)):
        plt.annotate(arrets[i].num,(arrets[i].x,arrets[i].y))
    
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
        self.nb_arrets = rd.randint(10,40)
#        print("On choisi de créer",self.nb_arrets,"arrêts.")
        #Création aléatoire d'un certain nombre d'arrêts
        arrets_dispo = []
        for i in range(self.nb_arrets):
            arret = Arret(i)
            while self.distance_mini(arret) < distance_minimale:
                arret = Arret(i)
            self.arrets.append(arret)
            arrets_dispo.append(arret)
        
        self.r_m = rd.choice(self.arrets)     # Arrêt principal
        self.r_m.set_Gare_Centrale()
        
        ##### Construction des tableaux et constantes #####
        
        self.D_build()         # Matrice des distances entre les arrêts i et j
        self.T_build()         # Matrice des nb de personnes en attente à l’arrêt i ayant l’arrêt j pour destination
        #print("D :", D)
        #print("T :", T)
        
        self.nb_lignes = rd.randint(2,self.nb_arrets-1)     # On veut au moins deux arrêts par lignes, sachant que toutes doivent passer par la gare centrale
#        print("On choisi de créer",self.nb_lignes,"lignes.")
        self.lignes = []
        arrets_dispo.remove(self.r_m)
        nb_arrets_dispo = len(arrets_dispo)
        
        for i in range(1,self.nb_lignes+1):
#            print()
#            print("--- Construction d'une ligne ---")
            if i != self.nb_lignes :
                nb_arrets_ligne = rd.randint(1,nb_arrets_dispo-(self.nb_lignes-i))
                arrets_ligne = [self.r_m]                        # On ajoute forcement la gare centrale
                for j in range(nb_arrets_ligne):
                    arret = rd.choice(arrets_dispo)
                    arrets_dispo.remove(arret)
                    arrets_ligne.append(arret)
            else : 
                arrets_ligne = [self.r_m] + arrets_dispo         # On fait la dernière ligne avec les arrêts restants
                
            self.lignes.append(Ligne(arrets_ligne,i-1))
            self.set_lignes_in_arrets()
#            print("La ligne créée est :", self.lignes[i-1])
            nb_arrets_dispo = len(arrets_dispo)
            self.lignes[i-1].ordonner_arrets()
#            print("Après arrangement, on a la ligne :", self.lignes[i-1])
    
    
    def distance_mini(self,arret):
        mini = taille_map*4
        for a in self.arrets:
            A = a.x - arret.x
            B = a.y - arret.y
            norme = np.sqrt(A**2 + B**2)   
            if norme < mini:
                mini = norme
        return mini
    
    def set_lignes_in_arrets(self):
        for l in self.lignes:
            for a in l.arrets:
                a.ligne = l
    
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
        self.D = np.zeros([nb_arrets, nb_arrets])
        for i in range(nb_arrets):
            for j in range(i, nb_arrets):
                self.D[i,j] = np.sqrt(abs(self.arrets[i].x - self.arrets[j].x)**2 + abs(self.arrets[i].y - self.arrets[j].y)**2)
                self.D[j,i] = self.D[i,j]
        self.D = np.array(self.D).tolist()
        return self.D
    
    def T_build(self):
        """
        Construction d'une matrice aléatoire qui représente le nombre de personnnes
        présentes à chaque arrêt
        """
        nb_arrets = len(self.arrets)
        self.T = np.zeros([nb_arrets, nb_arrets])
        for i in range(nb_arrets):
            for j in range(nb_arrets):
                if i != j :
                    self.T[i,j] = int(rd.uniform(0,11))
        return self.T

    def change_de_ligne(self,arc):
        if self.arrets[arc[1]].r_m and (self.arrets[arc[0]].ligne != self.arrets[arc[2]].ligne):
            #On arrive à la station principale, changement potentiel
            #Et il y a changement :o
            return True
        return False

    def distance_arret_initial(self, arret, next_arret):
        d_tot = 0
        arret = self.arrets[arret]
        next_arret = self.arrets[next_arret]
        ligne = next_arret.ligne
        
        index = ligne.arrets.index(arret)
        next_index = ligne.arrets.index(next_arret)
        if index - next_index > 0:
            # Alors on va en ordre croissant donc le premier arrêt est en 0
            for i in range(index):
                d_tot += self.D[ligne.arrets[i].num][ligne.arrets[i+1].num]
            return d_tot
        elif index - next_index < 0:
            # On va dans l'autre sens, le premier arrêt est le dernier
            for i in range(-1,index-len(ligne.arrets),-1):
                d_tot += self.D[ligne.arrets[i].num][ligne.arrets[i-1].num]
            return d_tot
        else:
            print("CRITICAL ERROR")
            return None

    def calcul_tps_trajet(self,chemin):
        tps = 0
        for i in range(len(chemin)-2):
            tps += self.D[chemin[i]][chemin[i+1]]/v
            # t = d/v
            if self.change_de_ligne(chemin[i:i+3]):
                tps += 20
                #Il y a un paquet d'amélioration à faire.
                d_tot = self.distance_arret_initial(chemin[i+1],chemin[i+2])
                delta_t = d_tot/v - int(tps*f)/f - tps%(1/f)
                #value = 1/f - tps%(1/f) #Simplification du modèle ici, autant de bus que d'arrêts
                tps += delta_t
                
        tps += self.D[chemin[-2]][chemin[-1]]/v
        return tps
        
    def U_build(self):
        Graphe = [[False for i in range(len(self.arrets))] for j in range(len(self.arrets))]

        for l in self.lignes: #Pour chaque ligne
            
            for i in range(len(l.arrets)-1):
                Graphe[l.arrets[i].num][l.arrets[i+1].num] = self.D[l.arrets[i].num][l.arrets[i+1].num]
                Graphe[l.arrets[i+1].num][l.arrets[i].num] = self.D[l.arrets[i].num][l.arrets[i+1].num]
        self.U = np.zeros((len(Graphe),len(Graphe)))
        for i in range(len(self.arrets)):
            for j in range(len(self.arrets)):
                if j != i:
                    chemin = plus_court_chemin(Graphe,i,j)
                    self.U[i,j] = self.calcul_tps_trajet(chemin)
        self.U = np.array(self.U)
        #print(self.U)
        
        return self.U
        #U est maintenant la matrice qui contient les plus petites distances
        #entre les arrêts i vers j
        #Il faut encore prendre en compte le temps de changement d'arrêt.
        

### MAIN ###

Bus = Reseau()

Bus.display()
D = Bus.D_build()
Bus.T_build()

U = Bus.U_build()
