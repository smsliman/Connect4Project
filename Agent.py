import math
import copy

class ConnectFourNode:
    def __init__(self, board, pt = 2):
        self.board = board
        self.player_turn = pt  # Assume player 2 goes first, since player one starts in framework

    def is_terminal(self):
        return self.is_winner(1, self.board) or self.is_winner(2, self.board) or self.is_board_full()

    def generate_children(self):
        children = []
        for col in range(7):
            if self.is_valid_move(col):
                #child_board = [row[:] for row in self.board]
                child_board = copy.deepcopy(self.board)
                self.make_move(child_board, col)
                children.append(ConnectFourNode(child_board, pt=(3 - self.player_turn))) # Make child and switch turn
        return children

    def heuristic(self, board, player, multiplier=7):
        
        if self.is_winner(player, board): 
            return 1000000
        if self.is_winner(3 - player, board): 
            return -1000000

        h = 0

        for row in range(6):
            for col in range(4):
                h_for, h_against = 1, 1
                for i in range(4):
                    h_for *= multiplier if board[row][col + i] == player else 1
                    h_against *= multiplier if board[row][col + i] == (3 - player) else 1
                h += h_for if all(board[row][col + i] != (3 - player) for i in range(4)) else 0
                h -= h_against if all(board[row][col + i] != player for i in range(4)) else 0

        for row in range(3):
            for col in range(7):
                h_for, h_against = 1, 1
                for i in range(4):
                    h_for *= multiplier if board[row + i][col] == player else 1
                    h_against *= multiplier if board[row + i][col] == (3 - player) else 1
                h += h_for if all(board[row + i][col] != (3 - player) for i in range(4)) else 0
                h -= h_against if all(board[row + i][col] != player for i in range(4)) else 0

        for row in range(3):
            for col in range(4):
                h_for, h_against = 1, 1
                for i in range(4):
                    h_for *= multiplier if board[row + i][col + i] == player else 1
                    h_against *= multiplier if board[row + i][col + i] == (3 - player) else 1
                h += h_for if all(board[row + i][col + i] != (3 - player) for i in range(4)) else 0
                h -= h_against if all(board[row + i][col + i] != player for i in range(4)) else 0

                h_for, h_against = 1, 1
                for i in range(4):
                    h_for *= multiplier if board[row + i][col + 3 - i] == player else 1
                    h_against *= multiplier if board[row + i][col + 3 - i] == (3 - player) else 1
                h += h_for if all(board[row + i][col + 3 - i] != (3 - player) for i in range(4)) else 0
                h -= h_against if all(board[row + i][col + 3 - i] != player for i in range(4)) else 0
        
        return h

    def evaluate(self):
        # if self.is_winner(1):
        #     return 100  # Player 1 wins
        # elif self.is_winner(2):
        #     return -100  # Player 2 wins
        # else:
        #     # Evaluate based on the number of pieces in a row
        return self.evaluate_board()

    def is_winner(self, player, b):
        # Check for a win in rows, columns, and diagonals
        for row in range(6):
            for col in range(4):
                if all(b[row][col + i] == player for i in range(4)):
                    return True  # Horizontal win

        for row in range(3):
            for col in range(7):
                if all(b[row + i][col] == player for i in range(4)):
                    return True  # Vertical win

        for row in range(3):
            for col in range(4):
                if all(b[row + i][col + i] == player for i in range(4)):
                    return True  # Diagonal win (top-left to bottom-right)

                if all(b[row + i][col + 3 - i] == player for i in range(4)):
                    return True  # Diagonal win (top-right to bottom-left)

        return False

    def is_board_full(self):
        return all(self.board[0][i] != 0 for i in range(7))

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, b, col):
        for row in range(5, -1, -1):
            if b[row][col] == 0:
                b[row][col] = self.player_turn
                break

    def evaluate_board(self):
        # Evaluate based on the number of potential unblocked rows, columns, or diagonals for both players
        #player1_score = self.evaluate_player(1)
        #player2_score = self.evaluate_player(2)
        return self.evaluate_player(1) #player1_score - player2_score

    ## THIS IS THE REWARD FUNCTION
    ## IF YOU WANT TO TEST A HEURISTIC, CHANGE THIS FUNCTION TO RETURN YOUR REWARD VAlUE
    def evaluate_player(self, player):
        return self.heuristic(self.board, player)
        """ score = 0
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 0:
                    score += self.score_position(row, col, 1, 0, player)  # Horizontal
                    score += self.score_position(row, col, 0, 1, player)  # Vertical
                    score += self.score_position(row, col, 1, 1, player)  # Diagonal /
                    score += self.score_position(row, col, 1, -1, player)  # Diagonal \
        return score """

    def score_position(self, row, col, row_change, col_change, player):
        score = 0
        for i in range(4):
            r = row + i * row_change
            c = col + i * col_change
            if 0 <= r < 6 and 0 <= c < 7:
                if self.board[r][c] == 0:
                    score += self.get_unblocked_count(r, c, row_change, col_change, player)
        return score

    def get_unblocked_count(self, row, col, row_change, col_change, player):
        unblocked_count = 0
        for i in range(4):
            r = row + i * row_change
            c = col + i * col_change
            if 0 <= r < 6 and 0 <= c < 7:
                if self.board[r][c] == player:
                    unblocked_count += 1
                elif self.board[r][c] == 3 - player:
                    return 0  # Blocked by opponent
        return unblocked_count


def minimax_alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.is_terminal():
        return node.evaluate()

    if maximizing_player:
        max_eval = -math.inf
        for child in node.generate_children():
            eval = minimax_alpha_beta(child, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cutoff
        return max_eval
    else:
        min_eval = math.inf
        for child in node.generate_children():
            eval = minimax_alpha_beta(child, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cutoff
        return min_eval

def reward(game, curr_player):
    depth = 3
    root = ConnectFourNode(game, curr_player)
    result = minimax_alpha_beta(root, 2 * depth, -math.inf, math.inf, curr_player == 2)
    print(result)
    return result
