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

    playerX = 0
    playerO = 0
    for list in board:
        for i in list:
            if i == X:
                playerX += 1
            elif i == O:
                playerO += 1
    if playerO == playerX:
        return X
    else:
        return O 


def actions(board):
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i,j))
    return moves

def result(board, action):
    for i in action:
        if (i > 2 or i < 0):
            raise ValueError('Invalid Action')
    player1 = player(board)
    boardDeep = copy.deepcopy(board)
    if boardDeep[action[0]][action[1]] is not EMPTY:
        raise Exception('taken move')
    boardDeep[action[0]][action[1]] = player1
    return boardDeep

def winner(board):

    if board[1][1] != EMPTY:
        if (board[0][0] == board [1][1] and board[2][2] == board[1][1]) or (board[0][2] == board [1][1] and board[2][0] == board [1][1]) or (board[0][1] == board [1][1] and board[2][1] == board [1][1]) or (board[1][0] == board [1][1] and board[1][2] == board [1][1]):
            return board[1][1]
    if board[0][0] != EMPTY:
        if (board[0][1] == board [0][0] and board[0][2] == board [0][0]) or (board[1][0] == board [0][0] and board [2][0] == board [0][0]):
            return board [0][0] 
    if board[2][2] != EMPTY:
        if (board[2][1] == board [2][2] and board[2][0] == board [2][2]) or (board[0][2] == board [2][2] and board [1][2] == board [2][2]):
            return board [2][2] 
    
    return None
    
def terminal(board):
    if winner(board) != None:
        return True
    for list in board:
        for i in list:
            if i == EMPTY:
                return False
    return True


def utility(board):
    var1 = winner(board)
    if var1 == None:
        return 0
    if var1 == X:
        return 1
    if var1 == O:
        return -1


def minimax(board):

    bestMove = None
    if player(board) == O: 
        v = 2
        for move in actions(board):
            minV = miniValue(result(board,move))
            if minV < v:
                bestMove = move
                v = minV
        return bestMove
    else:
        v = -2
        for move in actions(board):
            maxV = miniValue(result(board,move))
            if maxV > v:
                bestMove = move
                v = maxV
        return bestMove


def miniValue(board):
    if terminal(board):
        return utility(board)

    if player(board) == O: 
        v = 2
        for move in actions(board):
            v = min(v, miniValue(result(board,move)))
        return v
    else:
        v = -2
        for move in actions(board):
            v = max(v, miniValue(result(board,move)))
        return v