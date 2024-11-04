# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 19:19:30 2024

@author: kerri
"""

from plateau import Plateau 
from jeton import Jeton 
from joker import Joker 
import random


class Jeu:
    def __init__(self):
        self.joueurs = []
        self.tas_jetons = self.creer_tas_jetons()
        self.plateau = Plateau()  # Initialisez ici en tant qu'objet de type Plateau
        self.tour = 0
        self.tentatives_sans_jeton = 0

    def creer_tas_jetons(self):
    
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
        self.joueurs.append(joueur)

    def distribuer_jetons(self, nombre_jetons):
        for joueur in self.joueurs:
            for _ in range(nombre_jetons):
                if self.tas_jetons:
                    jeton = self.tas_jetons.pop()
                    joueur.piocher(jeton)

    def determine_depart(self):
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
        if self.verifier_combinaison(combinaison):
            self.plateau.ajouter_combinaison(combinaison)
            joueur_actuel = self.joueurs[self.tour % len(self.joueurs)]
            joueur_actuel.poser_jetons(combinaison)
            return True
        else:
            print("Combinaison invalide !")
            return False


    def verifier_combinaison(self, combinaison):
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
                print (ecart)
                if ecart == 2:  # Si l'écart est de 2, on peut utiliser un joker
                    jokers_utilises += 1
                if ecart == 3:  # Si l'écart est de 2, on peut utiliser un joker
                     jokers_utilises += 2
                elif ecart > 4:  # Si l'écart est supérieur à 2, c'est impossible
                    return False
                print (len(jokers))
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
        for joueur in self.joueurs:
            if not joueur.chevalet:
                return joueur
        return None

    def joueur_avec_moins_jetons(self):
        return min(self.joueurs, key=lambda joueur: len(joueur.chevalet))

    def jouer_tour(self):
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
    
            choix = self.demander_action(a_joue_combinaison, joueur_actuel.premier_jeu)

            if choix == '1':  # Choix de piocher
                if joueur_actuel.chevalet != etat_initial_chevalet:
                    if a_joue_combinaison==True : 
                         # Demande de confirmation pour terminer le tour si le joueur n'a pas atteint 30 points ou a encore des jetons pris
                        if ( total_points < 30 and joueur_actuel.premier_jeu == False ) or jetons_pris:
                            confirmation = input(
                                f"Vous n'avez pas atteint 30 points ou vous avez encore des jetons pris du plateau. Voulez-vous terminer le tour ? (oui/non) : ").lower()
                            if confirmation == 'oui':
                                print(f"{joueur_actuel.nom} a choisi de terminer son tour.")
                                joueur_actuel.chevalet = etat_initial_chevalet[:]
                                joueur_actuel.jetons_du_plateau = etat_initial_plateaux[:]
                                self.plateau.combinaisons = etat_initial_combinaisons[:]
                                joueur_actuel.premier_jeu = etat_initial_joueur
                                if self.tas_jetons:
                                    jeton = self.tas_jetons.pop()
                                    joueur_actuel.piocher(jeton)
                                    print(f"{joueur_actuel.nom} a pioché un jeton pour finir son tour : {jeton}")
                            else:
                                print("Tour annulé. Vous pouvez continuer à jouer.")
                        else :
                             joueur_actuel.premier_jeu = False  # Le joueur peut désormais sélectionner le choix 3
                             break
                        
                    
                elif self.tas_jetons:
                    jeton = self.tas_jetons.pop()
                    joueur_actuel.piocher(jeton)
                    print(f"{joueur_actuel.nom} a pioché : {jeton}")
                    break
                else:
                    self.tentatives_sans_jeton +=1
                    print("Il n'y a plus de jetons à piocher.")
                    break

            elif choix == '2':  # Jouer une combinaison
                combinaison = self.demander_combinaison(joueur_actuel)

                if self.ajouter_combinaison(combinaison):
                    score_combinaison = self.calculer_score_combinaison(combinaison)
                    combinaisons_posees.append(combinaison)
                    total_points += score_combinaison
                    self.tentatives_sans_jeton = 0
                    a_joue_combinaison = True

                    if joueur_actuel.premier_jeu and total_points >= 30:
                       
                        print(f"{joueur_actuel.nom} a atteint 30 points et peut maintenant prendre des jetons du plateau.")

                    print(f"Points cumulés : {total_points}")

                else:
                    print("Combinaison invalide !")
                    joueur_actuel.chevalet = etat_initial_chevalet[:]
                    self.plateau.combinaisons = etat_initial_combinaisons[:]
                    combinaisons_posees.clear()
                    total_points = 0
                    continue

            elif choix == '3' and not joueur_actuel.premier_jeu:  # Prendre un jeton du plateau
                comb_index = int(input("Entrez le numéro de la combinaison : ")) - 1
                jeton_index = int(input("Entrez l'index du jeton dans la combinaison : "))
                if self.plateau.prendre_jeton(comb_index, jeton_index, joueur_actuel):
                    jetons_pris.append((comb_index, jeton_index))
                else:
                    print("Erreur lors de la prise de jeton.")
                continue

            else:
                print("Choix invalide. Veuillez entrer 1, 2 ou 3 (le choix 3 est indisponible tant que vous n'avez pas atteint 30 points).")

            if not joueur_actuel.chevalet and not joueur_actuel.jetons_du_plateau:
               print(f"{joueur_actuel.nom} a gagné la partie en n'ayant plus de jetons !")
               return False  # La partie est terminée

        self.tour += 1
        return True
    
    def demander_action(self, a_joue_combinaison, premier_jeu):
        if a_joue_combinaison:
            # Si le joueur a déjà joué une combinaison, il peut terminer son tour ou jouer une autre combinaison
            return input("Voulez-vous (1) terminer votre tour, (2) jouer une autre combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ") if not premier_jeu else input("Voulez-vous (1) terminer votre tour ou (2) jouer une autre combinaison ? (entrez 1 ou 2) : ")
        else:
            # Si le joueur n'a pas encore joué de combinaison
            if premier_jeu:
                return input("Voulez-vous (1) piocher ou (2) jouer une combinaison ? (entrez 1 ou 2) : ")
            else:
                return input("Voulez-vous (1) piocher, (2) jouer une combinaison ou (3) prendre un jeton du plateau? (entrez 1, 2 ou 3) : ")

    def demander_combinaison(self, joueur_actuel):
        lettres = input("Entrez les lettres des jetons à poser (séparées par des virgules) : ")
        indices = [ord(l) - 65 for l in lettres if l.isalpha() and 0 <= ord(l) - 65 < len(joueur_actuel.chevalet)]
        return [joueur_actuel.chevalet[i] for i in indices]

    # def demander_continuer(self, joueur_actuel, total_points, combinaisons_posees):
    #     continuer = input("Voulez-vous jouer une autre combinaison ? (oui/non) : ").lower()
    #     if continuer == "non":
    #         return False
    #     print(f"Points cumulés : {total_points}")
    #     return True

    def calculer_score_combinaison(self, combinaison):
        return sum(jeton.nombre if jeton.nombre is not None else 0 for jeton in combinaison if isinstance(jeton, Jeton))

    def partie_terminee(self):
        return not self.tas_jetons and self.tentatives_sans_jeton >= len(self.joueurs)*2