from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class BoardJetonWidget(QLabel):
    """Widget for displaying a board tile that can be selected."""
    
    def __init__(self, jeton, parent):
        """
        Initialise un widget pour afficher un jeton sur le plateau.
        
        Paramètres :
        - jeton : l'objet jeton à afficher dans le widget.
        - parent : le widget parent qui contient ce widget.
        """
        super().__init__(parent)  # Appelle le constructeur de la classe parente QLabel
        self.jeton = jeton  # Stocke l'objet jeton
        self.parent = parent  # Stocke la référence au widget parent
        self.setPixmap(QPixmap(jeton.image))  # Définit l'image du jeton à afficher
        self.setFixedSize(60, 60)  # Définit la taille fixe du widget
        self.setScaledContents(True)  # Permet de redimensionner l'image pour s'adapter au widget
        self.setStyleSheet("border: 1px solid black;")  # Définit le style de la bordure du widget
        self.selected = False  # Indique si le jeton est sélectionné

    def mousePressEvent(self, event):
        """
        Gère l'événement de pression de la souris pour sélectionner ou désélectionner le jeton.
        
        Paramètres :
        - event : l'événement de la souris, qui contient des informations sur la pression de la souris.
        """
        self.selected = not self.selected  # Change l'état de sélection du jeton
        self.setStyleSheet("border: 3px solid blue;" if self.selected else "border: 1px solid black;")  # Met à jour le style de la bordure selon l'état de sélection
        
        # Update selected board jetons in parent GUI
        if self.selected:  # Si le jeton est sélectionné
            self.parent.selected_board_jetons.append(self.jeton)  # Ajoute le jeton à la liste des jetons sélectionnés dans le widget parent
        else:  # Si le jeton est désélectionné
            self.parent.selected_board_jetons.remove(self.jeton)  # Retire le jeton de la liste des jetons sélectionnés
