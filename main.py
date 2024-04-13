import tkinter as tk
from tkinter import font
from tic_tac import tic_tac_board, tic_tac_game

game = tic_tac_game()
board = tic_tac_board(game)
board.mainloop()

