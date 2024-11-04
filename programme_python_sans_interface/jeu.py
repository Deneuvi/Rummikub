from plateau import Plateau 
from jeton import Jeton 
from joker import Joker 
import random


class Jeu:
    """Représente le jeu Rummikub, gérant les joueurs, les jetons et le plateau."""
    
    def __init__(self):
        """Initialise une nouvelle partie de Rummikub avec les joueurs, le tas de jetons, le plateau, et d'autres paramètres.
        
        Les attributs incluent :
        - joueurs : une liste de joueurs participant au jeu.
        - tas_jetons : le tas de jetons à distribuer aux joueurs.
        - plateau : un objet de type Plateau pour gérer les combinaisons posées.
        - tour : l'indice du tour actuel.
        - tentatives_sans_jeton : le nombre de tentatives sans jeton à piocher.
        """
        self.joueurs = []
        self.tas_jetons = self.creer_tas_jetons()
        self.plateau = Plateau()  # Initialisez ici en tant qu'objet de type Plateau
        self.tour = 0
        self.tentatives_sans_jeton = 0

    def creer_tas_jetons(self):
        """Crée le tas de jetons pour le jeu, incluant les jetons de couleurs et les jokers.
        
        Retourne :
        - Une liste de jetons mélangés, prêts à être distribués aux joueurs.
        """
        couleurs = ['Rouge', 'Bleu', 'Vert', 'Jaune']
        jetons = []
        # Créer les jetons avec les chemins d'image appropriés
        for couleur in couleurs:
            for nombre in range(1, 14):
                image = f"{couleur}/{nombre}_{couleur[0]}.PNG"  # Chemin d'image formaté
                jetons.append(Jeton(nombre, couleur, image))
                jetons.append(Jeton(nombre, couleur, image)) 
        
        joker_images = ["joker/joker_1.PNG", "joker/joker_2.PNG"]
        jetons += [Joker(image) for image in joker_images] 
        random.shuffle(jetons)
        return jetons

    def ajouter_joueur(self, joueur):
        """Ajoute un joueur à la liste des joueurs du jeu.
        
        Paramètres :
        - joueur : l'objet joueur à ajouter.
        """
        self.joueurs.append(joueur)

    def distribuer_jetons(self, nombre_jetons):
        """Distribue un certain nombre de jetons à chaque joueur.
        
        Paramètres :
        - nombre_jetons : le nombre de jetons à distribuer à chaque joueur.
        """
        for joueur in self.joueurs:
            for _ in range(nombre_jetons):
                if self.tas_jetons:
                    jeton = self.tas_jetons.pop()
                    joueur.piocher(jeton)

    def determine_depart(self):
        """Détermine quel joueur commence la partie, en fonction de la valeur du jeton pioché.
        
        Retourne :
        - Le joueur qui commence la partie.
        """
        max_jeton = -1
        premier_joueur = None
        for joueur in self.joueurs:
            jeton = self.tas_jetons.pop()
            if jeton.nombre > max_jeton:
                max_jeton = jeton.nombre
                premier_joueur = joueur
            joueur.piocher(jeton)
        return premier_joueur

    def ajouter_combinaison(self, combinaison):
        """Ajoute une combinaison de jetons au plateau si elle est valide.
        
        Paramètres :
        - combinaison : la liste de jetons à ajouter au plateau.
        
        Retourne :
        - True si la combinaison a été ajoutée avec succès, False sinon.
        """
        if self.verifier_combinaison(combinaison):
            self.plateau.ajouter_combinaison(combinaison)
            joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]
            joueur_actuel.poser_jetons(combinaison)
            return True
        else:
            print("Combinaison invalide !")
            return False

    def verifier_combinaison(self, combinaison):
        """Vérifie si une combinaison de jetons est valide selon les règles du jeu.
        
        Une combinaison peut être une suite (même couleur) ou une série (même nombre).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est valide, False sinon.
        """
        if len(combinaison) < 3:
            return False
        
        # Séparer les jokers et les jetons normaux
        jokers = [jeton for jeton in combinaison if isinstance(jeton, Joker)]
        non_jokers = [jeton for jeton in combinaison if isinstance(jeton, Jeton) and not jeton.est_joker()]
    
        # Cas spécial : 2 jokers et 1 seul jeton
        if len(jokers) == 2 and len(non_jokers) == 1:
            return True  # Les deux jokers peuvent être considérés comme des couleurs manquantes pour une série
    
        # Trier les jetons non-jokers par nombre pour comparer en ordre croissant
        non_jokers.sort(key=lambda jeton: jeton.nombre)
        couleurs = {jeton.couleur for jeton in non_jokers}
        nombres = [jeton.nombre for jeton in non_jokers]

        # Vérification des suites
        if len(couleurs) == 1:  # Si c'est une suite
            jokers_utilises = 0  # Compteur pour les jokers utilisés
            for i in range(len(nombres) - 1):
                # Vérifie les suites avec possibilité de joker
                ecart = nombres[i + 1] - nombres[i]  # Calcul de l'écart
                print(ecart)
                if ecart == 2:  # Si l'écart est de 2, on peut utiliser un joker
                    jokers_utilises += 1
                if ecart == 3:  # Si l'écart est de 3, on peut utiliser un joker
                    jokers_utilises += 2
                elif ecart > 4:  # Si l'écart est supérieur à 4, c'est impossible
                    return False
                print(len(jokers))
                # Vérifie si le nombre de jokers utilisés ne dépasse pas le nombre de jokers disponibles
                if jokers_utilises > len(jokers):
                    return False
    
            return True
    
        elif len(set(nombres)) == 1:  # Si c'est une série
            # Vérification si le nombre de couleurs est suffisant avec les jokers
            # Vérification des couleurs uniques
            if len(couleurs) == len(non_jokers):
                return len(couleurs) + len(jokers) >= 3
            
        return False

    def joueur_gagnant(self):
        """Détermine si un joueur a gagné en n'ayant plus de jetons.
        
        Retourne :
        - L'objet joueur qui a gagné, ou None si aucun joueur n'a gagné.
        """
        for joueur in self.joueurs:
            if not joueur.chevalet:
                return joueur
        return None

    def joueur_avec_moins_jetons(self):
        """Détermine le joueur ayant le moins de jetons restants dans son chevalet.
        
        Retourne :
        - L'objet joueur avec le moins de jetons.
        """
        return min(self.joueurs, key=lambda joueur: len(joueur.chevalet))

    def jouer_tour(self):
        """Joue un tour pour le joueur actuel, incluant la logique de prise et de pose des jetons.
        
        Retourne :
        - True si le tour a été joué avec succès, False si la partie est terminée.
        """
        joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]
        print(f"C'est le tour de {joueur_actuel.nom}!")
    
        # Sauvegarder l'état initial du plateau et de la main du joueur
        etat_initial_chevalet = joueur_actuel.chevalet[:]
        etat_initial_plateaux = joueur_actuel.jetons_du_plateau[:]
        etat_initial_combinaisons = [comb[:] for comb in self.plateau.combinaisons]
        etat_initial_joueur = joueur_actuel.premier_jeu
    
        # Vérification de fin de partie pour le joueur actuel
        if not joueur_actuel.chevalet and not joueur_actuel.jetons_du_plateau:
            print(f"{joueur_actuel.nom} a gagné la partie en n'ayant plus de jetons !")
            return False  # Indique que la partie est terminée
    
        # Logique de tour restante
        combinaisons_posees = []  # Combinaisons que le joueur pose ce tour-ci
        jetons_pris = []  # Jetons pris du plateau
        total_points = 0  # Points accumulés pendant le tour
        a_joue_combinaison = False  # Indique si une combinaison a été jouée
    
        while True:
            print("Chevalet:\n", joueur_actuel.afficher_chevalet())
            print("Plateau :")
            self.plateau.afficher()
    
            # Processus de prise de jetons
            jeton = joueur_actuel.prendre_jeton()
            if jeton:
                print(f"{joueur_actuel.nom} a pris le jeton {jeton}")
                total_points += jeton.nombre  # Ajout de la valeur du jeton aux points totaux
    
            if total_points >= 30 and not a_joue_combinaison:
                print(f"{joueur_actuel.nom} a déjà atteint 30 points.")
                break  # Quitte la boucle si 30 points sont atteints et aucune combinaison n'a été jouée
    
            # Logique pour poser une combinaison
            choix_combinaison = input("Voulez-vous poser une combinaison? (o/n): ")
            if choix_combinaison.lower() == "o":
                combinaison_str = input("Entrez les indices des jetons à poser séparés par des espaces : ")
                indices = [int(i) for i in combinaison_str.split()]
                combinaison_a_poser = [joueur_actuel.chevalet[i] for i in indices]
    
                if self.ajouter_combinaison(combinaison_a_poser):
                    a_joue_combinaison = True
                    combinaisons_posees.append(combinaison_a_poser)
                else:
                    print("Échec lors de la pose de la combinaison.")
    
            # Logique pour piocher un jeton si aucune combinaison n'a été posée
            choix = input("Voulez-vous piocher un jeton? (o/n): ")
            if choix.lower() == "o":
                jeton_pris = self.prendre_jeton(joueur_actuel)
                if jeton_pris:
                    print(f"{joueur_actuel.nom} a pris le jeton {jeton_pris}.")
    
            if total_points >= 30 and a_joue_combinaison:
                print(f"{joueur_actuel.nom} a terminé son tour avec succès.")
                break  # Quitte la boucle si le tour est terminé avec succès

            if not jeton and not a_joue_combinaison:
                self.tentatives_sans_jeton += 1
    
            if self.tentatives_sans_jeton >= 3:
                print(f"{joueur_actuel.nom} ne peut plus piocher de jetons.")
                break  # Quitte la boucle si le joueur ne peut plus piocher de jetons
    
        # Mise à jour de l'état final du joueur
        joueur_actuel.jetons_du_plateau.extend(joueur_actuel.chevalet)
        joueur_actuel.chevalet = []  # Réinitialise le chevalet du joueur
        self.tour += 1  # Passe au tour suivant
        return True

    def prendre_jeton(self, joueur):
        """Permet à un joueur de piocher un jeton du tas, si disponible.
        
        Paramètres :
        - joueur : l'objet joueur qui essaie de piocher un jeton.
        
        Retourne :
        - Le jeton pioché, ou None s'il n'y a pas de jeton à piocher.
        """
        if self.tas_jetons:
            jeton = self.tas_jetons.pop()
            joueur.piocher(jeton)
            return jeton
        else:
            print("Aucun jeton à piocher !")
            return None
