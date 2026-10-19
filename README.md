# TIPE Cryptographie
Simulation d'échange de clés Diffie-Hellman et de chiffrement AES / EC-ElGamal appliqués aux courbes elliptiques.
Cryptographie sur courbes elliptiques en Python (TIPE)

Prérequis :
Voici ce qui doit être installé sur la machine avant de lancer le code.
Python 3.x,
les module pycryptodome (pour l'algorithme AES) matplotlib et numpy (pour l'affichage des courbes)
=> code :  
git clone https://github.com/ton-pseudo/projet_crypto.git
cd projet_crypto
pip install pycryptodome matplotlib numpy

Pour lancer la simulation de chiffrement entre Alice et Bob, exécutez le script principal :
python main.py
Le script affichera dans la console la génération des points sur la courbe, l'échange des clés publiques, ainsi que les messages chiffrés et déchiffrés.

Structure des fichiers :
ECC.py : Définition des classes CourbeElliptique et Point avec la gestion de l'arithmétique modulaire.
Chiffrement.py : Implémentation des classes DH_AES et EC_ElGamal.
main.py : Script de test contenant les fonctions de simulation.
