import math
import copy

class ConnectFourNode:

    memo = {}

    def __init__(self, board, pt = 2):
        self.board = board
        self.player_turn = pt  # Assume player 2 goes first, since player 1 starts in Framework.py

    def is_terminal(self):
        return self.is_winner(1, self.board) or self.is_winner(2, self.board) or self.is_board_full()

    def generate_children(self):
        children = []
        for col in range(7):
            if self.is_valid_move(col):
                child = ConnectFourNode(board=copy.deepcopy(self.board), pt=(3 - self.player_turn))
                child.make_move(child.board, col)
                children.append(child)
        return children

    def heuristic(self, b, p=1, m=7):
        # Check the memo first
        if self.key(p, b) in ConnectFourNode.memo.keys():
            return ConnectFourNode.memo[self.key(p, b)]
        
        # Initialize return value
        h = 0

        # Test for immediate win/loss conditions
        if self.is_winner(p, b): 
            h = 1000000
            ConnectFourNode.memo[self.key(p, b)] = h
            return h
        if any(child.is_winner(3 - p, b) for child in self.generate_children()):
            h = -1000000
            ConnectFourNode.memo[self.key(p, b)] = h
            return h
        
        # Check horizontal sequences of 4
        for r in range(6):
            for c in range(4):
                h_f, h_a = 1, 1
                for i in range(4):
                    h_f *= (2 * m if self.player_turn == (3 - p) else m) if b[r][c + i] == p else (0.5 if b[r][c + i] == 0 else 0)
                    h_a *= (2 * m if self.player_turn == p else m) if b[r][c + i] == (3 - p) else (0.5 if b[r][c + i] == 0 else 0)
                h += h_f - h_a

        # Check vertical sequences of 4
        for r in range(3):
            for c in range(7):
                h_f, h_a = 1, 1
                for i in range(4):
                    h_f *= (2 * m if self.player_turn == (3 - p) else m) if b[r + i][c] == p else (0.5 if b[r+ i][c] == 0 else 0)
                    h_a *= (2 * m if self.player_turn == p else m) if b[r + i][c] == (3 - p) else (0.5 if b[r + i][c] == 0 else 0)
                h += h_f - h_a

        # Check diagonal sequences of 4
        for r in range(3):
            for c in range(4):

                # Check leftward diagonal (\) sequences of 4
                h_f, h_a = 1, 1
                for i in range(4):
                    h_f *= (2 * m if self.player_turn == (3 - p) else m) if b[r + i][c + i] == p else (0.5 if b[r+ i][c + i] == 0 else 0)
                    h_a *= (2 * m if self.player_turn == p else m) if b[r + i][c + i] == (3 - p) else (0.5 if b[r+ i][c + i] == 0 else 0)
                h += h_f - h_a

                # Check rightward diagonal (/) sequences of 4
                h_f, h_a = 1, 1
                for i in range(4):
                    h_f *= (2 * m if self.player_turn == (3 - p) else m) if b[r + i][c + 3 - i] == p else (0.5 if b[r+ i][c + 3 - i] == 0 else 0)
                    h_a *= (2 * m if self.player_turn == p else m) if b[r + i][c + 3 - i] == (3 - p) else (0.5 if b[r+ i][c + 3 - i] == 0 else 0)
                h += h_f - h_a
        
        ConnectFourNode.memo[self.key(p, b)] = h
        return h

    def evaluate(self):
        # return self.heuristic(self.board, p=1, m=7)
        return self.heuristic(self.board)

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
    
    def key(self, p, b):
        ret_val = f"{p}"
        for r in range(len(b)):
            for c in range(len(b[r])):
                ret_val += f"{b[r][c]}"
        return ret_val

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, b, col):
        for row in range(5, -1, -1):
            if b[row][col] == 0:
                b[row][col] = self.player_turn
                break


def minimax_alpha_beta(node, depth, alpha, beta, maximizing_player):
    if depth == 0 or node.is_terminal():
        return node.evaluate()
    elif maximizing_player:
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
    depth = 2
    return minimax_alpha_beta(ConnectFourNode(game, curr_player), 2 * depth, -math.inf, math.inf, curr_player == 2)
