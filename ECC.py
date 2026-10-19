# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:05:57 2024

@author: maxime
"""

import matplotlib.pyplot as plt
import numpy as np
import random

mod_zero = float('inf')

"""Arithmétique modulaire"""

def inv_mod(n, p):
    """
    Calcule l'inverse modulaire de x modulo 'p' en utilisant l'algorithme d'Euclide étendu.
    
    Arguments:
        x : int
            Le nombre dont on souhaite trouver l'inverse modulo p.
        p : int
            Le modulo pour lequel on cherche l'inverse de x.
    
    Retourne:
        int : L'inverse modulaire de x modulo p.
    
    Lève une exception ValueError si l'inverse modulaire n'existe pas (si le pgcd(x, p) ≠ 1).
    """
    
    a, r, u, v = n, p, 1, 0
    
    while r > 0:
        q = a // r
        a, r = r, a % r
        u, v = v, u - q * v

    assert a == 1, "L'inverse modulaire n'existe pas car pgcd(x, p) ≠ 1"
    
    return u % p


def residu_quadratique(n, p):
    """
    Trouve une racine carrée de n modulo p, où p est un premier impair et n est un résidu quadratique modulo p.

    Arguments:
       n : int
           Le nombre pour lequel on cherche la racine carrée modulo p.
       p : int
           Le modulo, un nombre premier impair.

    Retourne:
       int : La racine carrée de n modulo p.

    Lève une exception ValueError si n n'est pas un résidu quadratique modulo p.

    Si p ≡ 3 (mod 4), utilise une méthode simplifiée. Sinon, utilise l'algorithme de Tonelli-Shanks.
    """
   
    # Vérifie si n est un résidu quadratique modulo p
    if pow(int(n), (p - 1) // 2, p) != 1:  # Si n n'est pas un résidu quadratique
        raise ValueError(f"{n} n'est pas un résidu quadratique modulo {p}")
    
    # Cas trivial
    if n == 0:
        return 0
    if n == 1:
        return 1

    # Si p ≡ 3 (mod 4), on peut utiliser la formule simplifiée
    if p % 4 == 3:
        return pow(int(n), (p + 1) // 4, p)

    # Sinon, utiliser l'algorithme de Tonelli–Shanks
    # Recherche de q et s dans p-1 = q * 2^s, où q est impair
    s = 0
    q = p - 1
    while q % 2 == 0:
        s += 1
        q //= 2

    # Initialisation de z
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # Initialisation de x, y, t, m
    x = pow(n, (q + 1) // 2, p)
    y = pow(n, q, p)
    t = pow(n, q, p)
    m = s

    while t != 0 and t != 1:
        # Recherche d'un k
        t2i = t
        i = 0
        for i in range(1, m):
            t2i = pow(t2i, 2, p)
            if t2i == 1:
                break
        # Mise à jour de x, y, t, m
        if i == 0:
            return x
        b = pow(y, 2 ** (m - i - 1), p)
        m = i
        x = (x * b) % p
        y = (y * b * b) % p
        t = (t * b * b) % p

    return x  # Si t == 1, on a trouvé la racine carrée.

class CourbeElliptique:
    """
    Représente une courbe elliptique de l'équation y^2 = x^3 + ax + b (mod p).
    """
    
    def __init__(self, a, b, mod=mod_zero):
        """
        Initialise une courbe elliptique avec les paramètres a, b et mod.

        Arguments:
            a : int
                Le coefficient de x dans l'équation de la courbe elliptique.
            b : int
                Le coefficient constant dans l'équation de la courbe elliptique.
            mod : int, optionnel
                Le modulo de la courbe (par défaut, "mod_zero" est utilisé).
        
        Lève une exception ValueError si le delta de la courbe est nul.
        """
        
        self.a = a
        self.b = b
        self.mod = mod
        
        self.delta = (-16) * (4 * (a**3) + 27 * (b**2)) % self.mod
        if not self.delta:
            raise ValueError("Le delta est nul")
    
    def __str__(self):
        """
       Retourne une représentation sous forme de chaîne de la courbe elliptique.

       Retourne:
           str : Une chaîne représentant l'équation de la courbe elliptique.
       """
       
        return f"y^2 = x^3 + {self.a} * x + {self.b}" 
    
    def __repr__(self):
        """
       Retourne une représentation plus détaillée de la courbe elliptique.

       Retourne:
           str : Une chaîne détaillant la courbe elliptique et son modulo.
       """
       
        return str(self) + " mod " + str(self.mod)
        
    
    def __eq__(self, autre):
        """
        Vérifie si deux courbes elliptiques sont égales.

        Arguments:
            autre : CourbeElliptique
                Une autre courbe elliptique à comparer.
        
        Retourne:
            bool : True si les courbes sont égales, False sinon.
        """
        
        return (self.a, self.b, self.mod) == (autre.a, autre.b, autre.p)
    
    def __call__(self, x): 
        """
        Retourne y pour un x donné, modulo p.

        Arguments:
            x : int
                La coordonnée x du point.

        Retourne:
            int : La coordonnée y du point sur la courbe elliptique.

        Lève une exception ValueError si aucune solution n'existe pour ce x.
        """
        
        y2 = (x**3 + self.a * x + self.b) % self.mod
        try:
            y_pos = residu_quadratique(y2, self.mod)
            return y_pos
        
        except Exception:
            raise ValueError(f"Aucune solution pour x = {x} dans Z/{self.mod}Z")

    def appartient(self, P):
        """
        Vérifie si un point P appartient à la courbe elliptique.

        Arguments:
            P : Point
                Le point à vérifier.

        Retourne:
            bool : True si le point appartient à la courbe, False sinon.
        """
       
        if P.isInf():  # Le point à l'infini appartient toujours à la courbe
           return True
    
        x = P.x
        y = P.y
        return y == self(x) or y == self.mod - self(x)

    def point_aleatoire(self, inf=-10, sup=10):
        """
        Génère un point aléatoire sur la courbe elliptique.

        Arguments:
            inf : int, optionnel
                La limite inférieure de l'intervalle pour la coordonnée x.
            sup : int, optionnel
                La limite supérieure de l'intervalle pour la coordonnée x.

        Retourne:
            Point : Un point aléatoire sur la courbe elliptique.
        """
        
        i = random.randint(0, 1) # Au hasard entre positif et négatif
        
        boucle_max = 1000
        boucle = 0
        
        while boucle < boucle_max:
            x = random.randint(inf, sup)
            try:
                y_pos = self(x)  # Utiliser la méthode __call__ mise à jour
                y_neg = self.mod - y_pos
                return Point(x, y_pos, self.mod) if i else Point(x, y_neg, self.mod)
            except ValueError:
                pass  # Si n'est pas un résidu quadratique, on essaie un autre x
            boucle += 1
           
    def plus(self, P, Q):
        """
        Effectue l'addition de deux points P et Q sur la courbe elliptique.

        Arguments:
            P : Point
                Le premier point à additionner.
            Q : Point
                Le second point à additionner.

        Retourne:
            Point : Le résultat de l'addition des deux points.
        
        Lève une exception si l'un des points ne appartient pas à la courbe.
        """
        
        assert self.appartient(P)
        assert self.appartient(Q)
        
        if P.isInf():
            return Q.copy()
        
        if Q.isInf():
            return P.copy()
        
        if P == Q.opose():
            return Point(None, None)
        
        if P != Q:
            a_plus = (Q.y - P.y) % self.mod 
            b_plus = (Q.x - P.x) % self.mod 
            l = (a_plus*(inv_mod(b_plus, self.mod))) % self.mod
        
        else:  # Si P = Q
            a_plus = (3*(P.x**2) + self.a) % self.mod
            b_plus = (2*P.y) % self.mod
            l = (a_plus*inv_mod(b_plus, self.mod)) % self.mod
            
        x3 = (l**2 - P.x - Q.x) % self.mod 
        y3 = (l*(P.x - x3) - P.y) % self.mod
        
        R = Point(x3, y3, self.mod)
        assert self.appartient(R)
        return R
        
    def scalaire(self, n, P):
        """
        Calcule n * P (multiplication d'un point par un scalaire) en utilisant l'exponentiation rapide.

        Arguments:
            n : int
                Le scalaire par lequel multiplier le point.
            P : Point
                Le point à multiplier.

        Retourne:
            Point : Le résultat de la multiplication scalaire.
        
        Lève une exception si le point n'appartient pas à la courbe ou si n n'est pas un entier.
        """
        
        assert self.appartient(P)  # Vérification si point appartient à la courbe
        assert type(n) == int # Ne marche que si n est entier
        
        if n < 0:
            return self.mul(-n, -P)  # On prend l'opposé du point
        
        # Initialisation
        Q = P.copy()
        R = Point(None, None, self.mod)
        
        while n > 0:
            if n % 2 == 1: # Si n est impaire
                R = self.plus(R, Q) # R = R+Q
            Q = self.plus(Q, Q) # Q = 2*Q
            n //= 2 # On divise n par deux 
            
        return Point(R.x, R.y, self.mod)
    
    def afficher_courbe(self, xmin=-10, xmax=10):
        """
        Trace la courbe elliptique dans l'intervalle [xmin, xmax] modulo p.
        
        Arguments:
            xmin : int, optionnel
                La borne inférieure de l'intervalle pour x. Par défaut, -10.
            xmax : int, optionnel
                La borne supérieure de l'intervalle pour x. Par défaut, 10.
    
        Retourne:
            None : Affiche un graphique avec les points de la courbe elliptique.
        """
       
        if self.mod > 1000:
            x_vals = [i for i in range(1000)]
        else:
            x_vals = np.arange(self.mod)
            
        points = []

        for x in x_vals:
            try:
                y_pos = self(x)  # Utiliser la méthode __call__ mise à jour
                points.append((x, y_pos))
                points.append((x, self.mod - y_pos))  # -y est aussi une solution
            except ValueError:
                pass  # Si n'est pas un résidu quadratique, on passe au x suivant
        
        # Tracer les points sur le graphique
        plt.figure(figsize=(8, 6))
        for (x, y) in points:
            plt.plot(x, y, 'bo')  # Point positif
            plt.plot(x, -y % self.mod, 'ro')  # Point négatif modulo p
        
        titre = f"Courbe elliptique : y^2 = x^3 + {self.a}x + {self.b} modulo {self.mod}"
        if len(titre) > 100:
            plt.title("Courbe elliptique modulo")
        else: 
            plt.title(titre)

class Point:
    """
   Représente un point sur une courbe elliptique avec des coordonnées (x, y).
   """
  
    
    def __init__(self, x, y, p=mod_zero):
        """
        Initialise un point avec les coordonnées (x, y) et le modulo p.

        Arguments:
           x : int
               La coordonnée x du point.
           y : int
               La coordonnée y du point.
           p : int, optionnel
               Le modulo pour la courbe elliptique.
        """
       
        self.x = x % p if x != None else x
        self.y = y % p if y != None else y
        self.p = p 
     
    def isInf(self): # Pour faire la différence entre le point infini et les autres
        """
        Vérifie si le point est le point à l'infini.

        Retourne:
           bool : True si le point est à l'infini, False sinon.
       """
       
        return (self.x, self.y) == (None, None)
    
    def __str__(self):
        """
        Retourne une chaîne de caractères représentant le point.

        Retourne:
           str : La représentation du point sous forme de chaîne.
       """
       
        return "0" if self.isInf() else f"({self.x}, {self.y})"
    
    def __repr__(self):
        """
        Retourne une représentation plus détaillée du point.

        Retourne:
            str : La représentation détaillée du point.
        """
        
        return str(self)
    
    def __eq__(self, Q):
        """
       Vérifie si deux points sont égaux.

       Arguments:
           Q : Point
               Le point à comparer avec l'objet courant.
       
       Retourne:
           bool : True si les points sont égaux, False sinon.
       """
       
        return (self.p, self.x, self.y) == (Q.p, Q.x, Q.y)
    
    def opose(self):
        """
        Retourne l'opposé d'un point sur la courbe elliptique.

        Retourne:
           Point : L'opposé du point courant.
        """
       
        if self.isInf():
            return self
        
        return Point(self.x, (-self.y) % self.p, self.p)
    
    def copy(self):
        """
        Crée une copie du point courant.

        Retourne:
           Point : Une copie du point courant.
        """
       
        return Point(self.x, self.y, self.p)

