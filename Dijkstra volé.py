# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 17:53:58 2020

@author: vinch
"""

# Implémentation de l’algorithme de Dijkstra
Graphe = [[ 0, 2, 5, False, 3, False, False ],
[ 2, 0, 2, 1, False, False, 8 ],
[ 5, 2, 0, 1, 4, 2, False ],
[ False, 1, 1, 0, False, False, 5 ],
[ 3, False, 4, False, 0, False, False ],
[ False, False, 2, False, False, 0, 1 ],
[ False, 8, False, 5, False, 1, False ]]
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
    for i in range(n) :
        if not(i in S_marques) :
            # si le sommet d’indice i n’est pas marqué
            if L[i]:
                if not(min) or L[i][0] < min :
                    # on trouve un nouveau minimum
                    # ou si le minimum n’est pas défini
                    min = L[i][0]
                    marque = i
        
    return(marque)
    
    
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
    T = calcule_tableau (Graphe,depart)
    # liste qui contiendra le chemin le plus court, on place l’arrivée
    C = [ arrivee ]
    while C[-1] != depart :
        C.append( T[-1][ C[-1] ][1] )
        # Renverse C, pour qu’elle soit plus lisible
    C.reverse()
    return C

print(plus_court_chemin(Graphe, 1, 5))