from jeu import Jeu
from joueur import Joueur 

# Création d'une instance de la classe Jeu pour démarrer une nouvelle partie.
jeu = Jeu()

# Création des joueurs avec leurs noms respectifs.
joueur1 = Joueur("Alice")
joueur2 = Joueur("Bob")
joueur3 = Joueur("Charlie")
joueur4 = Joueur("Diana")

# Ajout des joueurs à la partie.
jeu.ajouter_joueur(joueur1)
jeu.ajouter_joueur(joueur2)
jeu.ajouter_joueur(joueur3)
jeu.ajouter_joueur(joueur4)

# Distribution de 14 jetons à chaque joueur.
jeu.distribuer_jetons(14)

# Détermination du joueur qui commencera la partie.
premier_joueur = jeu.determine_depart()
print(f"{premier_joueur.nom} commence le jeu!")

# Boucle principale du jeu qui continue tant que la partie n'est pas terminée.
while True:
    # Le joueur actuel joue son tour. Si la méthode retourne False, cela signifie que le tour est terminé.
    if not jeu.jouer_tour():
        break  # Sortie de la boucle si le tour est terminé.

    # Vérification du gagnant après le tour.
    gagnant = jeu.joueur_gagnant()
    if gagnant:
        # Affichage du nom du gagnant si un joueur a posé tous ses jetons.
        print(f"{gagnant.nom} a gagné le jeu en posant tous ses jetons !")
        break  # Sortie de la boucle en cas de victoire.

    # Vérification si la partie est terminée en raison de l'absence de jetons à piocher.
    if jeu.partie_terminee():
        # Identification du joueur ayant le moins de jetons restants.
        joueur_moins_jetons = jeu.joueur_avec_moins_jetons()
        # Affichage du gagnant basé sur le nombre de jetons restants.
        print(f"Il n'y a plus de jetons à piocher. {joueur_moins_jetons.nom} gagne avec le moins de jetons restants !")
        break  # Sortie de la boucle lorsque la partie est terminée.
