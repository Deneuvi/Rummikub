# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:35:55 2024

@author: kerri
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class JetonWidget(QLabel):
    def __init__(self, jeton, parent):
        super().__init__(parent)
        self.jeton = jeton
        self.parent = parent  # Stocker la référence au parent
        self.setPixmap(QPixmap(jeton.image))
        self.setFixedSize(60, 60)
        self.setScaledContents(True)
        self.setStyleSheet("border: 1px solid black;")
        self.selected = False

    def mousePressEvent(self, event):
        # Basculer l'état de sélection
        self.selected = not self.selected
        # Mettre à jour le style de la bordure en fonction de la sélection
        self.setStyleSheet("border: 3px solid green;" if self.selected else "border: 1px solid black;")
        
        # Mettre à jour la liste selected_jetons dans le GUI parent
        if self.selected:
            self.parent.selected_jetons.append(self.jeton)  # Ajouter le jeton à la sélection
        else:
            self.parent.selected_jetons.remove(self.jeton)  # Retirer le jeton de la sélection
