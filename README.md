#Rummikub
pour jouer au jeux utiliser le code main pour lancer le jeux

Bienvenue dans le jeu Rummikub ! Ce projet est une implémentation du célèbre jeu de société qui allie stratégie et chance. Les joueurs s'efforcent de former des combinaisons de jetons pour marquer des points tout en jouant contre d'autres.

#Description du jeu

Rummikub est un jeu qui se joue avec des jetons numérotés de différentes couleurs. L'objectif est de poser toutes ses tuiles sur le plateau en formant des combinaisons valides. Le jeu se termine lorsqu'un joueur n'a plus de jetons, et le gagnant est celui qui a le moins de points restants.

#Technologies utilisées

    Python 3.x
    PyQt5

#Règles du Rummikub
Objectif du jeu : Le but est de se débarrasser de tous ses jetons en formant des combinaisons valides sur le plateau.

Jetons : Le jeu comprend des jetons numérotés de 1 à 13, dans quatre couleurs différentes, ainsi que des jokers.

Mises en place :

    Chaque joueur commence avec 14 jetons.
    Les jetons restants sont placés face cachée pour former une pioche.

Combinaisons valides :

    Séries : Trois jetons ou plus de la même couleur avec des numéros consécutifs (ex. : 3, 4, 5).
    Groupes : Trois jetons ou plus de même numéro mais de couleurs différentes (ex. : 5 rouge, 5 bleu, 5 jaune).

Premier tour :

    Pour poser des jetons sur le plateau lors du premier tour, un joueur doit accumuler 30 points en un seul coup. Les points correspondent à la valeur des jetons posés.

Tours de jeu :

    À chaque tour, un joueur peut :
        Piocher un jeton.
        Poser des jetons sur le plateau.
        Ajouter des jetons aux combinaisons existantes.
    Le tour se termine quand le joueur mis fin à sont tour en piochant 

Fin du jeu :

    Le jeu se termine lorsqu'un joueur n'a plus de jetons ou quand la pioche est épuisée et que les joueurs ne peuvent plus jouer.
    Le gagnant est le joueur avec le moins de points.
