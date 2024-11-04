class Joueur:
    def __init__(self, nom):
        self.nom = nom  # Nom du joueur
        self.chevalet = []  # Liste de jetons que le joueur a en main
        self.jetons_du_plateau = []  # Liste pour stocker les jetons pris depuis le plateau
        self.premier_jeu = True  # Indicateur pour savoir si le joueur a déjà effectué son premier jeu

    def piocher(self, jeton, depuis_plateau=False):
        """
        Ajoute un jeton soit au chevalet, soit aux jetons pris depuis le plateau, selon l'origine.
        
        Paramètres :
        - jeton : le jeton à ajouter.
        - depuis_plateau : un booléen indiquant si le jeton provient du plateau.
        """
        if depuis_plateau:
            # Ajoute le jeton à la liste des jetons pris depuis le plateau
            self.jetons_du_plateau.append(jeton)
            print(f"{self.nom} a pris un jeton du plateau : {jeton}")
        else:
            # Ajoute le jeton au chevalet
            self.chevalet.append(jeton)

    def poser_jetons(self, jetons):
        """
        Retire des jetons du chevalet ou de la liste de jetons pris depuis le plateau.
        
        Paramètre :
        - jetons : liste des jetons que le joueur souhaite poser.
        """
        for jeton in jetons:
            # Retire le jeton du chevalet s'il y est présent
            if jeton in self.chevalet:
                self.chevalet.remove(jeton)
            # Retire le jeton de la liste des jetons pris depuis le plateau s'il y est présent
            if jeton in self.jetons_du_plateau:
                self.jetons_du_plateau.remove(jeton)

    def ajouter_jeton(self, jeton):
        """
        Ajoute un jeton au chevalet du joueur.
        
        Paramètre :
        - jeton : le jeton à ajouter au chevalet.
        """
        print(f"Ajout du jeton {jeton} au chevalet de {self.nom}.")
        self.chevalet.append(jeton)

    def afficher_chevalet(self):
        """
        Renvoie une chaîne de caractères représentant le chevalet du joueur, avec les jetons
        du chevalet affichés en colonnes de taille fixe et les jetons pris du plateau affichés séparément.
        """
        col_size = 4  # Nombre de jetons à afficher par ligne
        chevalet_str = ["Jetons du chevalet :"]

        # Boucle pour afficher le chevalet par groupes de `col_size` jetons
        for i in range(0, len(self.chevalet), col_size):
            ligne = ' | '.join(
                f"{chr(65 + j)}: {self.chevalet[j]}"  # Associe chaque jeton à une lettre (A, B, C, ...)
                for j in range(i, min(i + col_size, len(self.chevalet)))
            )
            chevalet_str.append(ligne)

        # Ajoute les jetons pris depuis le plateau, listés en dessous
        chevalet_str.append("\nJetons pris du plateau :")
        for jeton in self.jetons_du_plateau:
            chevalet_str.append(f" - {jeton}")

        # Retourne la chaîne de caractères complète pour affichage
        return '\n'.join(chevalet_str)
