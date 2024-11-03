# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:27:35 2024

@author: kerri
"""


class Joueur:
    def __init__(self, nom):
        self.nom = nom
        self.chevalet = []
        self.jetons_du_plateau = []  # Liste pour les jetons pris depuis le plateau
        self.premier_jeu = True 

    def piocher(self, jeton, depuis_plateau=False):
        if depuis_plateau:
            self.jetons_du_plateau.append(jeton)
            print(f"{self.nom} a pris un jeton du plateau : {jeton}")
        else:
            self.chevalet.append(jeton)

    def poser_jetons(self, jetons):
        for jeton in jetons:
            if jeton in self.chevalet:
                self.chevalet.remove(jeton)
    
    def ajouter_jeton(self, jeton):
        """Ajoute un jeton au chevalet."""
        print(f"Ajout du jeton {jeton} au chevalet de {self.nom}.")
        self.chevalet.append(jeton)

    def afficher_chevalet(self):
        col_size = 4
        chevalet_str = ["Jetons du chevalet :"]
        
        # Affichage du chevalet
        for i in range(0, len(self.chevalet), col_size):
            ligne = ' | '.join(f"{chr(65 + j)}: {self.chevalet[j]}" for j in range(i, min(i + col_size, len(self.chevalet))))
            chevalet_str.append(ligne)
        
        # Affichage des jetons pris du plateau
        chevalet_str.append("\nJetons pris du plateau :")
        for jeton in self.jetons_du_plateau:
            chevalet_str.append(f" - {jeton}")
        
        return '\n'.join(chevalet_str)
