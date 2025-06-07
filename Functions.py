import math

class GameState:
    """
    Représente un état du jeu de Morpion (Tic-Tac-Toe).
    Attributs:
        board (list of list of str): grille 3x3 contenant 'X', 'O' ou None pour vide.
        current_player (str): 'X' ou 'O', joueur dont c'est le tour.
    """
    def __init__(self, board=None, current_player='X'):
        if board is None:
            # Initialise une grille vide
            self.board = [[None for _ in range(3)] for _ in range(3)]
        else:
            # Copie profonde de la grille fournie
            self.board = [row.copy() for row in board]
        self.current_player = current_player


def actions(state: GameState):
    """
    Renvoie un ensemble de tuples (x, y) au lieu de (i, j).
    x = numéro de ligne, y = numéro de colonne
    """
    return {
        (i, j)
        for i in range(3)
        for j in range(3)
        if state.board[i][j] is None
    }

def result(state: GameState, action: tuple) -> GameState:
    """
    Retourne l'état résultant de l'application de l'action donnée sur l'état courant.
    Ne modifie pas l'état fourni, mais crée une nouvelle copie.

    Args:
        state (GameState): l'état courant du jeu.
        action (tuple): coup à jouer, sous la forme (i, j).

    Returns:
        GameState: nouvel état après avoir joué le coup et changé de joueur.
    """
    # Copie profonde de la grille
    new_board = [row.copy() for row in state.board]
    i, j = action
    # Placement du pion du joueur courant
    new_board[i][j] = state.current_player
    # Passage au joueur suivant
    next_player = 'O' if state.current_player == 'X' else 'X'
    return GameState(board=new_board, current_player=next_player)

def terminal(state: GameState) -> bool:
    """
    Teste si l'état est terminal : victoire pour 'X' ou 'O', ou grille pleine.
    Retourne True si le jeu est terminé, False sinon.
    """
    b = state.board
    # Vérifier les lignes, colonnes et diagonales
    # Lignes et colonnes
    for i in range(3):
        if b[i][0] is not None and b[i][0] == b[i][1] == b[i][2]:
            return True
        if b[0][i] is not None and b[0][i] == b[1][i] == b[2][i]:
            return True
    # Diagonales
    if b[0][0] is not None and b[0][0] == b[1][1] == b[2][2]:
        return True
    if b[0][2] is not None and b[0][2] == b[1][1] == b[2][0]:
        return True
    # Match nul si plus de coups possibles
    if not actions(state):
        return True
    return False

def utility(state: GameState, player: str) -> str:
    """
    Renvoie la valeur finale du jeu pour le joueur donné dans l'état s.
    +1 si ce joueur a gagné, -1 s'il a perdu, 0 pour un match nul ou si l'état n'est pas terminal.
    """
    if not terminal(state):
        return 0
    b = state.board
    # Vérifier victoire de 'X'
    win_x = (
        any(b[i][0] == b[i][1] == b[i][2] == 'X' for i in range(3)) or
        any(b[0][j] == b[1][j] == b[2][j] == 'X' for j in range(3)) or
        (b[0][0] == b[1][1] == b[2][2] == 'X') or
        (b[0][2] == b[1][1] == b[2][0] == 'X')
    )
    # Vérifier victoire de 'O'
    win_o = (
        any(b[i][0] == b[i][1] == b[i][2] == 'O' for i in range(3)) or
        any(b[0][j] == b[1][j] == b[2][j] == 'O' for j in range(3)) or
        (b[0][0] == b[1][1] == b[2][2] == 'O') or
        (b[0][2] == b[1][1] == b[2][0] == 'O')
    )
    if win_x and player == 'X':
        return 'X'
    if win_x and player != 'X':
        return 'X'
    if win_o and player == 'O':
        return 'O'
    if win_o and player != 'O':
        return 'O'
    # match nul
    return 'None'

def utility_value(state: GameState) -> int:
    """
    Renvoie +1 si 'X' a gagné, -1 si 'O' a gagné, et 0 sinon (match nul ou état non terminal).
    """
    b = state.board
    # lignes, colonnes, diagonales
    lines = [
        # lignes
        [(i,0),(i,1),(i,2)] for i in range(3)
    ] + [
        # colonnes
        [(0,j),(1,j),(2,j)] for j in range(3)
    ] + [
        # diagonales
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)],
    ]
    for line in lines:
        cells = [b[i][j] for i,j in line]
        if cells == ['X','X','X']:
            return +1
        if cells == ['O','O','O']:
            return -1
    return 0  # match nul ou état non terminal

def minimax_decision(state: GameState) -> tuple:
    """
    Retourne le meilleur coup pour state.current_player selon Minimax.
    """
    player = state.current_player
    if player == 'X':
        best_val = -math.inf
        best_action = None
        for a in actions(state):
            v = min_value(result(state, a))
            if v > best_val:
                best_val = v
                best_action = a
    else:  # joueur 'O' minimise
        best_val = math.inf
        best_action = None
        for a in actions(state):
            v = max_value(result(state, a))
            if v < best_val:
                best_val = v
                best_action = a
    return best_action

def max_value(state: GameState) -> int:
    """
    Valeur Minimax quand c'est au tour du MAX ('X') de jouer.
    """
    if terminal(state):
        return utility_value(state)
    v = -math.inf
    for a in actions(state):
        v = max(v, min_value(result(state, a)))
    return v

def min_value(state: GameState) -> int:
    """
    Valeur Minimax quand c'est au tour du MIN ('O') de jouer.
    """
    if terminal(state):
        return utility_value(state)
    v = math.inf
    for a in actions(state):
        v = min(v, max_value(result(state, a)))
    return v

def alpha_beta_search(state: GameState) -> tuple:
    """
    Lance l'Alpha-Beta et renvoie le coup optimal pour state.current_player.
    """
    player = state.current_player
    best_action = None

    # on initialise alpha/beta
    alpha = -math.inf
    beta  = +math.inf

    if player == 'X':
        value = -math.inf
        for a in actions(state):
            v = min_value_ab(result(state, a), alpha, beta)
            if v > value:
                value = v
                best_action = a
            alpha = max(alpha, value)
    else:
        value = +math.inf
        for a in actions(state):
            v = max_value_ab(result(state, a), alpha, beta)
            if v < value:
                value = v
                best_action = a
            beta = min(beta, value)

    return best_action

def max_value_ab(state: GameState, alpha: float, beta: float) -> int:
    if terminal(state):
        return utility_value(state)
    v = -math.inf
    for a in actions(state):
        v = max(v, min_value_ab(result(state, a), alpha, beta))
        if v >= beta:
            return v        # coupure beta
        alpha = max(alpha, v)
    return v

def min_value_ab(state: GameState, alpha: float, beta: float) -> int:
    if terminal(state):
        return utility_value(state)
    v = +math.inf
    for a in actions(state):
        v = min(v, max_value_ab(result(state, a), alpha, beta))
        if v <= alpha:
            return v        # coupure alpha
        beta = min(beta, v)
    return v