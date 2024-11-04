from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap

class JetonWidget(QLabel):
    def __init__(self, jeton, parent):
        """
        Initialise un widget pour afficher un jeton spécifique dans l'interface graphique.

        Paramètres :
        - jeton : l'objet Jeton contenant les données du jeton (comme l'image).
        - parent : le widget parent auquel ce widget est associé.
        """
        super().__init__(parent)  # Appel au constructeur de la classe QLabel
        self.jeton = jeton  # Stocker le jeton associé au widget
        self.parent = parent  # Stocker la référence au widget parent pour interaction
        self.setPixmap(QPixmap(jeton.image))  # Définir l'image du jeton
        self.setFixedSize(60, 60)  # Fixer la taille du widget à 60x60 pixels
        self.setScaledContents(True)  # Redimensionner l'image pour remplir le widget
        self.setStyleSheet("border: 1px solid black;")  # Appliquer un style de bordure par défaut
        self.selected = False  # Initialiser l'état de sélection du jeton à "non sélectionné"

    def mousePressEvent(self, event):
        """
        Gère l'événement de clic de souris sur le widget.

        Cette méthode bascule l'état de sélection du jeton et met à jour l'apparence du widget.
        Elle ajoute ou retire également le jeton de la liste des jetons sélectionnés dans le parent.
        """
        # Basculer l'état de sélection (True si non sélectionné, False si déjà sélectionné)
        self.selected = not self.selected
        
        # Mettre à jour la bordure du widget en fonction de l'état de sélection
        self.setStyleSheet("border: 3px solid green;" if self.selected else "border: 1px solid black;")
        
        # Ajouter ou retirer le jeton de la liste selected_jetons dans le GUI parent
        if self.selected:
            self.parent.selected_jetons.append(self.jeton)  # Ajouter le jeton si sélectionné
        else:
            self.parent.selected_jetons.remove(self.jeton)  # Retirer le jeton si désélectionné
