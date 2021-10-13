"""
Tic Tac Toe Player
"""

import math
import copy

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
    # Set counter for X and O on board
    X_count = 0
    O_count = 0
    # Loop through the board and count X and O
    for i in board:
        for j in i:
            if board[i][j]== X:
                X_count+=1
            elif board[i][j]== O:
                O_count+=1
    # Calculate the player who has next turn and return it
    if O_count < X_count:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions_set = {}
    # Loop through the board and look for EMPTY spaces
    for i in board:
        for j in i:
            if board[i][j]== EMPTY:
                actions_set.add((i,j))
    # Return a set of all possible actions available
    return actions_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a deepcopy of the input board
    board_copy = copy.deepcopy(board)

    # Find who the turn is
    current_player = player(board)

    # Loop through the board_copy and add the action
    for i in board:
        for j in i:
            if (j,i) == action:
                if (j,i) == EMPTY:
                    board_copy[i][j] = current_player
                else:
                    raise Exception("A move in {} is not possible".format(board_copy[i][j]))
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if any possible solution combination is met !This solution is not very elegant, have to check for other some opportuniti of recursion!
    # Check for orizontal tris combination
    if ((board[0][0] != EMPTY) and (board[0][0] == board[0][1]) and (board[0][1] == board[0][2])):
        return board[0][0]
    elif ((board[1][0] != EMPTY) and (board[1][0] == board[1][1]) and (board[1][1] == board[1][2])):
        return board[1][0]
    elif ((board[2][0] != EMPTY) and (board[2][0] == board[2][1]) and (board[2][1] == board[2][2])):
        return board[2][0]
    # Check for diagonal tris combination
    elif ((board[0][0] != EMPTY) and (board[0][0] == board[1][1]) and (board[1][1] == board[2][2])):
        return board[0][0]
    elif ((board[0][2] != EMPTY) and (board[0][2] == board[1][1]) and (board[1][1] == board[2][0])):
        return board[0][2]
    # Check for vertical tris combination
    elif ((board[0][0] != EMPTY) and (board[0][0] == board[1][0]) and (board[1][0] == board[2][0])):
        return board[0][0]
    elif ((board[1][0] != EMPTY) and (board[1][0] == board[1][1]) and (board[1][1] == board[1][2])):
        return board[1][0]
    elif ((board[2][0] != EMPTY) and (board[2][0] == board[2][1]) and (board[2][1] == board[2][2])):
        return board[2][0]
    # If no winner comibation is met, return None
    else:
        return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if some move are available. If no, the game must be over so return True
    move_available = 0
    for i in board:
        for j in board:
            if board[i][j] == EMPTY:
                move_available += 1
    if move_available == 0:
        return True
    elif winner(board) != None:
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)
    if game_winner == X:
        return 1
    elif game_winner == O:
        return (0-1)
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Find if the game is still on
    if terminal(board) == True:
        return None

    # Find who the turn is
    current_player = player(board)
    
    if current_player == X:
        d

    elif current_player == O:



def MaxValue(board):
    v = -math.inf
    if terminal(board) == True:
        return utility(board)
    
    # Find all the possible actions
    possible_actions = actions(board)
    for possible_action in possible_actions:
        v = max(v, MinValue(result(board, possible_action)))
        return v

def MinValue(board):
    v = math.inf
    if terminal(board) == True:
        return utility(board)
    
    # Find all the possible actions
    possible_actions = actions(board)
    for possible_action in possible_actions:
        v = min(v, MaxValue(result(board, possible_action)))
        return v
