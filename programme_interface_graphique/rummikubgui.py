from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QGridLayout, QLabel, QMessageBox, QHBoxLayout, QMainWindow
from jetonwidget import JetonWidget
from boardJetonwidget import BoardJetonWidget

class RummikubGUI(QMainWindow):
    def __init__(self, jeu):
        """
        Initialise l'interface graphique du jeu Rummikub.
        
        Paramètres :
        - jeu : Instance de la classe Jeu qui contient les informations de jeu.
        """
        super().__init__()
      
        self.jeu = jeu  # Instance de la classe Jeu
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
        self.setWindowTitle("Rummikub")
        self.selected_jetons = []  # Liste pour stocker les jetons sélectionnés
        self.selected_board_jetons = []  # Liste pour les jetons sélectionnés sur le plateau
        self.setGeometry(100, 100, 800, 600)
        self.etat_initial_chevalet = joueur_actuel.chevalet[:]  # État initial du chevalet du joueur
        self.etat_initial_plateaux = joueur_actuel.jetons_du_plateau[:]  # État initial des jetons du plateau
        self.etat_initial_combinaisons = [comb[:] for comb in self.jeu.plateau.combinaisons]  # État initial des combinaisons sur le plateau
        self.etat_initial_joueur = joueur_actuel.premier_jeu  # État initial de premier_jeu du joueur

        # Initialisation de la zone de plateau et du chevalet
        self.plateau_widget = QWidget()
        self.chevalet_widget = QWidget()
        self.init_ui()  # Appel à la méthode pour initialiser l'interface utilisateur
        self.a_joue_combinaison = False  # Indique si une combinaison a été jouée
        self.total_points = 0  # Points accumulés pendant le tour

    def init_ui(self):
        """
        Initialise l'interface utilisateur du jeu avec les différents layouts et widgets.
        """
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
        self.bouton_piocher.clicked.connect(self.piocher)  # Connexion de l'action à la méthode piocher
        self.bouton_jouer_combinaison = QPushButton("Jouer Combinaison")
        self.bouton_jouer_combinaison.clicked.connect(self.jouer_combinaison)  # Connexion de l'action à la méthode jouer_combinaison
        self.bouton_prendre_jeton = QPushButton("Prendre Jeton")
        self.bouton_prendre_jeton.clicked.connect(self.prendre_jeton)  # Connexion de l'action à la méthode prendre_jeton

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
        self.afficher_plateau()  # Affichage initial du plateau
        self.afficher_chevalet()  # Affichage initial du chevalet

    def afficher_plateau(self):
        """
        Affiche toutes les combinaisons sur le plateau de jeu sans écraser les combinaisons précédentes.
        """
        # Nettoyer le layout du plateau
        for i in reversed(range(self.plateau_layout.count())):
            widget_to_remove = self.plateau_layout.itemAt(i).widget()
            self.plateau_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
    
        # Ajouter chaque combinaison comme une ligne distincte dans le plateau
        for row_index, combinaison in enumerate(self.jeu.plateau.combinaisons):
            for col_index, jeton in enumerate(combinaison):
                image_label = BoardJetonWidget(jeton, self)  # Utiliser BoardJetonWidget pour chaque jeton
                self.plateau_layout.addWidget(image_label, row_index, col_index)

    def afficher_chevalet(self):
        """
        Affiche les jetons dans le chevalet du joueur actuel et les jetons pris du plateau.
        """
        joueur = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
    
        # Nettoyer le layout du chevalet
        for i in reversed(range(self.chevalet_layout.count())):
            widget_to_remove = self.chevalet_layout.itemAt(i).widget()
            self.chevalet_layout.removeWidget(widget_to_remove)
            widget_to_remove.deleteLater()
    
        # Afficher chaque jeton du chevalet en tant que JetonWidget
        for jeton in joueur.chevalet:
            jeton_widget = JetonWidget(jeton, self)  # Utiliser JetonWidget
            self.chevalet_layout.addWidget(jeton_widget)
    
        # Afficher les jetons pris du plateau
        print(f"Jetons pris par {joueur.nom}: {joueur.jetons_du_plateau}")  # Afficher les jetons pris
        for jeton in joueur.jetons_du_plateau:
            jeton_widget = JetonWidget(jeton, self)  # Utiliser JetonWidget pour les jetons pris
            self.chevalet_layout.addWidget(jeton_widget)  # Ajouter à la même interface graphique
  
    def piocher(self):
        """Action du bouton 'Piocher'."""
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]

        print (self.etat_initial_combinaisons)
        while True:
            print("Chevalet:\n", joueur_actuel.afficher_chevalet())
            print("Plateau :")
            self.jeu.plateau.afficher()
    
            if joueur_actuel.chevalet != self.etat_initial_chevalet or joueur_actuel.jetons_du_plateau != self.etat_initial_plateaux :
                if  (self.total_points < 30 and joueur_actuel.premier_jeu == True ) or joueur_actuel.jetons_du_plateau!=[]:
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
                            jeton = self.jeu.tas_jetons.pop()
                            joueur_actuel.piocher(jeton)
                            print(f"{joueur_actuel.nom} a pioché un jeton pour finir son tour : {jeton}")
                        break  # Sortir de la boucle
                    else:
                        # Lorsque l'utilisateur choisit "Non", nous sortons simplement de la condition.
                        print("Tour annulé. Vous pouvez continuer à jouer.")
                        return
                else :
                    joueur_actuel.premier_jeu = False 
                    break
    
            # Vérifier s'il y a des jetons à piocher
            if self.jeu.tas_jetons:
                jeton = self.jeu.tas_jetons.pop()
                joueur_actuel.piocher(jeton)
                self.afficher_chevalet()
                print(f"{joueur_actuel.nom} a pioché : {jeton}")
                break
            else:
                self.jeu.tentatives_sans_jeton += 1
                print("Il n'y a plus de jetons à piocher.")
                break
    
        # Réinitialiser la sélection après la pioche
        self.reset_selection()
    
        # Passer au tour suivant
        self.jeu.tour += 1
        self.check_end_game()
        joueur_futur = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
        self.etat_initial_chevalet = joueur_futur.chevalet[:]
        self.etat_initial_plateaux = joueur_futur.jetons_du_plateau[:]
        self.etat_initial_combinaisons = [comb[:] for comb in self.jeu.plateau.combinaisons]
        self.etat_initial_joueur = joueur_futur.premier_jeu
        self.a_joue_combinaison = False
        self.total_points = 0  # Réinitialiser les points accumulés
        self.afficher_chevalet()
    
    
    def check_end_game(self):
       """Vérifie si un joueur a terminé la partie en n'ayant plus de jetons."""
       for joueur in self.jeu.joueurs:
           if not joueur.chevalet and not joueur.jetons_du_plateau:
               QMessageBox.information(self, "Fin de Partie", f"{joueur.nom} a gagné la partie !")
               self.close()  # Ferme la fenêtre pour terminer le jeu
               return True
       return False

    
    def update_status(self):
        """Met à jour l'affichage du statut du joueur actuel."""
        print(f"C'est le tour de {self.joueur_actuel.nom}!")
        print("Chevalet:\n", self.joueur_actuel.afficher_chevalet())
        print("Plateau :")
        self.jeu.plateau.afficher()
            
    def jouer_combinaison(self):
      
        """Action du bouton 'Jouer Combinaison'."""
        joueur_actuel = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
        etat_initial_chevalet = joueur_actuel.chevalet[:]
        etat_initial_combinaisons = [comb[:] for comb in self.jeu.plateau.combinaisons]
    
        # Récupérer les jetons sélectionnés pour la combinaison
        combinaison = list(self.selected_jetons)  # Clone pour éviter la référence partagée
        print(combinaison)
    
        if self.jeu.ajouter_combinaison(combinaison):  # Ajoute la combinaison sans partager de référence
            score_combinaison = self.jeu.calculer_score_combinaison(combinaison)
            self.total_points += score_combinaison
            self.jeu.tentatives_sans_jeton = 0
            self.a_joue_combinaison = True
            self.afficher_plateau()  # Réafficher le plateau après ajout
            self.afficher_chevalet()
            self.reset_selection()
    
            if joueur_actuel.premier_jeu and self.total_points >= 30:

                print(f"{joueur_actuel.nom} a atteint 30 points et peut maintenant prendre des jetons du plateau.")
            print(f"Points cumulés : {self.total_points}")
    
        else:
            print("Combinaison invalide !")
            joueur_actuel.chevalet = etat_initial_chevalet[:]
            self.jeu.plateau.combinaisons = etat_initial_combinaisons[:]
            self.reset_selection()
            self.total_points = 0
        
    

    
    
    def prendre_jeton(self):
        """Action du bouton 'Prendre Jeton'."""
        joueur = self.jeu.joueurs[self.jeu.tour % len(self.jeu.joueurs)]
        
        if joueur.premier_jeu:
            print("Vous ne pouvez pas prendre de jetons avant d'avoir joué une combinaison.")
            return
    
        if self.selected_board_jetons:
            for jeton in self.selected_board_jetons:
                for comb_index, combinaison in enumerate(self.jeu.plateau.combinaisons):
                    if jeton in combinaison:
                        jeton_index = combinaison.index(jeton)
                        if self.jeu.plateau.prendre_jeton(comb_index, jeton_index, joueur):
                            print(f"{joueur.nom} a pris le jeton : {jeton}")
                        else:
                            print("Erreur lors de la prise de jeton.")
                        break  # Sortir après avoir traité le jeton
            self.afficher_chevalet()  # Mettre à jour l'affichage de la main du joueur
            self.afficher_plateau()    # Mettre à jour l'affichage du plateau
            self.reset_selection()      # Réinitialiser toute sélection
        else:
            print("Aucun jeton sélectionné pour prise.")
            self.reset_selection()

    def reset_selection(self):
        """Réinitialise la sélection de jetons dans le chevalet et sur le plateau."""
        # Vider les listes de sélection
        self.selected_jetons.clear()
        self.selected_board_jetons.clear()
    
        # Réinitialiser l'apparence des jetons sélectionnés dans le chevalet
        for i in range(self.chevalet_layout.count()):
            widget = self.chevalet_layout.itemAt(i).widget()
            if isinstance(widget, JetonWidget):  # Vérifie que c'est bien un JetonWidget
                widget.selected = False
                widget.setStyleSheet("border: 1px solid black;")
    
        # Réinitialiser l'apparence des jetons sélectionnés sur le plateau
        for i in range(self.plateau_layout.count()):
            widget = self.plateau_layout.itemAt(i).widget()
            if isinstance(widget, BoardJetonWidget):  # Vérifie que c'est bien un BoardJetonWidget
                widget.selected = False
                widget.setStyleSheet("border: 1px solid black;")
                
