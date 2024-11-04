class Plateau:
    def __init__(self):
        """Initialise le plateau avec une liste vide de combinaisons."""
        self.combinaisons = []

    def ajouter_combinaison(self, combinaison):
        """Ajoute une combinaison au plateau et tente de fusionner avec des suites existantes.

        Paramètres :
        - combinaison : liste de jetons à ajouter sur le plateau.
        """
        self.combinaisons.append(combinaison)
        self.fusionner_suites(combinaison)

    def fusionner_suites(self, nouvelle_suite):
        """Fusionne une nouvelle suite avec une suite existante si possible.

        Paramètres :
        - nouvelle_suite : liste de jetons à fusionner avec les suites existantes.
        """
        if not self.est_suite(nouvelle_suite):
            return  # Retourne si la nouvelle suite n'est pas valide

        couleur = nouvelle_suite[0].couleur
        nombres_nouvelle = sorted(jeton.nombre if not jeton.est_joker() else -1 for jeton in nouvelle_suite)

        for combinaison in self.combinaisons:
            if self.est_suite(combinaison) and combinaison[0].couleur == couleur:
                nombres_existants = sorted(jeton.nombre for jeton in combinaison if jeton.nombre is not None)
                if self.peut_fusionner(nombres_nouvelle, nombres_existants):
                    combinaison.extend(nouvelle_suite)  # Fusionne les jetons
                    self.combinaisons.remove(nouvelle_suite)  # Supprime la nouvelle suite
                    print(f"Fusion effectuée avec la suite existante : {combinaison}")
                    return  # Sortie de la méthode après fusion

    def peut_fusionner(self, nombres_nouvelle, nombres_existants):
        """Détermine si deux listes de nombres peuvent être fusionnées.

        Paramètres :
        - nombres_nouvelle : liste de nombres de la nouvelle suite.
        - nombres_existants : liste de nombres de la suite existante.

        Retourne :
        - True si les listes peuvent être fusionnées, False sinon.
        """
        return (nombres_nouvelle[0] == nombres_existants[-1] + 1 or 
                nombres_nouvelle[-1] == nombres_existants[0] - 1)

    def est_suite(self, combinaison):
        """Détermine si une combinaison de jetons forme une suite (même couleur et séquence numérique).

        Paramètres :
        - combinaison : liste de jetons à évaluer.

        Retourne :
        - True si la combinaison est une suite, False sinon.
        """
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}
        return len(couleurs) == 1  # Vérifie que tous les jetons ont la même couleur

    def est_serie(self, combinaison):
        """Détermine si une combinaison de jetons forme une série (même nombre mais couleurs différentes).

        Paramètres :
        - combinaison : liste de jetons à évaluer.

        Retourne :
        - True si la combinaison est une série, False sinon.
        """
        nombres = {jeton.nombre for jeton in combinaison if not jeton.est_joker()}
        couleurs = {jeton.couleur for jeton in combinaison if not jeton.est_joker()}
        return len(nombres) == 1 and len(couleurs) >= 3  # Vérifie qu'il y a des couleurs différentes

    def afficher(self):
        """Affiche toutes les combinaisons sur le plateau numérotées."""
        if not self.combinaisons:
            print("Aucune combinaison sur le plateau.")
            return
        
        for idx, combinaison in enumerate(self.combinaisons):
            # Séparer les jetons normaux et les jokers
            jetons_normaux = [jeton for jeton in combinaison if not jeton.est_joker()]
            jokers = [jeton for jeton in combinaison if jeton.est_joker()]
    
            # Déterminer le type de combinaison
            if len(jetons_normaux) == 1:
                comb_type = "Série"  # Si un seul jeton normal, c'est une série
            else:
                comb_type = "Suite" if self.est_suite(combinaison) else "Série"
            
            # Vérifier s'il y a un saut pour le placement du joker
            joker_positions = []
            
            if self.est_suite(combinaison):
                # Trier les jetons normaux pour une suite
                jetons_normaux.sort(key=lambda j: j.nombre)
    
                # Vérifier la présence d'un saut
                for i in range(len(jetons_normaux) - 1):
                    if jetons_normaux[i + 1].nombre - jetons_normaux[i].nombre > 1:
                        joker_positions.append(i + 1)  # Ajouter la position où le saut a été détecté
    
                # Placer les jokers dans les espaces disponibles
                for pos in joker_positions:
                    if jokers:  # Vérifier s'il reste des jokers à placer
                        jetons_normaux.insert(pos, jokers.pop(0))  # Insérer le premier joker à la position trouvée
    
            # Si aucun saut, demander à l'utilisateur où placer les jokers restants
            while jokers:
                choix = ""
                while choix not in ["gauche", "droite"]:
                    choix = input("Aucun saut détecté. Où voulez-vous placer le joker ? (gauche/droite) : ").strip().lower()
                    if choix not in ["gauche", "droite"]:
                        print("Choix invalide. Veuillez entrer 'gauche' ou 'droite'.")
    
                # Placer le joker à la position choisie
                if choix == "gauche":
                    joker_position = 0  # Placer à gauche
                elif choix == "droite":
                    joker_position = len(jetons_normaux)  # Placer à droite
                
                # Vérifier si la position est occupée
                if joker_position < len(jetons_normaux) and jetons_normaux[joker_position].est_joker():
                    print("L'espace est déjà occupé par un joker. Veuillez choisir un autre emplacement.")
                    continue  # Demander à nouveau où placer le joker
                else:
                    jetons_normaux.insert(joker_position, jokers.pop(0))  # Insérer le joker à la position choisie
    
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
           et les deux jetons restants sont donnés au joueur.

        Paramètres :
        - comb_index : index de la combinaison à partir de laquelle le jeton est pris.
        - jeton_index : index du jeton à prendre dans la combinaison.
        - joueur : l'objet joueur qui prend le jeton.
        
        Retourne :
        - True si le jeton a été pris avec succès, False sinon.
        """
        if 0 <= comb_index < len(self.combinaisons):
            combinaison = self.combinaisons[comb_index]
            if 0 <= jeton_index < len(combinaison):
                jeton = combinaison.pop(jeton_index)
                joueur.piocher(jeton, depuis_plateau=True)  # Précise que le jeton vient du plateau
                print(f"{joueur.nom} a pris le jeton : {jeton}")

                # Vérifie s'il ne reste que deux jetons et les transfère si nécessaire
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
