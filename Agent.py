import math

class ConnectFourNode:
    def __init__(self, board):
        self.board = board
        self.player_turn = 1  # Assume player 1 goes first

    def is_terminal(self):
        return self.is_winner(1) or self.is_winner(2) or self.is_board_full()

    def generate_children(self):
        children = []
        for col in range(7):
            if self.is_valid_move(col):
                child_board = [row[:] for row in self.board]
                self.make_move(child_board, col)
                child_node = ConnectFourNode(child_board)
                child_node.player_turn = 3 - self.player_turn  # Switch player turn
                children.append(child_node)
        return children

    def evaluate(self):
        if self.is_winner(1):
            return 100  # Player 1 wins
        elif self.is_winner(2):
            return -100  # Player 2 wins
        else:
            # Evaluate based on the number of pieces in a row
            return self.evaluate_board()

    def is_winner(self, player):
        # Check for a win in rows, columns, and diagonals
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True  # Horizontal win

        for row in range(3):
            for col in range(7):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True  # Vertical win

        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True  # Diagonal win (top-left to bottom-right)

                if all(self.board[row + i][col + 3 - i] == player for i in range(4)):
                    return True  # Diagonal win (top-right to bottom-left)

        return False

    def is_board_full(self):
        return all(self.board[0][i] != 0 for i in range(7))

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, board, col):
        for row in range(5, -1, -1):
            if board[row][col] == 0:
                board[row][col] = self.player_turn
                break

    def evaluate_board(self):
        # Evaluate based on the number of potential unblocked rows, columns, or diagonals for both players
        player1_score = self.evaluate_player(1)
        player2_score = self.evaluate_player(2)
        return player1_score - player2_score

    def evaluate_player(self, player):
        score = 0
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 0:
                    score += self.score_position(row, col, 1, 0, player)  # Horizontal
                    score += self.score_position(row, col, 0, 1, player)  # Vertical
                    score += self.score_position(row, col, 1, 1, player)  # Diagonal /
                    score += self.score_position(row, col, 1, -1, player)  # Diagonal \
        return score

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

def reward(game):
    root = ConnectFourNode(game)
    result = minimax_alpha_beta(root, 3, -math.inf, math.inf, True)
    return result
