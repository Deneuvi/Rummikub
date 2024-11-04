from jeton_I import Jeton 

class Joker(Jeton):
    """Représente un joker dans le jeu, hérite de la classe Jeton."""
    
    def __init__(self, joker_image):
        """
        Initialise un joker avec une image spécifique.
        
        Paramètres :
        - joker_image : le chemin de l'image représentant le joker.
        """
        super().__init__(None, 'Joker', joker_image)  # Utiliser None pour le nombre car le joker ne devrait pas avoir de valeur spécifique

    def __str__(self):
        """
        Renvoie une représentation sous forme de chaîne du joker.
        
        Retourne :
        - "Joker" pour indiquer qu'il s'agit d'un joker.
        """
        return "Joker"  # Affiche "Joker" à la place de "0 Joker"

    def est_joker(self):
        """
        Indique que l'objet est un joker.
        
        Retourne :
        - True, car cette méthode confirme que c'est un joker.
        """
        return True  # Méthode pour indiquer que c'est un joker
