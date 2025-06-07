from Functions import *

def visualize_actions(state: GameState):
    """
    Affiche la grille 3×3 en marquant par '*' les coups possibles,
    et en laissant 'X' ou 'O' là où ils sont joués.
    """
    coups = actions(state)
    print("Grille (les '*' sont les coups possibles) :\n")
    for i in range(3):
        row = []
        for j in range(3):
            if state.board[i][j] is None:
                # case vide : si c'est un coup possible, on met '*', sinon on met un espace
                row.append('*' if (i, j) in coups else ' ')
            else:
                # case déjà jouée
                row.append(state.board[i][j])
        # on imprime la ligne et une séparation
        print(" | ".join(row))
        if i < 2:
            print("---+---+---")
    print()  # ligne vide en fin

if __name__ == "__main__":
    # Choix du joueur humain
    human = ''
    while human not in ('X', 'O'):
        human = input("Veux-tu jouer X ou O ? ").upper()
    ai = 'O' if human == 'X' else 'X'

    # État de départ
    state = GameState()
    print("\nGrille initiale :")
    visualize_actions(state)

    # Boucle de jeu
    while not terminal(state):
        if state.current_player == human:
            # Tour de l'humain
            valid = False
            while not valid:
                try:
                    coup = input("Ton coup (format i,j avec i et j de 0 à 2) : ")
                    i, j = map(int, coup.split(','))
                    if (i, j) in actions(state):
                        valid = True
                    else:
                        print("Case déjà occupée ou hors grille, recommence.")
                except Exception:
                    print("Entrée invalide, format attendu : i,j")
            state = result(state, (i, j))
        else:
            # Tour de l'IA
            print(f"IA ({ai}) réfléchit…")
            coup_ia = minimax_decision(state)
            print("L’IA joue :", coup_ia)
            state = result(state, coup_ia)

        # Affichage de la grille après chaque coup
        visualize_actions(state)

    # Fin de partie
    score = utility_value(state)
    if score == +1:
        gagnant = 'X'
    elif score == -1:
        gagnant = 'O'
    else:
        gagnant = None

    if gagnant is None:
        print("Match nul !")
    elif gagnant == human:
        print("Bravo, tu as gagné ! 🎉")
    else:
        print("L’IA gagne. 😢")


