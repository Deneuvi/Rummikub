
from jeton import Jeton 

class Joker(Jeton):
    """Représente un joker dans le jeu Rummikub.
    
    Hérite de la classe Jeton et modifie certains comportements pour
    représenter un joker spécifique.
    """

    def __init__(self, joker_image):
        """Initialise un joker avec l'image fournie.
        
        Paramètres :
        - joker_image : une chaîne de caractères représentant le chemin de l'image du joker.
        
        Utilise None pour le nombre car le joker ne devrait pas avoir de valeur spécifique.
        """
        super().__init__(None, 'Joker', joker_image)  # Utiliser None pour le nombre car le joker ne devrait pas avoir de valeur spécifique

    def __str__(self):
        """Renvoie une représentation sous forme de chaîne du joker.
        
        Retourne :
        - Une chaîne contenant le texte "Joker".
        """
        return "Joker"  # Affiche "Joker" à la place de "0 Joker"

    def est_joker(self):
        """Détermine si le jeton est un joker.
        
        Retourne :
        - True car cette méthode indique que c'est un joker.
        """
        return True  # Méthode pour indiquer que c'est un joker
