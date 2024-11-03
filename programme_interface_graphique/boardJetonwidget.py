# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:33:53 2024

@author: kerri
"""
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class BoardJetonWidget(QLabel):
    """Widget for displaying a board tile that can be selected."""
    def __init__(self, jeton, parent):
        super().__init__(parent)
        self.jeton = jeton
        self.parent = parent
        self.setPixmap(QPixmap(jeton.image))
        self.setFixedSize(60, 60)
        self.setScaledContents(True)
        self.setStyleSheet("border: 1px solid black;")
        self.selected = False

    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.setStyleSheet("border: 3px solid blue;" if self.selected else "border: 1px solid black;")
        
        # Update selected board jetons in parent GUI
        if self.selected:
            self.parent.selected_board_jetons.append(self.jeton)
        else:
            self.parent.selected_board_jetons.remove(self.jeton)