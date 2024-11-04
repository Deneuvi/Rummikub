import random
from plateau_I import Plateau
from jeton_I import Jeton
from joker_I import Joker
from plateau_I import Plateau

class Jeu:
    def __init__(self):
        """
        Initialise le jeu en créant une liste de joueurs, un tas de jetons, un plateau et un compteur de tours.
        """
        self.joueurs = []  # Liste pour stocker les joueurs
        self.tas_jetons = self.creer_tas_jetons()  # Crée le tas de jetons pour la partie
        self.plateau = Plateau()  # Initialise ici en tant qu'objet de type Plateau
        self.tour = 0  # Compteur pour suivre le tour actuel
        self.tentatives_sans_jeton = 0  # Compte le nombre de tentatives sans tirage de jetons

    def creer_tas_jetons(self):
        """
        Crée un tas de jetons composé de jetons de différentes couleurs et de jokers.
        
        Retourne :
        - Une liste de jetons mélangés.
        """
        couleurs = ['Rouge', 'Bleu', 'Noir', 'Jaune']  # Définition des couleurs des jetons
        jetons = []  # Liste pour stocker les jetons créés
        # Créer les jetons avec les chemins d'image appropriés
        for couleur in couleurs:
            for nombre in range(1, 14):
                image = f"{couleur}/{nombre}_{couleur[0]}.PNG"  # Chemin d'image formaté
                jetons.append(Jeton(nombre, couleur, image))  # Ajout de deux jetons par couleur et nombre
                jetons.append(Jeton(nombre, couleur, image))
        
        # Ajouter des jokers au tas
        joker_images = ["joker/joker_1.PNG", "joker/joker_2.PNG"]
        jetons += [Joker(image) for image in joker_images]  # Ajouter des jokers à la liste de jetons
        random.shuffle(jetons)  # Mélange les jetons pour une distribution aléatoire
        return jetons  # Retourne le tas de jetons

    def ajouter_joueur(self, joueur):
        """
        Ajoute un joueur à la liste des joueurs.
        
        Paramètres :
        - joueur : le joueur à ajouter.
        """
        self.joueurs.append(joueur)  # Ajoute le joueur à la liste des joueurs

    def distribuer_jetons(self, nombre_jetons):
        """
        Distribue un certain nombre de jetons à chaque joueur.
        
        Paramètres :
        - nombre_jetons : le nombre de jetons à distribuer par joueur.
        """
        for joueur in self.joueurs:  # Pour chaque joueur dans la liste des joueurs
            for _ in range(nombre_jetons):  # Distribuer le nombre spécifié de jetons
                if self.tas_jetons:  # Vérifie s'il reste des jetons à distribuer
                    jeton = self.tas_jetons.pop()  # Prend le dernier jeton du tas
                    joueur.piocher(jeton)  # Le joueur pioche le jeton

    def determine_depart(self):
        """
        Détermine le joueur qui commence la partie en piochant un jeton du tas.
        
        Retourne :
        - Le joueur qui a le jeton avec le plus grand nombre.
        """
        max_jeton = -1  # Initialise la variable pour le jeton maximal
        premier_joueur = None  # Initialise la variable pour le premier joueur
        for joueur in self.joueurs:  # Pour chaque joueur dans la liste des joueurs
            jeton = self.tas_jetons.pop()  # Le joueur pioche un jeton
            if jeton.nombre > max_jeton:  # Vérifie si le jeton est le plus grand
                max_jeton = jeton.nombre  # Met à jour le jeton maximal
                premier_joueur = joueur  # Définit le premier joueur
            joueur.piocher(jeton)  # Le joueur pioche le jeton
        return premier_joueur  # Retourne le premier joueur

    def ajouter_combinaison(self, combinaison):
        """
        Ajoute une combinaison de jetons au plateau si elle est valide.
        
        Paramètres :
        - combinaison : liste de jetons à ajouter.
        
        Retourne :
        - True si la combinaison a été ajoutée, False sinon.
        """
        if self.verifier_combinaison(combinaison):  # Vérifie si la combinaison est valide
            self.plateau.ajouter_combinaison(combinaison)  # Ajoute la combinaison au plateau
            joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]  # Obtient le joueur actuel
            joueur_actuel.poser_jetons(combinaison)  # Le joueur pose les jetons
            return True  # Retourne vrai si la combinaison a été ajoutée
        else:
            print("Combinaison invalide !")  # Affiche un message d'erreur si la combinaison est invalide
            return False  # Retourne faux si la combinaison n'a pas été ajoutée

    def verifier_combinaison(self, combinaison):
        """
        Vérifie si une combinaison de jetons est valide (suite ou série).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est valide, False sinon.
        """
        if len(combinaison) < 3:  # Vérifie si la combinaison a au moins 3 jetons
            return False  # Retourne faux si la combinaison est trop courte
        
        # Séparer les jokers et les jetons normaux
        jokers = [jeton for jeton in combinaison if isinstance(jeton, Joker)]  # Liste des jokers
        non_jokers = [jeton for jeton in combinaison if isinstance(jeton, Jeton) and not jeton.est_joker()]  # Liste des jetons normaux

        # Cas spécial : 2 jokers et 1 seul jeton
        if len(jokers) == 2 and len(non_jokers) == 1:  # Si la combinaison contient 2 jokers et 1 jeton
            return True  # Les deux jokers peuvent être considérés comme des couleurs manquantes pour une série
    
        # Trier les jetons non-jokers par nombre pour comparer en ordre croissant
        non_jokers.sort(key=lambda jeton: jeton.nombre)  # Trie les jetons non-jokers
        couleurs = {jeton.couleur for jeton in non_jokers}  # Ensemble des couleurs uniques
        nombres = [jeton.nombre for jeton in non_jokers]  # Liste des nombres des jetons

        # Vérification des suites
        if len(couleurs) == 1:  # Si c'est une suite
            jokers_utilises = 0  # Compteur pour les jokers utilisés
            for i in range(len(nombres) - 1):  # Parcourt les jetons pour vérifier les suites
                ecart = nombres[i + 1] - nombres[i]  # Calcul de l'écart
                if ecart == 2:  # Si l'écart est de 2, on peut utiliser un joker
                    jokers_utilises += 1  # Incrémente le compteur de jokers utilisés
                if ecart == 3:  # Si l'écart est de 3, on peut utiliser deux jokers
                    jokers_utilises += 2
                elif ecart > 4:  # Si l'écart est supérieur à 4, c'est impossible
                    return False  # Retourne faux si la combinaison n'est pas valide

                # Vérifie si le nombre de jokers utilisés ne dépasse pas le nombre de jokers disponibles
                if jokers_utilises > len(jokers):  # Si trop de jokers sont utilisés
                    return False  # Retourne faux si la combinaison n'est pas valide
    
            return True  # Retourne vrai si la combinaison est une suite valide
    
        elif len(set(nombres)) == 1:  # Si c'est une série
            # Vérification si le nombre de couleurs est suffisant avec les jokers
            if len(couleurs) == len(non_jokers):  # Vérifie si chaque couleur est unique
                return len(couleurs) + len(jokers) >= 3  # Retourne vrai si le nombre total de couleurs avec jokers est au moins 3
            
        return False  # Retourne faux si la combinaison n'est pas valide

    def joueur_gagnant(self):
        """
        Détermine le joueur gagnant qui n'a plus de jetons.
        
        Retourne :
        - Le joueur gagnant ou None si aucun joueur n'a gagné.
        """
        for joueur in self.joueurs:  # Pour chaque joueur
            if not joueur.chevalet:  # Vérifie si le joueur n'a plus de jetons
                return joueur  # Retourne le joueur gagnant
        return None  # Retourne None si aucun joueur n'a gagné

    def joueur_avec_moins_jetons(self):
        """
        Trouve le joueur avec le moins de jetons dans son chevalet.
        
        Retourne :
        - Le joueur avec le moins de jetons.
        """
        return min(self.joueurs, key=lambda joueur: len(joueur.chevalet))  # Retourne le joueur avec le moins de jetons
    
    def demander_action(self, a_joue_combinaison, premier_jeu):
        """
        Demande au joueur quelle action il souhaite effectuer.
        
        Paramètres :
        - a_joue_combinaison : booléen indiquant si le joueur a joué une combinaison.
        - premier_jeu : booléen indiquant si c'est le premier jeu du joueur.
        
        Retourne :
        - La réponse de l'utilisateur sous forme de chaîne de caractères.
        """
        if a_joue_combinaison:  # Si le joueur a déjà joué une combinaison
            return input("Voulez-vous (1) terminer votre tour, (2) jouer une autre combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ") if not premier_jeu else input("Voulez-vous (1) terminer votre tour ou (2) jouer une autre combinaison ? (entrez 1 ou 2) : ")
        else:  # Si le joueur n'a pas encore joué de combinaison
            if premier_jeu:  # Si c'est le premier jeu
                return input("Voulez-vous (1) piocher ou (2) jouer une combinaison ? (entrez 1 ou 2) : ")
            else:  # Si ce n'est pas le premier jeu
                return input("Voulez-vous (1) piocher, (2) jouer une combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ")

    def demander_combinaison(self, joueur_actuel):
        """
        Demande au joueur d'entrer les lettres des jetons à poser.
        
        Paramètres :
        - joueur_actuel : le joueur dont c'est le tour.
        
        Retourne :
        - Une liste de jetons sélectionnés par le joueur.
        """
        lettres = input("Entrez les lettres des jetons à poser (séparées par des virgules) : ")  # Demande les lettres
        indices = [ord(l) - 65 for l in lettres if l.isalpha() and 0 <= ord(l) - 65 < len(joueur_actuel.chevalet)]  # Conversion des lettres en indices
        return [joueur_actuel.chevalet[i] for i in indices]  # Retourne les jetons sélectionnés

    def calculer_score_combinaison(self, combinaison):
        """
        Calcule le score d'une combinaison de jetons.
        
        Paramètres :
        - combinaison : liste de jetons dont le score doit être calculé.
        
        Retourne :
        - Le score total de la combinaison.
        """
        return sum(jeton.nombre if jeton.nombre is not None else 0 for jeton in combinaison if isinstance(jeton, Jeton))  # Somme des valeurs des jetons

    def partie_terminee(self):
        """
        Vérifie si la partie est terminée.
        
        Retourne :
        - True si la partie est terminée, False sinon.
        """
        return not self.tas_jetons and self.tentatives_sans_jeton >= len(self.joueurs)*2  # Vérifie si le tas est vide et si les tentatives sans jeton sont suffisantes
