from PyQt5.QtWidgets import QMessageBox

class Plateau:
    """
    Classe représentant le plateau de jeu Rummikub, contenant toutes les combinaisons de jetons en jeu.
    """
    
    def __init__(self):
        """
        Initialise un plateau vide sans combinaisons de jetons.
        """
        self.combinaisons = []  # Liste pour stocker les combinaisons de jetons sur le plateau.

    def ajouter_combinaison(self, combinaison):
        """
        Ajoute une nouvelle combinaison de jetons au plateau et tente de fusionner avec d'autres suites existantes.
        
        Paramètres :
        - combinaison : liste de jetons représentant la combinaison à ajouter.
        """
        self.combinaisons.append(combinaison)  # Ajoute la combinaison à la liste.
        self.fusionner_suites(combinaison)     # Tente de fusionner avec d'autres suites.

    def fusionner_suites(self, nouvelle_suite):
        """
        Tente de fusionner la nouvelle suite avec des suites existantes si elles partagent la même couleur et peuvent former une suite continue.
        
        Paramètres :
        - nouvelle_suite : la nouvelle suite de jetons à évaluer pour une fusion.
        """
        if not self.est_suite(nouvelle_suite):  # Vérifie si la nouvelle suite est valide.
            return

        couleur = nouvelle_suite[0].couleur  # Récupère la couleur de la nouvelle suite.
        # Trie les nombres des jetons de la nouvelle suite, en remplaçant les jokers par -1 pour les ignorer.
        nombres_nouvelle = sorted(jeton.nombre if not jeton.est_joker() else -1 for jeton in nouvelle_suite)

        for combinaison in self.combinaisons:  # Parcourt toutes les combinaisons existantes sur le plateau.
            if self.est_suite(combinaison) and combinaison[0].couleur == couleur:  # Vérifie si c'est une suite de la même couleur.
                # Trie les nombres des jetons existants.
                nombres_existants = sorted(jeton.nombre for jeton in combinaison if jeton.nombre is not None)
                if self.peut_fusionner(nombres_nouvelle, nombres_existants):  # Vérifie si la fusion est possible.
                    combinaison.extend(nouvelle_suite)  # Fusionne la nouvelle suite avec la combinaison existante.
                    self.combinaisons.remove(nouvelle_suite)  # Retire la nouvelle suite de la liste.
                    print(f"Fusion effectuée avec la suite existante : {combinaison}")
                    return

    def peut_fusionner(self, nombres_nouvelle, nombres_existants):
        """
        Vérifie si deux suites peuvent être fusionnées en une suite continue.
        
        Paramètres :
        - nombres_nouvelle : liste des nombres de la nouvelle suite.
        - nombres_existants : liste des nombres de la suite existante.
        
        Retourne :
        - True si les suites peuvent être fusionnées, False sinon.
        """
        # Vérifie si le début de la nouvelle suite est juste après la fin de l'existante ou vice versa.
        return (nombres_nouvelle[0] == nombres_existants[-1] + 1 or 
                nombres_nouvelle[-1] == nombres_existants[0] - 1)

    def est_suite(self, combinaison):
        """
        Détermine si une combinaison de jetons forme une suite (tous les jetons ont la même couleur).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est une suite, False sinon.
        """
        # Récupère les couleurs des jetons normaux et vérifie qu'elles sont toutes identiques.
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}
        return len(couleurs) == 1

    def est_serie(self, combinaison):
        """
        Détermine si une combinaison de jetons forme une série (même nombre mais couleurs différentes).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est une série, False sinon.
        """
        nombres = {jeton.nombre for jeton in combinaison if not jeton.est_joker()}
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}
        return len(nombres) == 1 and len(couleurs) >= 3  # Vérifie qu'il y a au moins 3 couleurs différentes.

    def afficher(self):
        """
        Affiche toutes les combinaisons présentes sur le plateau, avec les détails de chaque combinaison.
        """
        if not self.combinaisons:
            print("Aucune combinaison sur le plateau.")
            return
        
        for idx, combinaison in enumerate(self.combinaisons):  # Parcourt chaque combinaison sur le plateau.
            jetons_normaux = [jeton for jeton in combinaison if not jeton.est_joker()]  # Sépare les jetons normaux des jokers.
            jetons_normaux.sort(key=lambda j: j.nombre)  # Trie les jetons normaux par nombre.
            jokers = [jeton for jeton in combinaison if jeton.est_joker()]  # Récupère les jokers de la combinaison.
    
            # Détermine le type de combinaison (suite ou série).
            if len(jetons_normaux) == 1:
                comb_type = "Série"  # Une seule carte normale signifie une série.
            else:
                comb_type = "Suite" if self.est_suite(combinaison) else "Série"
            
            joker_positions = []  # Liste pour stocker les positions où les jokers peuvent être placés.
            
            if self.est_suite(combinaison):    
                # Recherche des positions pour placer des jokers en cas de saut dans la suite.
                for i in range(len(jetons_normaux) - 1):
                    saut = jetons_normaux[i + 1].nombre - jetons_normaux[i].nombre
                    if saut > 2:  # Si le saut est supérieur à 2, place deux jokers.
                        joker_positions.append(i + 1)
                        joker_positions.append(i + 2)
                        break
                    
                    elif saut == 1:  # Si le saut est de 1, place un joker à la position du saut.
                        joker_positions.append(i + 1)

                # Vérifie si un joker est présent et demande où le placer.
                if 'joker' in [jeton.couleur for jeton in combinaison]:  
                   choix = QMessageBox.question(
                       self, 
                       "Placement du Joker",
                       "Aucun saut détecté. Où voulez-vous placer le joker ?",
                       QMessageBox.Yes | QMessageBox.No
                   )
                   if choix == QMessageBox.Yes:
                       print("Joker placé à gauche.")
                   else:
                       print("Joker placé à droite.")
                       
                # Insère les jokers dans les espaces disponibles.
                for pos in joker_positions:
                    if jokers:  # Vérifie s'il reste des jokers à placer.
                        jetons_normaux.insert(pos, jokers.pop(0))  # Insère le premier joker.
                        if jokers:  # Place le second joker si disponible.
                            jetons_normaux.insert(pos + 1, jokers.pop(0))
    
            # Gère l'affichage des combinaisons.
            affichage_combinaison = []
            for jeton in jetons_normaux:
                if jeton.est_joker():
                    affichage_combinaison.append("joker")  # Représentation du joker.
                else:
                    affichage_combinaison.append(str(jeton))  # Affiche le jeton normal.
    
            # Affiche le type de combinaison et les jetons qu'elle contient.
            print(f"{comb_type} {idx + 1} : " + ' | '.join(f"{i}: {affichage_combinaison[i]}" for i in range(len(affichage_combinaison))))
        
    def prendre_jeton(self, comb_index, jeton_index, joueur):
        """
        Permet au joueur de prendre un jeton d'une combinaison sur le plateau.
        Si la combinaison résultante n'a plus que deux jetons, elle est retirée,
        et les deux jetons restants sont donnés au joueur.
        
        Paramètres :
        - comb_index : index de la combinaison dans la liste des combinaisons.
        - jeton_index : index du jeton à prendre dans la combinaison.
        - joueur : objet joueur qui prendra le jeton.
        
        Retourne :
        - True si l'opération est réussie, False sinon.
        """
        if 0 <= comb_index < len(self.combinaisons):
            combinaison = self.combinaisons[comb_index]
            if 0 <= jeton_index < len(combinaison):
                jeton = combinaison.pop(jeton_index)  # Retire le jeton de la combinaison.
                joueur.piocher(jeton, depuis_plateau=True)  # Précise que le jeton vient du plateau.
                print(f"{joueur.nom} a pris le jeton : {jeton}")

                # Vérifie s'il ne reste que deux jetons dans la combinaison.
                if len(combinaison) == 2:
                    print(f"Il reste seulement deux jetons dans la combinaison, ils vous sont donnés.")
                    for jeton_restant in combinaison:
                        joueur.piocher(jeton_restant, depuis_plateau=True)  # Donne les jetons restants au joueur.
                        print(f"{joueur.nom} a pris aussi le jeton restant : {jeton_restant}")
                    self.combinaisons.pop(comb_index)  # Retire la combinaison du plateau.
                return True
            else:
                print("Index de jeton invalide.")
        else:
            print("Index de combinaison invalide.")
        return False
