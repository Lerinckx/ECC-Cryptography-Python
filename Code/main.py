# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 15:20:19 2025

@author: maxime
"""

import Chiffrement

def simuler_chiffrement_DH_AES(message):
    """
    Simule l'échange de clé Diffie-Hellman et chiffre/déchiffre un message avec AES.
    
    - Alice et Bob génèrent leurs clés publiques et privées.
    - Ils échangent leurs clés publiques et dérivent une clé secrète commune (Ksym).
    - Alice chiffre le message avec AES en utilisant Ksym et l'envoie à Bob.
    - Bob déchiffre le message avec la même clé Ksym.
    
    Arguments:
        message (str): Le message à chiffrer.
    
    Lève:
        ValueError: Si l'échange de clé échoue ou si le message déchiffré ne correspond pas à l'original.
    """
    # Paramètres de la courbe elliptique
    a = 109454571331697278617670725030735128145969349647868738157201323556196022393856
    b = 107744541122042688792155207242782455150382764043089114141096634497567301547839
    mod = 109454571331697278617670725030735128145969349647868738157201323556196022393859
    chiffrage = Chiffrement.DH_AES(a, b, mod)
    
    # Génération des clés d'Alice et Bob
    pkA, skA, pkB, skB = chiffrage.generation_cles()
    
    # Échange de clés et dérivation de Ksym
    print(f"Bob envoi à Alice : {pkB}")
    print(f"Alice envoi à Bob : {pkA}")
    ksym_Alice = chiffrage.derive_cle_secrete(pkB, skA)
    print(f"Alice calcul Ksym : {ksym_Alice}")
    ksym_Bob = chiffrage.derive_cle_secrete(pkA, skB)
    print(f"Bob calcul Ksym : {ksym_Bob}")
    
    if ksym_Alice == ksym_Bob:
        print("L'obtention de Ksym a réussi")
        ksym = ksym_Bob
    else:
        raise ValueError("Erreur d'échange de clés.")
        
    # Chiffrement et transmission du message
    ciphertext, iv = chiffrage.chiffrement_message(message, ksym)
    print("Alice envoie le message chiffré à Bob")
    print(f"Message chiffré : {ciphertext}")
    
    # Déchiffrement et vérification
    message_decrypte = chiffrage.dechiffrement_message(ciphertext, iv, ksym)
    print("Bob décrypte le message")
    print(f"Message déchiffré : {message_decrypte}")
    
    if message_decrypte == message:
        print("Le chiffrement et déchiffrement ont réussi !")
    else:
        raise ValueError("Erreur : Le message déchiffré ne correspond pas au message original.")


def simuler_chiffrement_EC_ElGamal(message):
    """
    Simule le chiffrement et déchiffrement d'un message en utilisant EC-ElGamal.
    
    - Alice génère une clé publique et l'envoie à Bob.
    - Bob chiffre le message en utilisant la clé publique d'Alice et envoie son propre pkB à Alice.
    - Alice utilise sa clé privée pour déchiffrer le message.
    
    Arguments:
        message (str): Le message à chiffrer.
    
    Retourne:
        str: Le message déchiffré.
    
    Lève:
        ValueError: Si le chiffrement ou déchiffrement échoue.
    """
    # Paramètres de la courbe elliptique
    a = 109454571331697278617670725030735128145969349647868738157201323556196022393856
    b = 107744541122042688792155207242782455150382764043089114141096634497567301547839
    mod = 109454571331697278617670725030735128145969349647868738157201323556196022393859
    chiffrage = Chiffrement.EC_ElGamal(a, b, mod)
    
    # Génération des clés d'Alice et Bob
    pkA, skA, pkB, skB = chiffrage.generation_cles()
    
    # Chiffrement du message par Bob
    try:
        print(f"Alice envoie sa clé publique à Bob : {pkA}")
        print("Bob chiffre le message grâce à sa clé privée et à la clé publique d'Alice")
        (M_chiffre, decalage) = chiffrage.chiffrement_message(pkA, skB, message)
        print(f"Bob envoie à Alice sa clé publique : {pkB} ; et le message chiffré : {M_chiffre} avec le décalage : {decalage}")
    except ValueError as e:
        return f"Erreur de chiffrement : {e}"
    
    # Déchiffrement du message par Alice
    try:
        print("Alice déchiffre le message en utilisant sa clé privée, la clé publique de Bob, le message chiffré et le décalage")
        M_dechiffre = chiffrage.dechiffrement_message(skA, pkB, M_chiffre, decalage)
        return M_dechiffre
    except ValueError as e:
        return f"Erreur de déchiffrement : {e}"

# Exemple d'exécution
message1 = "Je suis heureux que cela fonctionne, vive mon TIPE !"
message2 = "Je suis heureux."
simuler_chiffrement_EC_ElGamal(message2)
