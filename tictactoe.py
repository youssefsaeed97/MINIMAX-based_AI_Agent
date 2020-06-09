"""
Tic Tac Toe Player
"""

import math
import copy
# to debug
# import time

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
    xchecker = []
    ochecker = []

    for row in board:
        for col in row:
            if col == 'X':
                xchecker.append('X')
            elif col == 'O':
                ochecker.append('O')

    if len(xchecker) - len(ochecker) == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    poss_actions = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                poss_actions.add((row, col))

    return poss_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if not any(action == poss_action for poss_action in actions(board)):
        raise Exception("Not a valid action")

    board_mod = copy.deepcopy(board)

    board_mod[action[0]][action[1]] = player(board)

    return board_mod


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    diag1 = zip(range(3), range(3))
    diag2 = [[0, 2], [1, 1], [2, 0]]
    board_copy = copy.deepcopy(board)

    if player(board) == X:
        checker_li = [O] * 3
        winner = O

    else:
        checker_li = [X] * 3
        winner = X

    if any(checker_li == row for row in board):
        return winner

    if any(checker_li == col for col in list(map(list, zip(*board_copy)))):
        return winner

    if all(checker_li[0] == board[row][col] for row, col in diag1):
        return winner

    if all(checker_li[0] == board[row][col] for row, col in diag2):
        return winner

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True

    if winner(board) == None:
        if len(actions(board)) == 0:
            return True
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0


def max_val(board, prun_fctr):
    """
    Finds the maximum value of all the minimum values that can result from a given state.
    """
    # the following di is used for debugging (has to be returned as a 3rd index in the 'return' at the bottom)
    # di1 = {}
    if terminal(board):
        optimal_action = None
        return utility(board), optimal_action

    v = -math.inf

    for action in actions(board):
        # next line is the basic idea of a max fn
        # v = max(v, min_val(result(board, action)))
        minval = min_val(result(board, action), v)[0]
        # di1[action] = di1.get(action, minval)
        if minval > v:
            v = minval
            optimal_action = action

        '''
        Checking if v is bigger (!orequal) than the pruning factor (which is passed as an argument and therefore local of this fn).
        v is the max value being considered while observing all of the poss min val outcomes of the 'for loop' actions.
        Pruning factor, is the value passed from the previous fn (min_val), which was found as the latest min value,
        consequently considering;
        IF the max value (v) of the current fn (considering a very specific branch of the tree) is bigger than the pruning factor, then,
        there is no need to explore what's beyond, as the previous min_val fn (which called this max_val fn)
        has already found a smaller value, and shall not even consider the max value of the current function,
        so why look beyond, where finding a higher val would make it worse and finding a smaller one won't change a thing ?
        and that is what is called ALPHA-BETA PRUNING.
        '''
        if v > prun_fctr:
            break

    # the returned current value might not be the highest of this branch,
    # but it's definitely sufficient for taking higher authority decisions
    return v, optimal_action


def min_val(board, prun_fctr):
    """
    Finds the minimum value of all the maximum values that can result from a given state.
    """
    # the following di is used for debugging (has to be returned as a 3rd index in the 'return' at the bottom)
    # di2 = {}
    if terminal(board):
        optimal_action = None
        return utility(board), optimal_action

    v = math.inf

    for action in actions(board):
        # next line is the basic idea of a min fn
        # v = min(v, max_val(result(board, action)))
        maxval = max_val(result(board, action), v)[0]
        # di2[action] = di2.get(action, maxval)
        if maxval < v:
            v = maxval
            optimal_action = action

        '''
        Checking if v is smaller (!orequal) than the pruning factor (which is passed as an argument and therefore local of this fn).
        v is the min value being considered while observing all of the poss max val outcomes of the 'for loop' actions.
        Pruning factor, is the value passed from the previous fn (max_val), which was found as the latest max value,
        consequently considering;
        IF the min value (v) of the current fn (considering a very specific branch of the tree) is smaller than the pruning factor, then,
        there is no need to explore what's beyond, as the previous max_val fn (which called this min_val fn)
        has already found a higher value, and shall not even consider the min value of the current function,
        so why look beyond, where finding a smaller val would make it worse and finding a higher one won't change a thing ?
        and that is what is called ALPHA-BETA PRUNING.
        '''
        if v < prun_fctr:
            break

    # the returned current value might not be the smallest of this branch,
    # but it's definitely sufficient for taking higher authority decisions
    return v, optimal_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # commented commands are for debugging use
    # capture start time:
    # start = time.time()

    if player(board) == X:
        # initializing a pruning factor and passing it to the max_val fn as an argument (considered as local to the max_val fn)
        prun_fctr = math.inf
        # print('action: minvalofthemaxvals')
        # print(max_val(board, x)[2])
        # print('--------------------------')
        # print('maxval of all the poss min val: ', max_val(board, x)[0])
        # print('--------------------------')
        # print('optimal action selected: ', max_val(board, x)[1])
        # print('--------------------------')
        # execution time calculation debug
        # output = max_val(board, x)[1]
        # end = time.time()
        # print('minimax execution time: ', end - start)
        # return output
        return max_val(board, prun_fctr)[1]

    if player(board) == O:
        # initializing a pruning factor and passing it to the max_val fn as an argument (considered as local to the max_val fn)
        prun_fctr = -math.inf
        # print('action: maxvalofalltheminvals')
        # print(min_val(board, x)[2])
        # print('--------------------------')
        # print('minval of all the poss max val: ', min_val(board, x)[0])
        # print('--------------------------')
        # print('optimal action selected: ', min_val(board, x)[1])
        # print('--------------------------')
        # execution time calculation debug
        # output = min_val(board, x)[1]
        # end = time.time()
        # print('minimax execution time: ', end - start)
        # return output
        return min_val(board, prun_fctr)[1]
