# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 18:47:44 2024

@author: kerri
"""
from PyQt5.QtWidgets import QMessageBox

class Plateau:
    def __init__(self):
        self.combinaisons = []

    def ajouter_combinaison(self, combinaison):
        self.combinaisons.append(combinaison)
        self.fusionner_suites(combinaison)

    def fusionner_suites(self, nouvelle_suite):
        if not self.est_suite(nouvelle_suite):
            return

        couleur = nouvelle_suite[0].couleur
        nombres_nouvelle = sorted(jeton.nombre if not jeton.est_joker() else -1 for jeton in nouvelle_suite)

        for combinaison in self.combinaisons:
            if self.est_suite(combinaison) and combinaison[0].couleur == couleur:
                nombres_existants = sorted(jeton.nombre for jeton in combinaison if jeton.nombre is not None)
                if self.peut_fusionner(nombres_nouvelle, nombres_existants):
                    combinaison.extend(nouvelle_suite)
                    self.combinaisons.remove(nouvelle_suite)
                    print(f"Fusion effectuée avec la suite existante : {combinaison}")
                    return

    def peut_fusionner(self, nombres_nouvelle, nombres_existants):
        return (nombres_nouvelle[0] == nombres_existants[-1] + 1 or 
                nombres_nouvelle[-1] == nombres_existants[0] - 1)

    def est_suite(self, combinaison):
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}
        #nombres = sorted(jeton.nombre for jeton in combinaison if not jeton.est_joker())
        return len(couleurs) == 1 #and all(nombres[i] + 1 == nombres[i + 1] for i in range(len(nombres) - 1))

    def est_serie(self, combinaison):
        nombres = {jeton.nombre for jeton in combinaison if not jeton.est_joker()}
        couleurs = {jeton.couleur for jeton in combinaison  if not jeton.est_joker()}
        return len(nombres) == 1 and len(couleurs) >= 3

    def afficher(self):
        """Affiche toutes les combinaisons sur le plateau numérotées."""
        if not self.combinaisons:
            print("Aucune combinaison sur le plateau.")
            return
        
        for idx, combinaison in enumerate(self.combinaisons):
            # Séparer les jetons normaux et les jokers
            jetons_normaux = [jeton for jeton in combinaison if not jeton.est_joker()]
            # Trier les jetons normaux pour une suite
            jetons_normaux.sort(key=lambda j: j.nombre)
            jokers = [jeton for jeton in combinaison if jeton.est_joker()]
    
            # Déterminer le type de combinaison
            if len(jetons_normaux) == 1:
                comb_type = "Série"  # Si un seul jeton normal, c'est une série
            else:
                comb_type = "Suite" if self.est_suite(combinaison) else "Série"
            
            # Vérifier s'il y a un saut pour le placement du joker
            joker_positions = []
            
            if self.est_suite(combinaison):    
                # Vérifier la présence d'un saut
                for i in range(len(jetons_normaux) - 1):
                    saut = jetons_normaux[i + 1].nombre - jetons_normaux[i].nombre
                    if saut > 2:
                        # Placer deux jokers au milieu si le saut est supérieur à 2
                        joker_positions.append(i + 1)  # Position du premier joker
                        joker_positions.append(i + 2)  # Position du deuxième joker
                        break  # On sort de la boucle après avoir placé les jokers
                    
                    elif saut == 1:
                        joker_positions.append(i + 1)  # Ajouter la position où le saut a été détecté
                    # Example code to prompt for joker placement if needed
                    if 'joker' in [jeton.couleur for jeton in combinaison]:  # Adjust to your joker identification
                       choix = QMessageBox.question(
                           self, 
                           "Placement du Joker",
                           "Aucun saut détecté. Où voulez-vous placer le joker ?",
                           QMessageBox.Yes | QMessageBox.No
                       )
                       if choix == QMessageBox.Yes:
                           # Code to place the joker on the left
                           print("Joker placé à gauche.")
                       else:
                           # Code to place the joker on the right
                           print("Joker placé à droite.")
                           
                # Placer les jokers dans les espaces disponibles
                for pos in joker_positions:
                    if jokers:  # Vérifier s'il reste des jokers à placer
                        jetons_normaux.insert(pos, jokers.pop(0))  # Insérer le premier joker à la position trouvée
                        if jokers:  # Placer le second joker si disponible
                            jetons_normaux.insert(pos + 1, jokers.pop(0))  # Insérer le deuxième joker juste après
    
                
            # Gérer l'affichage
            affichage_combinaison = []
            for jeton in jetons_normaux:
                if jeton.est_joker():
                    affichage_combinaison.append("joker")  # Représentation du joker
                else:
                    affichage_combinaison.append(str(jeton))
    
            print(f"{comb_type} {idx + 1} : " + ' | '.join(f"{i}: {affichage_combinaison[i]}" for i in range(len(affichage_combinaison))))
        
    def prendre_jeton(self, comb_index, jeton_index, joueur):
        """Permet au joueur de prendre un jeton d'une combinaison sur le plateau.
           Si la combinaison résultante n'a plus que deux jetons, elle est retirée,
           et les deux jetons restants sont donnés au joueur."""
        if 0 <= comb_index < len(self.combinaisons):
            combinaison = self.combinaisons[comb_index]
            if 0 <= jeton_index < len(combinaison):
                jeton = combinaison.pop(jeton_index)
                joueur.piocher(jeton, depuis_plateau=True)  # Précise que le jeton vient du plateau
                print(f"{joueur.nom} a pris le jeton : {jeton}")

                # Vérifie s'il ne reste que deux jetons dans la combinaison
                if len(combinaison) == 2:
                    print(f"Il reste seulement deux jetons dans la combinaison, ils vous sont donnés.")
                    for jeton_restant in combinaison:
                        joueur.piocher(jeton_restant, depuis_plateau=True)
                        print(f"{joueur.nom} a pris aussi le jeton restant : {jeton_restant}")
                    self.combinaisons.pop(comb_index)  # Retire la combinaison car elle est vide
                return True
            else:
                print("Index de jeton invalide.")
        else:
            print("Index de combinaison invalide.")
        return False