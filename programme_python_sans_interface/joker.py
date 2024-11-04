# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:26:29 2024

@author: kerri
"""
from jeton import Jeton 
class Joker(Jeton):
    def __init__(self,joker_image):
        super().__init__(None, 'Joker',joker_image)  # Utiliser None pour le nombre car le joker ne devrait pas avoir de valeur spécifique

    def __str__(self):
        return "Joker"  # Affiche "Joker" à la place de "0 Joker"

    def est_joker(self):
        return True  # Méthode pour indiquer que c'est un joker