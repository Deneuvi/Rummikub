from PyQt5.QtWidgets import QMessageBox

class Plateau:
    """Représente le plateau de jeu où les combinaisons de jetons sont stockées et gérées."""

    def __init__(self):
        """
        Initialise un plateau avec une liste vide de combinaisons.
        """
        self.combinaisons = []  # Liste pour stocker les combinaisons de jetons sur le plateau

    def ajouter_combinaison(self, combinaison):
        """
        Ajoute une nouvelle combinaison de jetons au plateau.
        
        Paramètres :
        - combinaison : liste de jetons à ajouter.
        """
        self.combinaisons.append(combinaison)  # Ajoute la combinaison à la liste
        self.fusionner_suites(combinaison)  # Tente de fusionner la nouvelle combinaison avec les suites existantes

    def fusionner_suites(self, nouvelle_suite):
        """
        Fusionne une nouvelle suite avec les suites existantes si elles sont compatibles.
        
        Paramètres :
        - nouvelle_suite : liste de jetons représentant la nouvelle suite.
        """
        if not self.est_suite(nouvelle_suite):  # Vérifie si la nouvelle suite est valide
            return  # Si ce n'est pas une suite, on ne fusionne pas

        couleur = nouvelle_suite[0].couleur  # Récupère la couleur de la nouvelle suite
        nombres_nouvelle = sorted(jeton.nombre if not jeton.est_joker() else -1 for jeton in nouvelle_suite)  # Trie les nombres de la nouvelle suite

        for combinaison in self.combinaisons:  # Parcourt les combinaisons existantes
            if self.est_suite(combinaison) and combinaison[0].couleur == couleur:  # Vérifie si la combinaison existante est une suite et de la même couleur
                nombres_existants = sorted(jeton.nombre for jeton in combinaison if jeton.nombre is not None)  # Trie les nombres existants
                if self.peut_fusionner(nombres_nouvelle, nombres_existants):  # Vérifie si les deux suites peuvent être fusionnées
                    combinaison.extend(nouvelle_suite)  # Fusionne les suites
                    self.combinaisons.remove(nouvelle_suite)  # Retire la nouvelle suite de la liste
                    print(f"Fusion effectuée avec la suite existante : {combinaison}")  # Affiche un message de succès
                    return  # Sort de la méthode après la fusion

    def peut_fusionner(self, nombres_nouvelle, nombres_existants):
        """
        Vérifie si deux suites de nombres peuvent être fusionnées.
        
        Paramètres :
        - nombres_nouvelle : liste de nombres de la nouvelle suite.
        - nombres_existants : liste de nombres de la suite existante.
        
        Retourne :
        - True si la fusion est possible, False sinon.
        """
        return (nombres_nouvelle[0] == nombres_existants[-1] + 1 or 
                nombres_nouvelle[-1] == nombres_existants[0] - 1)  # Vérifie si les nombres sont consécutifs

    def est_suite(self, combinaison):
        """
        Détermine si une combinaison de jetons forme une suite (même couleur avec des nombres consécutifs).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est une suite, False sinon.
        """
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}  # Récupère les couleurs des jetons non jokers
        return len(couleurs) == 1  # Vérifie si tous les jetons ont la même couleur

    def est_serie(self, combinaison):
        """
        Détermine si une combinaison de jetons forme une série (même nombre mais couleurs différentes).
        
        Paramètres :
        - combinaison : liste de jetons à évaluer.
        
        Retourne :
        - True si la combinaison est une série, False sinon.
        """
        nombres = {jeton.nombre for jeton in combinaison if not jeton.est_joker()}  # Récupère les nombres des jetons non jokers
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}  # Récupère les couleurs des jetons non jokers
        return len(nombres) == 1 and len(couleurs) >= 3  # Vérifie s'il y a un seul nombre et au moins trois couleurs différentes

    def afficher(self):
        """Affiche toutes les combinaisons sur le plateau numérotées."""
        if not self.combinaisons:  # Vérifie si le plateau est vide
            print("Aucune combinaison sur le plateau.")  # Affiche un message si aucune combinaison n'est présente
            return
        
        for idx, combinaison in enumerate(self.combinaisons):  # Parcourt chaque combinaison
            # Séparer les jetons normaux et les jokers
            jetons_normaux = [jeton for jeton in combinaison if not jeton.est_joker()]  # Liste des jetons normaux
            # Trier les jetons normaux pour une suite
            jetons_normaux.sort(key=lambda j: j.nombre)  # Trie les jetons normaux par leur nombre
            jokers = [jeton for jeton in combinaison if jeton.est_joker()]  # Liste des jokers

            # Déterminer le type de combinaison
            if len(jetons_normaux) == 1:
                comb_type = "Série"  # Si un seul jeton normal, c'est une série
            else:
                comb_type = "Suite" if self.est_suite(combinaison) else "Série"  # Détermine si c'est une suite ou une série
            
            # Vérifier s'il y a un saut pour le placement du joker
            joker_positions = []  # Liste pour stocker les positions où les jokers peuvent être placés
            
            if self.est_suite(combinaison):  # Si la combinaison est une suite
                # Vérifier la présence d'un saut
                for i in range(len(jetons_normaux) - 1):
                    saut = jetons_normaux[i + 1].nombre - jetons_normaux[i].nombre  # Calcule le saut entre les nombres
                    if saut > 2:
                        # Placer deux jokers au milieu si le saut est supérieur à 2
                        joker_positions.append(i + 1)  # Position du premier joker
                        joker_positions.append(i + 2)  # Position du deuxième joker
                        break  # On sort de la boucle après avoir placé les jokers
                    
                    elif saut == 1:
                        joker_positions.append(i + 1)  # Ajouter la position où le saut a été détecté
                    # Exemple de code pour demander le placement du joker si nécessaire
                    if 'joker' in [jeton.couleur for jeton in combinaison]:  # Ajustez pour votre identification de joker
                       choix = QMessageBox.question(
                           self, 
                           "Placement du Joker",
                           "Aucun saut détecté. Où voulez-vous placer le joker ?",
                           QMessageBox.Yes | QMessageBox.No
                       )
                       if choix == QMessageBox.Yes:
                           # Code pour placer le joker à gauche
                           print("Joker placé à gauche.")
                       else:
                           # Code pour placer le joker à droite
                           print("Joker placé à droite.")
                           
                # Placer les jokers dans les espaces disponibles
                for pos in joker_positions:
                    if jokers:  # Vérifie s'il reste des jokers à placer
                        jetons_normaux.insert(pos, jokers.pop(0))  # Insère le premier joker à la position trouvée
                        if jokers:  # Placer le second joker si disponible
                            jetons_normaux.insert(pos + 1, jokers.pop(0))  # Insère le deuxième joker juste après
    
            # Gérer l'affichage
            affichage_combinaison = []  # Liste pour stocker l'affichage de la combinaison
            for jeton in jetons_normaux:  # Parcourt les jetons normaux pour l'affichage
                if jeton.est_joker():
                    affichage_combinaison.append("joker")  # Représentation du joker
                else:
                    affichage_combinaison.append(str(jeton))  # Ajoute la représentation du jeton normal
    
            print(f"{comb_type} {idx + 1} : " + ' | '.join(f"{i}: {affichage_combinaison[i]}" for i in range(len(affichage_combinaison))))  # Affiche la combinaison

    def prendre_jeton(self, comb_index, jeton_index, joueur):
        """
        Permet au joueur de prendre un jeton d'une combinaison sur le plateau.
        Si la combinaison résultante n'a plus que deux jetons, elle est retirée,
        et les deux jetons restants sont donnés au joueur.
        
        Paramètres :
        - comb_index : l'index de la combinaison sur le plateau.
        - jeton_index : l'index du jeton à prendre dans la combinaison.
        - joueur : le joueur qui prend le jeton.
        
        Retourne :
        - True si le jeton a été pris avec succès, False sinon.
        """
        if 0 <= comb_index < len(self.combinaisons):  # Vérifie que l'index de la combinaison est valide
            combinaison = self.combinaisons[comb_index]  # Récupère la combinaison
            if 0 <= jeton_index < len(combinaison):  # Vérifie que l'index du jeton est valide
                jeton = combinaison.pop(jeton_index)  # Retire le jeton de la combinaison
                joueur.piocher(jeton, depuis_plateau=True)  # Précise que le jeton vient du plateau
                print(f"{joueur.nom} a pris le jeton : {jeton}")  # Affiche quel joueur a pris quel jeton

                # Vérifie s'il ne reste que deux jetons dans la combinaison
                if len(combinaison) == 2:
                    print(f"Il reste seulement deux jetons dans la combinaison, ils vous sont donnés.")  # Message d'information
                    for jeton_restant in combinaison:  # Donne les jetons restants au joueur
                        joueur.piocher(jeton_restant, depuis_plateau=True)
                        print(f"{joueur.nom} a pris aussi le jeton restant : {jeton_restant}")  # Affiche quel joueur a pris le jeton restant
                    self.combinaisons.pop(comb_index)  # Retire la combinaison car elle est vide
                return True  # Retourne True si le jeton a été pris avec succès
            else:
                print("Index de jeton invalide.")  # Message d'erreur si l'index du jeton est invalide
        else:
            print("Index de combinaison invalide.")  # Message d'erreur si l'index de la combinaison est invalide
        return False  # Retourne False si la prise du jeton a échoué
