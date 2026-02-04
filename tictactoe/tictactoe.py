import copy
import math
X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action_set.add((i, j))
    return action_set

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if i not in range(3) or j not in range(3):
        raise Exception("Invalid action: out of bounds")
    if board[i][j] != EMPTY:
        raise Exception("Invalid action: cell already occupied")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines = []


    for row in board:
        lines.append(row)


    for j in range(3):
        col = [board[i][j] for i in range(3)]
        lines.append(col)

    # Diagonals
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])

    for line in lines:
        if line.count(X) == 3:
            return X
        elif line.count(O) == 3:
            return O

    return None

def terminal(board):
    """
    Returns True if game is over (win or tie), False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False
    return True

def utility(board):
    """
    Returns 1 if X has won, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board using alpha-beta pruning.
    If board is terminal, returns None.
    """

    if terminal(board):
        return None

    current_player = player(board)

    if current_player == X:
        value, move = max_value(board, float('-inf'), float('inf'))
    else:
        value, move = min_value(board, float('-inf'), float('inf'))

    return move

def max_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = float('-inf')
    best_move = None

    for action in actions(board):
        min_v, _ = min_value(result(board, action), alpha, beta)
        if min_v > v:
            v = min_v
            best_move = action
        alpha = max(alpha, v)
        if beta <= alpha:
            break  # beta cutoff
    return v, best_move

def min_value(board, alpha, beta):
    if terminal(board):
        return utility(board), None

    v = float('inf')
    best_move = None

    for action in actions(board):
        max_v, _ = max_value(result(board, action), alpha, beta)
        if max_v < v:
            v = max_v
            best_move = action
        beta = min(beta, v)
        if beta <= alpha:
            break  # alpha cutoff
    return v, best_move
