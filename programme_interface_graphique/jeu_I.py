import random
from plateau_I import Plateau
from jeton_I import Jeton
from joker_I import Joker
from plateau_I import Plateau

class Jeu:
    def __init__(self):
        self.joueurs = []  # Liste des joueurs participant au jeu
        self.tas_jetons = self.creer_tas_jetons()  # Pile de tous les jetons créés pour le jeu
        self.plateau = Plateau()  # Plateau de jeu pour poser les combinaisons
        self.tour = 0  # Numéro du tour en cours
        self.tentatives_sans_jeton = 0  # Compteur de tours sans jetons restants pour signaler la fin de la partie

    def creer_tas_jetons(self):
        """Crée un tas de jetons, incluant les jokers, et mélange le tout."""
        couleurs = ['Rouge', 'Bleu', 'Noir', 'Jaune']
        jetons = []
        # Créer les jetons de 1 à 13 pour chaque couleur, avec une image pour chaque jeton
        for couleur in couleurs:
            for nombre in range(1, 14):
                image = f"{couleur}/{nombre}_{couleur[0]}.PNG"
                jetons.append(Jeton(nombre, couleur, image))
                jetons.append(Jeton(nombre, couleur, image))  # Ajoute chaque jeton deux fois pour correspondre aux règles du jeu

        # Ajouter deux jokers avec des images spécifiques
        joker_images = ["joker/joker_1.PNG", "joker/joker_2.PNG"]
        jetons += [Joker(image) for image in joker_images]
        random.shuffle(jetons)  # Mélanger tous les jetons pour un tirage aléatoire
        return jetons

    def ajouter_joueur(self, joueur):
        """Ajoute un joueur à la partie."""
        self.joueurs.append(joueur)

    def distribuer_jetons(self, nombre_jetons):
        """Distribue un certain nombre de jetons à chaque joueur au début de la partie."""
        for joueur in self.joueurs:
            for _ in range(nombre_jetons):
                if self.tas_jetons:  # Si le tas n'est pas vide
                    jeton = self.tas_jetons.pop()
                    joueur.piocher(jeton)  # Le joueur pioche un jeton

    def determine_depart(self):
        """Détermine le joueur qui commence en tirant le jeton avec le plus grand nombre."""
        max_jeton = -1
        premier_joueur = None
        for joueur in self.joueurs:
            jeton = self.tas_jetons.pop()
            if jeton.nombre > max_jeton:
                max_jeton = jeton.nombre
                premier_joueur = joueur
            joueur.piocher(jeton)  # Ajoute le jeton tiré au chevalet du joueur
        return premier_joueur  # Renvoie le joueur qui a tiré le plus grand jeton

    def ajouter_combinaison(self, combinaison):
        """Vérifie et ajoute une combinaison au plateau."""
        if self.verifier_combinaison(combinaison):  # Si la combinaison est valide
            self.plateau.ajouter_combinaison(combinaison)  # Ajoute au plateau
            joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]
            joueur_actuel.poser_jetons(combinaison)  # Retire les jetons posés du chevalet du joueur
            return True
        else:
            print("Combinaison invalide !")
            return False

    def verifier_combinaison(self, combinaison):
        """Vérifie la validité d'une combinaison (suite ou série)."""
        if len(combinaison) < 3:
            return False  # Une combinaison doit avoir au moins 3 jetons

        jokers = [jeton for jeton in combinaison if isinstance(jeton, Joker)]
        non_jokers = [jeton for jeton in combinaison if isinstance(jeton, Jeton) and not jeton.est_joker()]

        # Cas spécial : 2 jokers et 1 seul jeton
        if len(jokers) == 2 and len(non_jokers) == 1:
            return True

        # Vérification des suites
        non_jokers.sort(key=lambda jeton: jeton.nombre)  # Trie les jetons par nombre
        couleurs = {jeton.couleur for jeton in non_jokers}
        nombres = [jeton.nombre for jeton in non_jokers]

        if len(couleurs) == 1:  # Suite de même couleur
            jokers_utilises = 0
            for i in range(len(nombres) - 1):
                ecart = nombres[i + 1] - nombres[i]
                if ecart == 2:
                    jokers_utilises += 1
                elif ecart == 3:
                    jokers_utilises += 2
                elif ecart > 4:
                    return False
                if jokers_utilises > len(jokers):
                    return False
            return True

        elif len(set(nombres)) == 1:  # Série de même nombre
            if len(couleurs) == len(non_jokers):
                return len(couleurs) + len(jokers) >= 3

        return False

    def joueur_gagnant(self):
        """Renvoie le joueur gagnant (qui a vidé son chevalet), s'il y en a un."""
        for joueur in self.joueurs:
            if not joueur.chevalet:
                return joueur
        return None

    def joueur_avec_moins_jetons(self):
        """Renvoie le joueur ayant le moins de jetons dans son chevalet."""
        return min(self.joueurs, key=lambda joueur: len(joueur.chevalet))

    def demander_action(self, a_joue_combinaison, premier_jeu):
        """Demande au joueur s'il veut continuer, terminer son tour ou piocher."""
        if a_joue_combinaison:
            if premier_jeu:
                return input("Voulez-vous (1) terminer votre tour ou (2) jouer une autre combinaison ? (entrez 1 ou 2) : ")
            return input("Voulez-vous (1) terminer votre tour, (2) jouer une autre combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ")
        return input("Voulez-vous (1) piocher ou (2) jouer une combinaison ? (entrez 1 ou 2) : ") if premier_jeu else input("Voulez-vous (1) piocher, (2) jouer une combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ")

    def demander_combinaison(self, joueur_actuel):
        """Demande une combinaison à jouer en fonction des lettres des jetons."""
        lettres = input("Entrez les lettres des jetons à poser (séparées par des virgules) : ")
        indices = [ord(l) - 65 for l in lettres if l.isalpha() and 0 <= ord(l) - 65 < len(joueur_actuel.chevalet)]
        return [joueur_actuel.chevalet[i] for i in indices]

    def calculer_score_combinaison(self, combinaison):
        """Calcule le score d'une combinaison en additionnant les valeurs des jetons."""
        return sum(jeton.nombre if jeton.nombre is not None else 0 for jeton in combinaison if isinstance(jeton, Jeton))

    def partie_terminee(self):
        """Détermine si la partie est terminée."""
        return not self.tas_jetons and self.tentatives_sans_jeton >= len(self.joueurs) * 2
