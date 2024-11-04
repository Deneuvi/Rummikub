class Jeton:
    """Représente un jeton dans le jeu Rummikub.
    
    Chaque jeton a un nombre, une couleur, et une image associée.
    """

    def __init__(self, nombre, couleur, image):
        """Initialise un jeton avec les attributs fournis.
        
        Paramètres :
        - nombre : un entier représentant le nombre du jeton.
        - couleur : une chaîne de caractères représentant la couleur du jeton.
        - image : une chaîne de caractères représentant le chemin de l'image du jeton.
        
        Assure que le nombre n'est jamais None.
        """
        self.nombre = nombre  # Assurez-vous que nombre n'est jamais None
        self.couleur = couleur  # Couleur du jeton (par exemple, rouge, bleu)
        self.image = image  # Chemin de l'image du jeton

    def __str__(self):
        """Renvoie une représentation sous forme de chaîne du jeton.
        
        Retourne :
        - Une chaîne contenant le nombre et la couleur du jeton.
        """
        return f"{self.nombre} {self.couleur}"

    def est_joker(self):
        """Détermine si le jeton est un joker.
        
        Retourne :
        - False car cette méthode est par défaut pour les jetons normaux.
        """
        return False  # Méthode par défaut pour les jetons normaux
