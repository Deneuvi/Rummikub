# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:49:03 2024

@author: kerri
"""


class Jeton:
    def __init__(self, nombre, couleur, image):
        self.nombre = nombre  # Assurez-vous que nombre n'est jamais None
        self.couleur = couleur
        self.image = image

    def __str__(self):
        return f"{self.nombre} {self.couleur}"

    def est_joker(self):
        return False  # Méthode par défaut pour les jetons normaux