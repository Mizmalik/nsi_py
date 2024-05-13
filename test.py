import time
import random

class JeuClonium:
    def __init__(self):
        self.grille = []
        self.joueur = 0
        self.longueur = 0
        self.nbjoueurs = 0
        self.tour = 1
        self.compteur = 1

    def init_jeu(self):
        print("Bienvenue dans le jeu Clonium !")
        time.sleep(1)

        self.longueur = self.saisie_longueur()
        self.joueur = self.saisie_joueurs()
        self.nbjoueurs = self.joueur

        self.grille = self.initialiser_grille()
        print("La partie commence !")

    def saisie_longueur(self):
        longueur = int(input("Entrez la longueur de la grille (entre 5 et 10 cases): "))
        while longueur > 10 or longueur < 5:
            longueur = int(input("Entrez une longueur VALIDE (entre 5 et 10 cases): "))
        return longueur

    def saisie_joueurs(self):
        joueur = int(input("Entrez le nombre de joueur(s) humains (entre 1 et 4): "))
        while joueur < 1 or joueur > 4:
            print("Le nombre de joueurs humains doit être entre 1 et 4.")
            joueur = int(input("Entrez un nombre de joueur(s) humain(s) VALIDE (entre 1 et 4): "))
        return joueur

    def initialiser_grille(self):
        grille = [[0] * self.longueur for _ in range(self.longueur)]
        # Initialisation des joueurs
        for i in range(self.joueur):
            x, y = self.placer_joueur(grille)
            grille[x][y] = i + 1

        return grille

    def placer_joueur(self, grille):
        x = random.randint(0, self.longueur - 1)
        y = random.randint(0, self.longueur - 1)
        while grille[x][y] != 0:
            x = random.randint(0, self.longueur - 1)
            y = random.randint(0, self.longueur - 1)
        return x, y

    def jouer_tour(self):
        print(f"Tour du joueur {self.tour}")
        self.afficher_grille()
        self.choisir_case()
        self.explosion()
        self.tour_suivant()

    def choisir_case(self):
        print("Choisissez la case où jouer :")
        while True:
            x = int(input(f"Entrez la ligne (entre 0 et {self.longueur - 1}): "))
            y = int(input(f"Entrez la colonne (entre 0 et {self.longueur - 1}): "))
            if x >= 0 and x < self.longueur and y >= 0 and y < self.longueur and self.grille[x][y] == 0:
                self.grille[x][y] = self.tour
                self.compteur += 1
                break
            else:
                print("Case invalide ou occupée. Réessayez.")

    def explosion(self):
        for x in range(self.longueur):
            for y in range(self.longueur):
                if self.grille[x][y] == self.tour and self.grille[x][y] > 3:
                    self.grille[x][y] = 0
                    self.propager_explosion(x, y)

    def propager_explosion(self, x, y):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # Droite, Gauche, Bas, Haut
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.longueur and 0 <= new_y < self.longueur and self.grille[new_x][new_y] == self.tour:
                self.grille[new_x][new_y] = 0

    def tour_suivant(self):
        self.tour += 1
        if self.tour > self.nbjoueurs:
            self.tour = 1

    def victoire(self):
        if self.compteur == self.longueur * self.longueur:
            return True
        return False

    def afficher_grille(self):
        for row in self.grille:
            print(" ".join(str(cell) if cell != 0 else "0" for cell in row))


def main():
    jeu = JeuClonium()
    jeu.init_jeu()

    while not jeu.victoire():
        jeu.jouer_tour()

    print("Partie terminée !")


if __name__ == "__main__":
    main()