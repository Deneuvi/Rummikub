from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class BoardJetonWidget(QLabel):
    """
    Widget for displaying a board tile that can be selected.
    
    Attributs :
    - jeton : le jeton à afficher dans le widget.
    - parent : le widget parent, généralement l'interface principale.
    - selected : booléen indiquant si le jeton est sélectionné ou non.
    
    Méthodes :
    - __init__ : initialise le widget avec le jeton et configure l'apparence de base.
    - mousePressEvent : gère la sélection/désélection du jeton par clic et met à jour le style de bordure.
    """

    def __init__(self, jeton, parent):
        """
        Initialise un widget de jeton pour l'affichage sur le plateau.
        
        Paramètres :
        - jeton : instance de Jeton représentant le jeton à afficher.
        - parent : instance de QWidget, généralement la GUI principale qui contient ce widget.
        
        Comportement :
        - Définit l'image du jeton comme pixmap du widget.
        - Configure la taille fixe à 60x60 pixels.
        - Applique un style de bordure noire par défaut.
        """
        super().__init__(parent)
        self.jeton = jeton
        self.parent = parent
        self.setPixmap(QPixmap(jeton.image))
        self.setFixedSize(60, 60)
        self.setScaledContents(True)
        self.setStyleSheet("border: 1px solid black;")
        self.selected = False

    def mousePressEvent(self, event):
        """
        Gère l'événement de clic pour sélectionner ou désélectionner le jeton.
        
        Paramètres :
        - event : événement de clic de souris.
        
        Comportement :
        - Inverse l'état de sélection du jeton (True -> False ou False -> True).
        - Met à jour la bordure en bleu si sélectionné, sinon en noir.
        - Ajoute ou retire le jeton à la liste `selected_board_jetons` de l'interface parent en fonction de l'état.
        """
        self.selected = not self.selected
        # Met à jour le style de bordure en fonction de l'état de sélection
        self.setStyleSheet("border: 3px solid blue;" if self.selected else "border: 1px solid black;")
        
        # Ajoute ou retire le jeton dans la liste des jetons sélectionnés du parent
        if self.selected:
            self.parent.selected_board_jetons.append(self.jeton)
        else:
            self.parent.selected_board_jetons.remove(self.jeton)
