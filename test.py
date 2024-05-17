class JeuClonium:
    def __init__(self, nb_joueurs, taille_plateau):
        self.nb_joueurs = nb_joueurs
        self.taille_plateau = taille_plateau
        self.plateau = [[None for _ in range(taille_plateau)] for _ in range(taille_plateau)]
        self.joueurs = [chr(65 + i) for i in range(nb_joueurs)]  # Utilisation de lettres majuscules pour les joueurs
        self.couleurs = ["\033[31m", "\033[32m", "\033[34m", "\033[33m"]  # Couleurs pour les joueurs (rouge, vert, bleu, jaune)
        self.reset_color = "\033[0m"
        self.joueur_actuel = 0
        self.initialiser_plateau()

    def initialiser_plateau(self):
        # Configuration initiale avec un seul pion pour chaque joueur dans un coin différent à une case de tous les bords
        coins = [(1, 1), (1, self.taille_plateau - 2), (self.taille_plateau - 2, 1), (self.taille_plateau - 2, self.taille_plateau - 2)]
        for i, joueur in enumerate(self.joueurs):
            x, y = coins[i % 4]
            self.plateau[x][y] = (joueur, 3)

    def afficher_plateau(self):
        # Afficher la ligne du haut du plateau
        print("\033[1;30m╔\033[0m" + "\033[1;30m═══╦\033[0m" * (self.taille_plateau - 1) + "\033[1;30m═══╗\033[0m")
        for i, ligne in enumerate(self.plateau):
            row_str = "\033[1;30m║\033[0m"
            for cellule in ligne:
                if cellule:
                    joueur, points = cellule
                    couleur = self.couleurs[self.joueurs.index(joueur)]
                    row_str += f" {couleur}{points}{self.reset_color} \033[1;30m║\033[0m"
                else:
                    row_str += "   \033[1;30m║\033[0m"
            print(row_str)
            # Afficher la ligne de séparation ou la ligne du bas du plateau
            if i < self.taille_plateau - 1:
                print("\033[1;30m╠\033[0m" + "\033[1;30m═══╬\033[0m" * (self.taille_plateau - 1) + "\033[1;30m═══╣\033[0m")
            else:
                print("\033[1;30m╚\033[0m" + "\033[1;30m═══╩\033[0m" * (self.taille_plateau - 1) + "\033[1;30m═══╝\033[0m")
        print()

    def ajouter_point(self, x, y):
        joueur, points = self.plateau[x][y]
        if joueur != self.joueurs[self.joueur_actuel]:
            print("Vous ne pouvez pas ajouter un point au pion de l'adversaire !")
            return False
        self.plateau[x][y] = (joueur, points + 1)
        if points + 1 == 4:
            self.exploser(x, y)
        return True

    def exploser(self, x, y):
        joueur, _ = self.plateau[x][y]
        self.plateau[x][y] = None
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.taille_plateau and 0 <= ny < self.taille_plateau:
                if self.plateau[nx][ny]:
                    proprietaire, points = self.plateau[nx][ny]
                    self.plateau[nx][ny] = (joueur, points + 1)
                    if points + 1 == 4:
                        self.exploser(nx, ny)
                else:
                    self.plateau[nx][ny] = (joueur, 1)

    def changer_joueur(self):
        self.joueur_actuel = (self.joueur_actuel + 1) % self.nb_joueurs

    def verifier_vainqueur(self):
        pions_joueurs = {joueur: 0 for joueur in self.joueurs}
        for ligne in self.plateau:
            for cellule in ligne:
                if cellule:
                    pions_joueurs[cellule[0]] += 1
        for joueur, nb_pions in pions_joueurs.items():
            if nb_pions == 0:
                return joueur
        return None

    def jouer_tour(self):
        self.afficher_plateau()
        while True:
            try:
                x = int(input(f"{self.joueurs[self.joueur_actuel]}, entrez la colonne pour ajouter un point (0-{self.taille_plateau-1}): "))
                y = int(input(f"{self.joueurs[self.joueur_actuel]}, entrez la ligne pour ajouter un point (0-{self.taille_plateau-1}): "))
                if 0 <= x < self.taille_plateau and 0 <= y < self.taille_plateau and self.plateau[x][y]:
                    break
                else:
                    print("Coordonnées invalides ou case vide, veuillez réessayer.")
            except ValueError:
                print("Entrée invalide, veuillez entrer des nombres entiers.")
        
        if self.ajouter_point(x, y):
            vainqueur = self.verifier_vainqueur()
            if vainqueur:
                print(f"{vainqueur} a gagné !")
                return True
            self.changer_joueur()
        return False

    def jouer_jeu(self):
        while True:
            if self.jouer_tour():
                break

if __name__ == "__main__":
    # Initialiser le jeu avec les paramètres de l'utilisateur
    while True:
        try:
            nb_joueurs = int(input("Entrez le nombre de joueurs (entre 2 et 4): "))
            if 2 <= nb_joueurs <= 4:
                break
            else:
                print("Le nombre de joueurs doit être entre 2 et 4.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    while True:
        try:
            taille_plateau = int(input("Entrez la taille du plateau (entre 5 et 10): "))
            if 5 <= taille_plateau <= 10:
                break
            else:
                print("La taille du plateau doit être entre 5 et 10.")
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")
    
    jeu = JeuClonium(nb_joueurs, taille_plateau)
    jeu.jouer_jeu()
