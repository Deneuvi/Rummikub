# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:19:31 2024

@author: kerri
"""


from jeu import Jeu
from joueur import Joueur 

jeu = Jeu()
 
joueur1 = Joueur("Alice")
joueur2 = Joueur("Bob")
joueur3 = Joueur("Charlie")
joueur4 = Joueur("Diana")

jeu.ajouter_joueur(joueur1)
jeu.ajouter_joueur(joueur2)
jeu.ajouter_joueur(joueur3)
jeu.ajouter_joueur(joueur4)
   
jeu.distribuer_jetons(14)
   
premier_joueur = jeu.determine_depart()
print(f"{premier_joueur.nom} commence le jeu!")
   
while True:
    if not jeu.jouer_tour():
        break
   
    gagnant = jeu.joueur_gagnant()
    if gagnant:
        print(f"{gagnant.nom} a gagné le jeu en posant tous ses jetons !")
        break
   
    if jeu.partie_terminee():
        joueur_moins_jetons = jeu.joueur_avec_moins_jetons()
        print(f"Il n'y a plus de jetons à piocher. {joueur_moins_jetons.nom} gagne avec le moins de jetons restants !")
        break