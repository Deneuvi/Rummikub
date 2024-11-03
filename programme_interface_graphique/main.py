# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:35:04 2024

@author: kerri
"""
import sys
from PyQt5.QtWidgets import QApplication
from rummikubgui import RummikubGUI
from joueur_I import Joueur
from jeu_I import Jeu

# Création du jeu et des joueurs
jeu = Jeu()
joueur1 = Joueur("Joueur 1")
joueur2 = Joueur("Joueur 2")
joueur3 = Joueur("Joueur 3")
joueur4 = Joueur("Joueur 4")
jeu.ajouter_joueur(joueur1)
jeu.ajouter_joueur(joueur2)
jeu.ajouter_joueur(joueur3)
jeu.ajouter_joueur(joueur4)
jeu.distribuer_jetons(14)

# Initialisation de l'application Qt
app = QApplication(sys.argv)
gui = RummikubGUI(jeu)
gui.show()
sys.exit(app.exec_())