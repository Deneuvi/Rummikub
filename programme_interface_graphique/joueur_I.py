class Joueur:
    """Représente un joueur dans le jeu, avec un nom, un chevalet et des jetons pris depuis le plateau."""

    def __init__(self, nom):
        """
        Initialise un joueur avec un nom et des collections de jetons.
        
        Paramètres :
        - nom : le nom du joueur.
        """
        self.nom = nom  # Stocke le nom du joueur
        self.chevalet = []  # Liste pour stocker les jetons du joueur
        self.jetons_du_plateau = []  # Liste pour les jetons pris depuis le plateau
        self.premier_jeu = True  # Indique si c'est le premier tour du joueur

    def piocher(self, jeton, depuis_plateau=False):
        """
        Permet au joueur de piocher un jeton, soit du tas de jetons, soit du plateau.
        
        Paramètres :
        - jeton : le jeton à piocher.
        - depuis_plateau : booléen indiquant si le jeton vient du plateau.
        """
        if depuis_plateau:
            self.jetons_du_plateau.append(jeton)  # Ajoute le jeton à la liste des jetons pris du plateau
            print(f"{self.nom} a pris un jeton du plateau : {jeton}")  # Affiche un message de prise du jeton
        else:
            self.chevalet.append(jeton)  # Ajoute le jeton au chevalet du joueur

    def poser_jetons(self, jetons):
        """
        Permet au joueur de poser des jetons sur le plateau.
        
        Paramètres :
        - jetons : liste de jetons à poser.
        """
        for jeton in jetons:
            if jeton in self.chevalet:
                self.chevalet.remove(jeton)  # Retire le jeton du chevalet
            if jeton in self.jetons_du_plateau:
                self.jetons_du_plateau.remove(jeton)  # Retire le jeton de la liste des jetons pris du plateau

    def ajouter_jeton(self, jeton):
        """Ajoute un jeton au chevalet."""
        print(f"Ajout du jeton {jeton} au chevalet de {self.nom}.")  # Affiche un message d'ajout
        self.chevalet.append(jeton)  # Ajoute le jeton au chevalet

    def afficher_chevalet(self):
        """
        Affiche les jetons du chevalet et ceux pris du plateau.
        
        Retourne :
        - Une chaîne représentant le chevalet et les jetons pris du plateau.
        """
        col_size = 4  # Nombre de jetons à afficher par ligne
        chevalet_str = ["Jetons du chevalet :"]  # Initialise la liste des chaînes pour l'affichage
        
        # Affichage du chevalet
        for i in range(0, len(self.chevalet), col_size):
            ligne = ' | '.join(f"{chr(65 + j)}: {self.chevalet[j]}" for j in range(i, min(i + col_size, len(self.chevalet))))
            chevalet_str.append(ligne)  # Ajoute chaque ligne de jetons à la chaîne d'affichage
        
        # Affichage des jetons pris du plateau
        chevalet_str.append("\nJetons pris du plateau :")
        for jeton in self.jetons_du_plateau:
            chevalet_str.append(f" - {jeton}")  # Ajoute chaque jeton pris à la chaîne d'affichage
        
        return '\n'.join(chevalet_str)  # Retourne la chaîne d'affichage complète
