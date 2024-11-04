import random
from plateau_I import Plateau
from jeton_I import Jeton
from joker_I import Joker

class Jeu:
    def __init__(self):
        """
        Initialise le jeu avec la liste de joueurs, le tas de jetons, le plateau, le tour, et les tentatives sans jetons.
        """
        self.joueurs = []  # Initialise la liste des joueurs
        self.tas_jetons = self.creer_tas_jetons()  # Crée le tas de jetons en appelant la fonction correspondante
        self.plateau = Plateau()  # Initialise le plateau de jeu où les combinaisons seront posées
        self.tour = 0  # Compteur pour suivre le numéro du tour actuel
        self.tentatives_sans_jeton = 0  # Compteur des tentatives sans pioche de jeton pour détecter la fin du jeu

    def creer_tas_jetons(self):
        """
        Crée et mélange un tas de jetons, incluant des jokers.

        Retour :
        - Une liste de tous les jetons mélangés.
        """
        couleurs = ['Rouge', 'Bleu', 'Noir', 'Jaune']  # Définit les couleurs disponibles pour les jetons
        jetons = []  # Liste pour stocker tous les jetons créés
        for couleur in couleurs:
            for nombre in range(1, 14):
                image = f"{couleur}/{nombre}_{couleur[0]}.PNG"  # Définit le chemin de l'image du jeton
                jetons.append(Jeton(nombre, couleur, image))  # Ajoute le jeton de cette couleur et nombre à la liste
                jetons.append(Jeton(nombre, couleur, image))  # Chaque jeton est dupliqué selon les règles du jeu
        joker_images = ["joker/joker_1.PNG", "joker/joker_2.PNG"]  # Liste des images des jokers
        jetons += [Joker(image) for image in joker_images]  # Ajoute deux jokers au tas de jetons
        random.shuffle(jetons)  # Mélange tous les jetons pour un tirage aléatoire
        return jetons

    def ajouter_joueur(self, joueur):
        """
        Ajoute un joueur à la partie.

        Paramètre :
        - joueur : l'objet joueur à ajouter.
        """
        self.joueurs.append(joueur)  # Ajoute le joueur spécifié à la liste des joueurs

    def distribuer_jetons(self, nombre_jetons):
        """
        Distribue un nombre de jetons aux joueurs.

        Paramètre :
        - nombre_jetons : nombre de jetons à distribuer par joueur.
        """
        for joueur in self.joueurs:  # Parcourt tous les joueurs dans la partie
            for _ in range(nombre_jetons):  # Distribue le nombre spécifié de jetons à chaque joueur
                if self.tas_jetons:  # Vérifie qu'il reste des jetons dans le tas
                    joueur.piocher(self.tas_jetons.pop())  # Donne un jeton au joueur en prenant le dernier du tas

    def determine_depart(self):
        """
        Détermine le premier joueur en fonction du tirage du plus grand jeton.

        Retour :
        - Le joueur qui commence la partie.
        """
        max_jeton = -1  # Initialise la variable pour le nombre maximum de jeton tiré
        premier_joueur = None  # Initialise la variable pour le joueur qui commencera
        for joueur in self.joueurs:
            jeton = self.tas_jetons.pop()  # Pioche un jeton du tas pour chaque joueur
            if jeton.nombre > max_jeton:  # Vérifie si le jeton pioché est le plus grand jusqu'à présent
                max_jeton = jeton.nombre  # Met à jour le nombre maximum de jeton
                premier_joueur = joueur  # Assigne le joueur ayant tiré le plus grand jeton
            joueur.piocher(jeton)  # Le joueur garde le jeton pioché dans son chevalet
        return premier_joueur  # Renvoie le joueur qui commencera la partie

    def ajouter_combinaison(self, combinaison):
        """
        Ajoute une combinaison au plateau après vérification de sa validité.

        Paramètre :
        - combinaison : liste de jetons à ajouter au plateau.

        Retour :
        - True si la combinaison est valide et ajoutée ; sinon, False.
        """
        if self.verifier_combinaison(combinaison):  # Vérifie que la combinaison est valide
            self.plateau.ajouter_combinaison(combinaison)  # Ajoute la combinaison au plateau
            joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]  # Identifie le joueur actuel
            joueur_actuel.poser_jetons(combinaison)  # Retire les jetons joués du chevalet du joueur
            return True  # Renvoie True pour indiquer que la combinaison a été ajoutée
        else:
            print("Combinaison invalide !")  # Message d'erreur si la combinaison n'est pas valide
            return False  # Renvoie False pour indiquer l'échec de l'ajout

    def verifier_combinaison(self, combinaison):
        """
        Vérifie la validité d'une combinaison (suite ou série).

        Paramètre :
        - combinaison : liste de jetons à vérifier.

        Retour :
        - True si la combinaison est valide ; sinon, False.
        """
        if len(combinaison) < 3:  # Vérifie que la combinaison contient au moins 3 jetons
            return False  # Une combinaison avec moins de 3 jetons est invalide
        jokers = [jeton for jeton in combinaison if isinstance(jeton, Joker)]  # Liste des jokers dans la combinaison
        non_jokers = [jeton for jeton in combinaison if isinstance(jeton, Jeton) and not jeton.est_joker()]  # Liste des jetons normaux
        if len(jokers) == 2 and len(non_jokers) == 1:  # Cas spécial : deux jokers et un seul jeton
            return True  # Cette combinaison est considérée valide
        non_jokers.sort(key=lambda jeton: jeton.nombre)  # Trie les jetons normaux par nombre
        couleurs = {jeton.couleur for jeton in non_jokers}  # Récupère les couleurs des jetons normaux
        nombres = [jeton.nombre for jeton in non_jokers]  # Récupère les nombres des jetons normaux

        if len(couleurs) == 1:  # Si tous les jetons ont la même couleur, c'est potentiellement une suite
            jokers_utilises = 0  # Compte les jokers utilisés pour combler les écarts
            for i in range(len(nombres) - 1):
                ecart = nombres[i + 1] - nombres[i]  # Calcule l'écart entre deux jetons
                if ecart == 2:
                    jokers_utilises += 1  # Utilise un joker si l'écart est de 2
                elif ecart == 3:
                    jokers_utilises += 2  # Utilise deux jokers si l'écart est de 3
                elif ecart > 4:
                    return False  # Un écart supérieur à 4 rend la combinaison invalide
                if jokers_utilises > len(jokers):
                    return False  # Si plus de jokers sont nécessaires que disponibles, la combinaison est invalide
            return True  # La combinaison est valide si les critères sont remplis
        elif len(set(nombres)) == 1:  # Si tous les nombres sont identiques, c'est potentiellement une série
            if len(couleurs) == len(non_jokers):  # Vérifie qu'il n'y a pas de doublon de couleur
                return len(couleurs) + len(jokers) >= 3  # La série doit être composée d'au moins 3 jetons

        return False  # La combinaison n'est ni une suite ni une série valide

    def joueur_gagnant(self):
        """
        Identifie le joueur qui a gagné en ayant vidé son chevalet.

        Retour :
        - Le joueur gagnant, ou None s'il n'y en a pas encore.
        """
        for joueur in self.joueurs:  # Parcourt la liste des joueurs
            if not joueur.chevalet:  # Vérifie si le joueur n'a plus de jetons dans son chevalet
                return joueur  # Renvoie le joueur gagnant
        return None  # Aucun joueur n'a encore gagné

    def joueur_avec_moins_jetons(self):
        """
        Détermine le joueur avec le moins de jetons dans son chevalet.

        Retour :
        - Le joueur avec le moins de jetons.
        """
        return min(self.joueurs, key=lambda joueur: len(joueur.chevalet))  # Renvoie le joueur avec le moins de jetons

    def demander_action(self, a_joue_combinaison, premier_jeu):
        """
        Demande l'action que le joueur souhaite effectuer.

        Paramètres :
        - a_joue_combinaison : booléen indiquant si le joueur a joué une combinaison.
        - premier_jeu : booléen indiquant si c'est le premier jeu du joueur.

        Retour :
        - Choix de l'action du joueur.
        """
        if a_joue_combinaison:
            if premier_jeu:
                return input("Voulez-vous (1) terminer votre tour ou (2) jouer une autre combinaison ? : ")
            return input("Voulez-vous (1) terminer votre tour, (2) jouer une autre combinaison ou (3) prendre un jeton du plateau? : ")
        return input("Voulez-vous (1) piocher ou (2) jouer une combinaison ? : ") if premier_jeu else input("Voulez-vous (1) piocher, (2) jouer une combinaison ou (3) prendre un jeton du plateau? : ")

    def demander_combinaison(self, joueur_actuel):
        """
        Demande une combinaison de jetons à jouer.

        Paramètre :
        - joueur_actuel : le joueur dont on demande la combinaison.

        Retour :
        - La combinaison de jetons sélectionnée par le joueur.
        """
        lettres = input("Entrez les lettres des jetons à poser (séparées par des virgules) : ")
        indices = [ord(l) - 65 for l in lettres if l.isalpha() and 0 <= ord(l) - 65 < len(joueur_actuel.chevalet)]
        return [joueur_actuel.chevalet[i] for i in indices]

    def calculer_score_combinaison(self, combinaison):
        """
        Calcule le score d'une combinaison en additionnant les valeurs des jetons.

        Paramètre :
        - combinaison : liste des jetons de la combinaison.

        Retour :
        - Score total de la combinaison.
        """
        return sum(jeton.nombre if jeton.nombre is not None else 0 for jeton in combinaison if isinstance(jeton, Jeton))

    def partie_terminee(self):
        """
        Vérifie si la partie est terminée.

        Retour :
        - True si la partie est terminée ; sinon, False.
        """
        return not self.tas_jetons and self.tentatives_sans_jeton >= len(self.joueurs) * 2
