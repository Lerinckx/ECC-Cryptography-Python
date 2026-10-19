# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 19:16:24 2025

@author: Utilisateur
"""

import random
import hashlib
import ECC
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class DH_AES:
    """
    Classe gérant l'échange de clé Diffie-Hellman et le chiffrement AES avec Ksym.
    """

    def __init__(self, a, b, mod):
        """
        Initialise une courbe elliptique avec les paramètres donnés et génère un point de base.

        Arguments:
            a : int
                Le paramètre 'a' de la courbe elliptique.
            b : int
                Le paramètre 'b' de la courbe elliptique.
            mod : int
                Le modulaire de la courbe elliptique.
        """
        
        self.CE = ECC.CourbeElliptique(a, b, mod)
        self.G = self.CE.point_aleatoire()
        assert self.CE.appartient(self.G)
    
    def generation_cles(self):
        """
        Génère une paire de clés publiques et privées pour Alice et Bob.
        
        Retourne:
            tuple : (pkA, skA, pkB, skB)
                - pkA : Point, clé publique d'Alice.
                - skA : int, clé secrète d'Alice.
                - pkB : Point, clé publique de Bob.
                - skB : int, clé secrète de Bob.
        """
        
        skA = random.randint(1, self.CE.mod)
        pkA = self.CE.scalaire(skA, self.G)
        skB = random.randint(1, self.CE.mod)
        pkB = self.CE.scalaire(skB, self.G)
        return pkA, skA, pkB, skB
    
    def derive_cle_secrete(self, Pk, Sk):
        """
        Calcule une clé secrète partagée en utilisant Diffie-Hellman.
        Retourne la clé secrète partagée dérivée, hachée avec SHA-256 pour garantir une longueur fixe de 256 bits.

        Arguments:
            Pk : Point
                La clé publique de l'autre partie.
            Sk : int
                La clé secrète de l'utilisateur.

        Retourne:
            bytes : La clé secrète partagée dérivée et hachée.
        """
        
        S = self.CE.scalaire(Sk, Pk)
        S_bytes = str(S.x).encode()
        return hashlib.sha256(S_bytes).digest()
    
    def chiffrement_message(self, message, ksym):
        """
        Chiffre un message avec AES en utilisant la clé secrète partagée Ksym.

        Arguments:
            message : str
                Le message à chiffrer.
            ksym : bytes
                La clé secrète partagée utilisée pour le chiffrement.

        Retourne:
            tuple : (ciphertext, iv)
                - ciphertext : str, le message chiffré encodé en base64.
                - iv : str, le vecteur d'initialisation (IV) utilisé pour le chiffrement, encodé en base64.
        """
        
        ksym = ksym[:32]
        cipher = AES.new(ksym, AES.MODE_CBC)
        message_padded = pad(message.encode(), AES.block_size)
        ciphertext = cipher.encrypt(message_padded)
        return base64.b64encode(ciphertext).decode(), base64.b64encode(cipher.iv).decode()
    
    def dechiffrement_message(self, ciphertext, iv, ksym):
        """
        Déchiffre un message avec AES en utilisant la clé secrète Ksym.

        Arguments:
            ciphertext : str
                Le message chiffré encodé en base64.
            iv : str
                Le vecteur d'initialisation (IV) encodé en base64.
            ksym : bytes
                La clé secrète partagée utilisée pour le déchiffrement.

        Retourne:
            str : Le message déchiffré.
        """
        
        ksym = ksym[:32]
        cipher = AES.new(ksym, AES.MODE_CBC, iv=base64.b64decode(iv))
        decrypted_data = unpad(cipher.decrypt(base64.b64decode(ciphertext)), AES.block_size)
        return decrypted_data.decode()

class EC_ElGamal:
    """
    Classe gérant le chiffrement et déchiffrement basé sur les courbes elliptiques (EC-ElGamal).
    """
    
    def __init__(self, a, b, mod):
        """
        Initialise une courbe elliptique avec les paramètres donnés et génère un point de base.

        Arguments:
            a : int
                Le paramètre 'a' de la courbe elliptique.
            b : int
                Le paramètre 'b' de la courbe elliptique.
            mod : int
                Le modulaire de la courbe elliptique.
        """
        
        self.CE = ECC.CourbeElliptique(a, b, mod)
        self.G = self.CE.point_aleatoire()
        assert self.CE.appartient(self.G)
        
    def generation_cles(self):
        """
        Génère une paire de clés publiques et privées pour Alice et Bob.
        
        Retourne:
            tuple : (pkA, skA, pkB, skB)
                - pkA : Point, clé publique d'Alice.
                - skA : int, clé secrète d'Alice.
                - pkB : Point, clé publique de Bob.
                - skB : int, clé secrète de Bob.
        """
        
        skA = random.randint(1, self.CE.mod)
        pkA = self.CE.scalaire(skA, self.G)
        skB = random.randint(1, self.CE.mod)
        pkB = self.CE.scalaire(skB, self.G)
        return pkA, skA, pkB, skB 
    
    def message_to_point(self, message):
        """
        Convertit un message en un point sur la courbe elliptique en utilisant la méthode de rejet.

        Arguments:
            message : str
                Le message à convertir en point sur la courbe elliptique.

        Retourne:
            tuple : (point, decalage)
                - point : ECC.Point, le point sur la courbe elliptique représentant le message.
                - decalage : int, le décalage appliqué au message pour obtenir un point valide.
        
        Lève:
            ValueError : Si le message ne peut pas être converti en point après plusieurs tentatives.
        """
        
        x_original = int.from_bytes(message.encode(), 'big') % self.CE.mod
        x = x_original
        decalage = 0
        boucle_max = 1000
        boucle = 0

        while boucle < boucle_max:
            try:
                y = self.CE(x)
                return ECC.Point(x, y, self.CE.mod), decalage
            except ValueError:
                x = (x + 1) % self.CE.mod
                decalage += 1
                boucle += 1

        raise ValueError("Le message ne peut être converti")
    
    def point_to_message(self, point, decalage=0):
        """
        Convertit un point elliptique en message texte original en retirant le décalage appliqué.

        Arguments:
            point : ECC.Point
                Le point sur la courbe elliptique à convertir en message.
            decalage : int
                Le décalage appliqué lors de la conversion du message en point.

        Retourne:
            str : Le message récupéré depuis le point elliptique, ou un message d'erreur si la conversion échoue.
        """
        
        x_original = (point.x - decalage) % self.CE.mod
        try:
            message = x_original.to_bytes((x_original.bit_length() + 7) // 8, 'big').decode()
            return message
        except UnicodeDecodeError:
            return f"[Message illisible], {x_original}"
    
    def chiffrement_message(self, pkA, skB, message):
        """
        Chiffre un message en le transformant en point elliptique et en utilisant Diffie-Hellman.

        Arguments:
            pkA : ECC.Point
                La clé publique de la partie à qui le message est destiné.
            skB : int
                La clé privée de l'envoyeur
            message : str
                Le message à chiffrer.

        Retourne:
            tuple : (M_chiffre, decalage)
                - M_chiffre : ECC.Point, le message chiffré 
                - decalage : int, le décalage appliqué lors de la conversion du message.
        """
        
        M, decalage = self.message_to_point(message)
        skB_pkA = self.CE.scalaire(skB, pkA)
        M_chiffre = self.CE.plus(skB_pkA, M)
        return M_chiffre, decalage
    
    def dechiffrement_message(self, skA, pkB, M_chiffre, decalage):
        """
        Déchiffre un message chiffré sous forme de point elliptique.

        Arguments:
            skA : int
                La clé secrète de l'utilisateur (utilisée pour déchiffrer).
            pkB : ECC.Point
                La clé publique de l'envoyeur
            M_chiffre : ECC.Point
                Le message chiffré sous forme de point elliptique
            decalage : int
                Le décalage appliqué lors de la conversion du message en point.

        Retourne:
            str : Le message déchiffré.
        """
        
        skA_C1 = self.CE.scalaire(skA, pkB)
        skA_C1_inv = skA_C1.opose()
        M_dechiffre = self.CE.plus(M_chiffre, skA_C1_inv)
        return self.point_to_message(M_dechiffre, decalage)
