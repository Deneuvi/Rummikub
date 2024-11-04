class Jeton:
    """Représente un jeton de jeu avec un nombre, une couleur et une image associée."""
    
    def __init__(self, nombre, couleur, image):
        """
        Initialise un jeton avec un nombre, une couleur et une image.
        
        Paramètres :
        - nombre : le nombre du jeton (doit être un entier et ne doit jamais être None).
        - couleur : la couleur du jeton (chaîne de caractères).
        - image : le chemin de l'image représentant le jeton (chaîne de caractères).
        """
        self.nombre = nombre  # Assurez-vous que nombre n'est jamais None
        self.couleur = couleur  # Stocke la couleur du jeton
        self.image = image  # Stocke le chemin de l'image du jeton

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne du jeton.
        
        Retourne :
        - Une chaîne de caractères formatée avec le nombre et la couleur du jeton.
        """
        return f"{self.nombre} {self.couleur}"  # Format de la chaîne de sortie

    def est_joker(self):
        """
        Détermine si le jeton est un joker.
        
        Retourne :
        - False, car cette méthode est spécifique aux jetons normaux.
        """
        return False  # Méthode par défaut pour les jetons normaux
