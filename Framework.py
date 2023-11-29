import numpy as np
import math

class Connect4Game:
    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.board = np.zeros((rows, cols), dtype=int)
        self.current_player = 1
        self.mode = 'human'

    def is_valid_move(self, col):
        return self.board[0][col] == 0

    def make_move(self, col):
        for row in range(self.rows-1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                break

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def is_winner(self, player):
        # Check rows
        for row in range(self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] == player and
                    self.board[row][col+1] == player and
                    self.board[row][col+2] == player and
                    self.board[row][col+3] == player):
                    return True

        # Check columns
        for col in range(self.cols):
            for row in range(self.rows - 3):
                if (self.board[row][col] == player and
                    self.board[row+1][col] == player and
                    self.board[row+2][col] == player and
                    self.board[row+3][col] == player):
                    return True

        # Check diagonals (positive slope)
        for row in range(self.rows - 3):
            for col in range(self.cols - 3):
                if (self.board[row][col] == player and
                    self.board[row+1][col+1] == player and
                    self.board[row+2][col+2] == player and
                    self.board[row+3][col+3] == player):
                    return True

        # Check diagonals (negative slope)
        for row in range(3, self.rows):
            for col in range(self.cols - 3):
                if (self.board[row][col] == player and
                    self.board[row-1][col+1] == player and
                    self.board[row-2][col+2] == player and
                    self.board[row-3][col+3] == player):
                    return True

        return False

    def is_board_full(self):
        return np.all(self.board != 0)

    def print_board(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.board[row][col], end=' ')
            print()
        print()



# Adding a GUI

import tkinter as tk
from tkinter import messagebox

# GUI needs a little work but should be super easy to do
class Connect4GUI:

    def __init__(self, rows=6, cols=7):
        self.rows = rows
        self.cols = cols
        self.game = Connect4Game()
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.canvas = tk.Canvas(self.root, width=cols*100, height=rows*100, bg='blue')
        self.canvas.pack()
        self.root.after(1000, self.draw_board)

    def draw_board(self):
        self.canvas.delete(tk.ALL)
        for row in range(self.rows):
            for col in range(self.cols):
                if self.game.board[row][col] == 0:
                    color = 'white'
                elif self.game.board[row][col] == 1:
                    color = 'red'
                else:
                    color = 'yellow'
                self.canvas.create_oval(col*100+10, row*100+10, col*100+90, row*100+90, fill=color)
        if self.game.is_winner(1):
            messagebox.showinfo("Game Over", "Player 1 wins!")
            self.close()
        elif self.game.is_winner(2):
            messagebox.showinfo("Game Over", "Player 2 wins!")
            self.close()
        elif self.game.is_board_full():
            messagebox.showinfo("Game Over", "It's a draw!")
            self.close()
        else:
            self.root.after(1000, self.draw_board)

    def close(self):
        self.root.destroy()


# Create game and empty board
gui = Connect4GUI()
game = gui.game
gui.draw_board()
game.print_board()


def selectMove(game):

    # This is where our logic will go
    for col in range(game.cols):
        if game.is_valid_move(col):
            return col


while not game.is_board_full():
    if game.current_player == 1 and game.mode == 'human':
        col = int(input("Enter your move (column number): "))
        while not game.is_valid_move(col):
            col = int(input("Invalid move. Enter your move (column number): "))
    elif game.current_player == 1 and game.mode == 'computer':

        # Move logic for player 1 in Computer vs. Computer games
        col = selectMove(game)
    else:

        # Move logic for player 2 in all games
        col = selectMove(game)

    game.make_move(col)

    game.print_board()
    gui.draw_board()

    if game.is_winner(game.current_player):
        print(f"Player {game.current_player} wins!")
        break

    game.switch_player()

if game.is_board_full() and not game.is_winner(1) and not game.is_winner(2):
    print("It's a draw!")

def heuristic(game, multiplier=2, player=1):
    h, h_temp = 0, 0
    for r in range(len(game.board)):
        for c in range(len(game.board)):
            h_temp = h_pos(game, r, c, multiplier)
            if game.board[r][c] != player:
                h_temp *= -1
            h += h_temp
    return h

def h_pos(game, r_o, c_o, multiplier):

    if game.board[r_o][c_o] == 0: return 0

    # Tracking variables
    h = 0
    r, c = r_o, c_o

    # Check row
    h_temp = 1
    r = r_o - 1
    while (game.board[r][c_o] == game.board[r_o][c_o] or game.board[r][c_o] == 0) and r >= max(0, r_o - 3):
        r -= 1
        if game.board[r][c_o] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp
    h_temp = 1
    r = r_o + 1
    while (game.board[r][c_o] == game.board[r_o][c_o] or game.board[r][c_o] == 0) and r <= min(5, r_o + 3):
        r += 1
        if game.board[r][c_o] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp

    # Check column
    h_temp = 1
    r = r_o
    c = c_o - 1
    while (game.board[r_o][c] == game.board[r_o][c_o] or game.board[r_o][c] == 0) and c >= max(0, c_o - 3):
        c -= 1
        if game.board[r_o][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp
    h_temp = 1
    c = c_o + 1
    while (game.board[r_o][c] == game.board[r_o][c_o] or game.board[r_o][c] == 0) and c <= min(6, c_o + 3):
        c += 1
        if game.board[r_o][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp

    # Check diagonal
    h_temp = 1
    r = r_o + 1
    c = c_o - 1
    while (game.board[r][c] == game.board[r_o][c_o] or game.board[r][c] == 0) and c >= max(0, c_o - 3) and r <= min(5, r_o + 3):
        r += 1
        c -= 1
        if game.board[r][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp
    h_temp = 1
    r = r_o - 1
    c = c_o + 1
    while (game.board[r][c] == game.board[r_o][c_o] or game.board[r][c] == 0) and c <= min(6, c_o + 3) and r >= max(0, r_o - 3) :
        r -= 1
        c += 1
        if game.board[r][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp

    # Check other diagonal
    h_temp = 1
    r = r_o - 1
    c = c_o - 1
    while (game.board[r][c] == game.board[r_o][c_o] or game.board[r][c] == 0) and c >= max(0, c_o - 3) and r >= max(0, r_o - 3):
        r += 1
        c -= 1
        if game.board[r][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp
    h_temp = 1
    r = r_o + 1
    c = c_o + 1
    while (game.board[r][c] == game.board[r_o][c_o] or game.board[r][c] == 0) and c <= min(6, c_o + 3) and r <= min(5, r_o + 3):
        r -= 1
        c += 1
        if game.board[r][c] == game.board[r_o][c_o]:
            h_temp *= multiplier
            if h_temp >= 8:
                return math.inf
    h += h_temp

    return h



    







