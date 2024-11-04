from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QMessageBox, QHBoxLayout, QMainWindow
from jetonwidget import JetonWidget
from boardJetonwidget import BoardJetonWidget

class RummikubGUI(QMainWindow):
    """Classe représentant l'interface graphique du jeu Rummikub."""
    
    def __init__(self, jeu):
        """Initialise la fenêtre principale du jeu Rummikub.
        
        Args:
            jeu (Jeu): Instance de la classe Jeu, contenant les données du jeu.
        """
        super().__init__()
      
        self.jeu = jeu  # Instance de la classe Jeu
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
        self.setWindowTitle("Rummikub")
        self.selected_jetons = []  # Liste pour stocker les jetons sélectionnés
        self.selected_board_jetons = []  # Liste pour les jetons sélectionnés sur le plateau
        self.setGeometry(100, 100, 800, 600)
        self.etat_initial_chevalet = joueur_actuel.chevalet[:]  # État initial du chevalet
        self.etat_initial_plateaux = joueur_actuel.jetons_du_plateau[:]  # État initial des jetons du plateau
        self.etat_initial_combinaisons = [comb[:] for comb in self.jeu.plateau.combinaisons]  # État initial des combinaisons
        self.etat_initial_joueur = joueur_actuel.premier_jeu  # État initial du joueur

        # Initialisation de la zone de plateau et du chevalet
        self.plateau_widget = QWidget()  # Widget pour le plateau
        self.chevalet_widget = QWidget()  # Widget pour le chevalet
        self.init_ui()  # Appelle la méthode d'initialisation de l'interface
        self.a_joue_combinaison = False  # Indique si une combinaison a été jouée
        self.total_points = 0  # Points accumulés pendant le tour

    def init_ui(self):
        """Configure l'interface utilisateur avec les layouts et les widgets."""
        # Layout principal
        layout_principal = QVBoxLayout()

        # Layout pour le plateau de jeu
        self.plateau_layout = QGridLayout()
        self.plateau_widget.setLayout(self.plateau_layout)
        layout_principal.addWidget(QLabel("Plateau de jeu:"))
        layout_principal.addWidget(self.plateau_widget)

        # Layout pour le chevalet du joueur
        self.chevalet_layout = QHBoxLayout()
        self.chevalet_widget.setLayout(self.chevalet_layout)
        layout_principal.addWidget(QLabel("Chevalet du joueur:"))
        layout_principal.addWidget(self.chevalet_widget)

        # Boutons de contrôle
        self.bouton_piocher = QPushButton("Piocher")
        self.bouton_piocher.clicked.connect(self.piocher)  # Connecte le bouton à l'action de pioche
        self.bouton_jouer_combinaison = QPushButton("Jouer Combinaison")
        self.bouton_jouer_combinaison.clicked.connect(self.jouer_combinaison)  # Connecte le bouton à l'action de jouer une combinaison
        self.bouton_prendre_jeton = QPushButton("Prendre Jeton")
        self.bouton_prendre_jeton.clicked.connect(self.prendre_jeton)  # Connecte le bouton à l'action de prendre un jeton

        # Ajout des boutons au layout
        control_layout = QHBoxLayout()
        control_layout.addWidget(self.bouton_piocher)
        control_layout.addWidget(self.bouton_jouer_combinaison)
        control_layout.addWidget(self.bouton_prendre_jeton)
        layout_principal.addLayout(control_layout)

        # Configurer le widget central
        central_widget = QWidget()
        central_widget.setLayout(layout_principal)
        self.setCentralWidget(central_widget)

        # Afficher le plateau et le chevalet
        self.afficher_plateau()  # Méthode pour afficher le plateau
        self.afficher_chevalet()  # Méthode pour afficher le chevalet

    def afficher_plateau(self):
        """Affiche toutes les combinaisons sur le plateau de jeu sans écraser les combinaisons précédentes."""
        # Nettoyer le layout du plateau
        for i in reversed(range(self.plateau_layout.count())):
            widget_to_remove = self.plateau_layout.itemAt(i).widget()  # Récupère le widget à supprimer
            self.plateau_layout.removeWidget(widget_to_remove)  # Retire le widget du layout
            widget_to_remove.deleteLater()  # Supprime le widget

        # Ajouter chaque combinaison comme une ligne distincte dans le plateau
        for row_index, combinaison in enumerate(self.jeu.plateau.combinaisons):
            for col_index, jeton in enumerate(combinaison):
                image_label = BoardJetonWidget(jeton, self)  # Utiliser BoardJetonWidget pour chaque jeton
                self.plateau_layout.addWidget(image_label, row_index, col_index)  # Ajoute le widget au layout

    def afficher_chevalet(self):
        """Affiche les jetons dans le chevalet du joueur actuel et les jetons pris du plateau."""
        joueur = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]  # Récupère le joueur actuel

        # Nettoyer le layout du chevalet
        for i in reversed(range(self.chevalet_layout.count())):
            widget_to_remove = self.chevalet_layout.itemAt(i).widget()  # Récupère le widget à supprimer
            self.chevalet_layout.removeWidget(widget_to_remove)  # Retire le widget du layout
            widget_to_remove.deleteLater()  # Supprime le widget

        # Afficher chaque jeton du chevalet en tant que JetonWidget
        for jeton in joueur.chevalet:
            jeton_widget = JetonWidget(jeton, self)  # Utiliser JetonWidget
            self.chevalet_layout.addWidget(jeton_widget)  # Ajoute le widget au layout

        # Afficher les jetons pris du plateau
        print(f"Jetons pris par {joueur.nom}: {joueur.jetons_du_plateau}")  # Afficher les jetons pris
        for jeton in joueur.jetons_du_plateau:
            jeton_widget = JetonWidget(jeton, self)  # Utiliser JetonWidget pour les jetons pris
            self.chevalet_layout.addWidget(jeton_widget)  # Ajouter à la même interface graphique

    def piocher(self):
        """Action du bouton 'Piocher'."""
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]  # Récupère le joueur actuel

        print(self.etat_initial_combinaisons)  # Affiche l'état initial des combinaisons
        while True:
            print("Chevalet:\n", joueur_actuel.afficher_chevalet())  # Affiche le chevalet du joueur
            print("Plateau :")
            self.jeu.plateau.afficher()  # Affiche l'état du plateau

            # Vérifie les conditions pour terminer le tour
            if joueur_actuel.chevalet != self.etat_initial_chevalet or joueur_actuel.jetons_du_plateau != self.etat_initial_plateaux:
                if (self.total_points < 30 and joueur_actuel.premier_jeu) or joueur_actuel.jetons_du_plateau:
                    confirmation = QMessageBox.question(
                        self, "Confirmation",
                        "Vous n'avez pas atteint 30 points ou vous avez encore des jetons pris du plateau. Voulez-vous terminer le tour ?",
                        QMessageBox.Yes | QMessageBox.No,
                        QMessageBox.No
                    )

                    if confirmation == QMessageBox.Yes:
                        print(f"{joueur_actuel.nom} a choisi de terminer son tour.")
                        # Réinitialiser les états comme avant
                        joueur_actuel.chevalet = self.etat_initial_chevalet
                        joueur_actuel.jetons_du_plateau = self.etat_initial_plateaux
                        self.jeu.plateau.combinaisons = self.etat_initial_combinaisons
                        # Mettre à jour le plateau pour refléter les états réinitialisés
                        self.afficher_plateau()
                        joueur_actuel.premier_jeu = self.etat_initial_joueur
                        if self.jeu.tas_jetons:
                            jeton = self.jeu.tas_jetons.pop()  # Pioche un jeton si disponible
                            joueur_actuel.piocher(jeton)  # Ajoute le jeton au joueur
                            print(f"{joueur_actuel.nom} a pioché un jeton pour finir son tour : {jeton}")
                        break  # Sortir de la boucle
                    else:
                        print("Tour annulé. Vous pouvez continuer à jouer.")
                        return
                else:
                    joueur_actuel.premier_jeu = False  # Marque que le premier jeu a été joué
                    break

            # Vérifie s'il y a des jetons à piocher
            if self.jeu.tas_jetons:
                jeton = self.jeu.tas_jetons.pop()  # Pioche un jeton
                joueur_actuel.piocher(jeton)  # Ajoute le jeton au chevalet
                self.afficher_chevalet()  # Met à jour l'affichage du chevalet
                break
            else:
                QMessageBox.warning(self, "Alerte", "Il n'y a plus de jetons à piocher.")  # Alerte si le tas est vide
                break

    def prendre_jeton(self):
        """Action pour prendre un jeton du plateau."""
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]  # Récupère le joueur actuel
        if self.selected_board_jetons:
            for jeton in self.selected_board_jetons:
                joueur_actuel.jetons_du_plateau.append(jeton)  # Ajoute le jeton du plateau au chevalet
                self.jeu.plateau.remove_jeton(jeton)  # Retire le jeton du plateau
                print(f"{joueur_actuel.nom} a pris le jeton : {jeton}")

            self.afficher_chevalet()  # Met à jour l'affichage du chevalet
            self.afficher_plateau()  # Met à jour l'affichage du plateau
            self.selected_board_jetons.clear()  # Réinitialise la liste des jetons sélectionnés du plateau

    def jouer_combinaison(self):
        """Action pour jouer une combinaison de jetons."""
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]  # Récupère le joueur actuel
        if self.selected_jetons:
            print(f"Jetons sélectionnés pour la combinaison : {self.selected_jetons}")  # Affiche les jetons sélectionnés
            if joueur_actuel.peut_jouer_combinaison(self.selected_jetons):
                self.a_joue_combinaison = True  # Indique qu'une combinaison a été jouée
                self.total_points += joueur_actuel.calculer_points_combinaison(self.selected_jetons)  # Ajoute les points de la combinaison
                print(f"{joueur_actuel.nom} a joué une combinaison de {len(self.selected_jetons)} jetons, total de points : {self.total_points}")
                joueur_actuel.jouer_combinaison(self.selected_jetons)  # Joue la combinaison
                self.afficher_plateau()  # Met à jour l'affichage du plateau
                self.selected_jetons.clear()  # Réinitialise la liste des jetons sélectionnés
            else:
                QMessageBox.warning(self, "Erreur", "Combinaison invalide !")  # Alerte si la combinaison est invalide

    def keyPressEvent(self, event):
        """Gère les événements de touche pour sélectionner/désélectionner des jetons.
        
        Paramètre:
        - event : instance de l'objet QEvent qui contient des informations sur l'événement de souris.
        
        """
        if event.key() == Qt.Key_Delete:  # Vérifie si la touche 'Suppr' est enfoncée
            # Désélectionner tous les jetons si 'Suppr' est pressé
            self.selected_jetons.clear()
            self.selected_board_jetons.clear()  # Réinitialise la sélection sur le plateau
            print("Tous les jetons ont été désélectionnés.")

        # Si d'autres touches sont nécessaires pour l'interface, elles peuvent être ajoutées ici

    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre.
        
         Paramètre:
        - event : instance de l'objet QEvent qui contient des informations sur l'événement de souris.
        
        """
        confirmation = QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment quitter le jeu ?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if confirmation == QMessageBox.Yes:
            event.accept()  # Accepte la fermeture de la fenêtre
        else:
            event.ignore()  # Ignore la fermeture de la fenêtre
