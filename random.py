def afficher_allumettes(allumettes):
    print(f"Allumettes restantes: {allumettes} " + "|" * allumettes)

def tour_joueur(allumettes):
    while True:
        try:
            choix = int(input("\nCombien d'allumettes veux-tu prendre? (1-3): "))
            if choix in [1, 2, 3] and choix <= allumettes:
                return choix
            else:
                print("Choix invalide. Veuillez choisir un nombre entre 1 et 3 qui ne dépasse pas le nombre d'allumettes restantes.")
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def tour_bot(allumettes, niveau):
    if niveau == "facile":
        # Bot facile prend toujours 1 allumette si possible, sinon 1 allumette
        return 1
    elif niveau == "moyen":
        # Bot moyen joue semi-optimalement, essaye de laisser un multiple de 4 à l'adversaire mais parfois fait des erreurs
        if allumettes % 4 != 0:
            return allumettes % 4
        else:
            return 2 if allumettes >= 3 else 1
    else:  # niveau difficile
        # Bot difficile joue optimalement pour toujours essayer de gagner
        if allumettes % 4 == 0:
            return 3
        elif allumettes % 4 == 3:
            return 2
        elif allumettes % 4 == 2:
            return 1
        else:
            return 1

def jeu_des_allumettes():
    allumettes = 21
    print("Bienvenue au jeu des allumettes!")
    print("Il y a 21 allumettes. Chaque joueur peut en prendre 1 à 3 par tour.")
    print("Le joueur qui prend la dernière allumette perd.")

    mode = input("Choisissez le mode de jeu (1: Deux joueurs, 2: Contre le bot): ")
    if mode == "2":
        niveau = input("Choisissez le niveau de difficulté du bot (facile, moyen, difficile): ").lower()
    
    joueur_actuel = 1

    while allumettes > 0:
        afficher_allumettes(allumettes)

        if mode == "1" or (mode == "2" and joueur_actuel == 1):
            choix = tour_joueur(allumettes)
        else:
            choix = tour_bot(allumettes, niveau)
            print(f"\nLe bot prend {choix} allumette(s).")

        allumettes -= choix

        if allumettes == 0:
            afficher_allumettes(allumettes)
            if mode == "1":
                print(f"Le joueur {joueur_actuel} a pris la dernière allumette. Le joueur {joueur_actuel} a perdu!")
            else:
                if joueur_actuel == 1:
                    print("Tu as pris la dernière allumette. Tu as perdu!")
                else:
                    print("Le bot a pris la dernière allumette. Tu as gagné!")
            break

        joueur_actuel = 2 if joueur_actuel == 1 else 1

# Lancer le jeu
jeu_des_allumettes()
