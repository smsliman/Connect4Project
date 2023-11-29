import copy

ROWS = 7
COLS = 6

'''
@param: board, the state of the connect 4 board
@param: player_num, which is 2 for now
@return: (heuristic_val, column)

ASSUMPTION: player_num is 2 for computer
'''


def execute_minimax(board, player_num, depth):
    # do return with heuristic if depth is 0
    if depth == 0:  # or node is terminal:
        # MAKE HEURISTIC ASSESSMENT AND RETURN HEURISTIC VALUE
        # heuristic_val
        return 0

    # make recursive calls for each possible column entry
    utilities = []
    for col in range(ROWS):
        row_to_check = 0
        # find row to change
        while board[row_to_check][col] != 0:
            row_to_check = row_to_check + 1
        # if there is space in the column, then we run recursive call
        if row_to_check < 7:
            board_copy = copy.copy(board)
            board_copy[row_to_check][col] = player_num
            move_utility = execute_minimax(board_copy, flip_player_num(player_num), depth-1)
            utilities.append(move_utility)
    # find either the minimum or maximum of utilities




def flip_player_num(player_num):
    return 2 if player_num == 1 else 1
