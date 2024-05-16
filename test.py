class JeuClonium:
    def __init__(self, nb_joueurs, taille_plateau):
        self.nb_joueurs = nb_joueurs
        self.taille_plateau = taille_plateau
        self.plateau = [[None for _ in range(taille_plateau)] for _ in range(taille_plateau)]
        self.joueurs = [chr(65 + i) for i in range(nb_joueurs)]
        self.joueur_actuel = 0
        self.initialiser_plateau()

    def initialiser_plateau(self):
        coins = [(1, 1), (1, self.taille_plateau - 2), (self.taille_plateau - 2, 1), (self.taille_plateau - 2, self.taille_plateau - 2)]
        for i, joueur in enumerate(self.joueurs):
            x, y = coins[i % 4]
            self.plateau[x][y] = (joueur, 3)

    def afficher_plateau(self):
        for ligne in self.plateau:
            row_str = ""
            for cellule in ligne:
                if cellule:
                    joueur, points = cellule
                    row_str += f"{joueur}|{points} "
                else:
                    row_str += "... "
            print(row_str[:-1])
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
    while True:
        try:
            nb_joueurs = int(input("Entrez le nombre de joueurs (entre 2 et 4) : "))
            if nb_joueurs < 2 or nb_joueurs > 4:
                print("Le nombre de joueurs doit être entre 2 et 4.")
                continue
            taille_plateau = int(input("Entrez la taille du plateau (entre 5 et 10) : "))
            if taille_plateau < 5 or taille_plateau > 10:
                print("La taille du plateau doit être entre 5 et 10.")
                continue
            break
        except ValueError:
            print("Entrée invalide, veuillez entrer un nombre entier.")

    jeu = JeuClonium(nb_joueurs, taille_plateau)
    jeu.jouer_jeu()
