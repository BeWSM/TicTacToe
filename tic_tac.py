import tkinter as tk
from tkinter import font
from itertools import cycle
from player import Player, Move
                
class tic_tac_game:
    def __init__(self, players = Move.DEFAULT_PLAYERS, board_size = Move.BOARD_SIZE):
        self.players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self.players)
        self.winner_combo = []
        self.current_moves = []
        self.has_winner = False
        self.winning_combos = []
        self.setup_board()
        
    def get_winnig_combos(self):
        rows= [ [(Move.row, Move.col) for Move in row ]
               for row in self.current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        
        return rows + columns + [first_diagonal, second_diagonal]
    
    def setup_board(self):
        self.current_moves = [
            [Move(row, col) for col in range(self.board_size)] 
            for row in range(self.board_size)
        ]      
        self.winning_combos = self.get_winnig_combos()
    
    def is_valid_move(self, move):
        row, col = move.row, move.col
        move_was_not_played = self.current_moves[row][col].label == ""
        no_winner = not self.has_winner
        
        return no_winner and move_was_not_played
        
    def process_move(self, move):
        row, col = move.row, move.col
        self.current_moves[row][col] = move
        for combo in self.winning_combos:
            result = set(
                self.current_moves[n][m].label
                for n, m in combo
            )
            is_win = (len(result) == 1) and ("" not in result)
            if is_win:
                self.has_winner =  True
                self.winner_combo = combo
                break
    
    def _has_winner(self):
        winner = self.has_winner
        if winner is True:
            return True
        else:
            return False
    
    def is_tied(self, move):    
        no_winner = not self.has_winner
        played_moves =(
            move.label for row in self.current_moves for move in row
        )
        return no_winner and all(played_moves)
    
    def toggle_player(self):
        self.current_player = next(self.players)
        
        
    # def disapear_last_move(self):
    #     if Player.moves == 3:
            
    #         Player.moves = 2
    
class tic_tac_board(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.title("Tic Tac Toe 2")
        self.cells = {}
        self.game = game
        self.create_board_display()
        self.create_board_grid()
    
    def create_board_display(self):
        display_frame = tk.Frame(master = self)
        display_frame.pack(fill = tk.X)
        self.display = tk.Label(
            master = display_frame,
            text = "Ready?",
            font= font.Font(size = 28, weight = "bold"))
        self.display.pack()
    
    def create_board_grid(self):
        grid_frame = tk.Frame( master = self)
        grid_frame.pack()
        
        for row in range (self.game.board_size):
            self.rowconfigure(row, weight = 1, minsize = 50)
            self.rowconfigure(row, weight = 1, minsize = 75)
            
            for col in range (self.game.board_size):
                button = tk.Button(
                    master = grid_frame,
                    text = "",
                    font = font.Font(size= 36, weight= "bold"),
                    fg = "grey",
                    width = 3,
                    height = 2,
                    highlightbackground = "purple"
                )
                self.cells[button] = (row, col)
                button.bind("<ButtonPress - 1>", self.play)
                button.grid(
                    row = row,
                    column = col,
                    padx = 5,
                    pady = 5,
                    sticky = "nsew"
                    
                )   
    def update_button(self, clicked_btn):
        clicked_btn.config(text = self.game.current_player.label)
        clicked_btn.config(fg = self.game.current_player.color)
    
    def update_display(self, msg, color = "dark magenta"):
        self.display["text"] = msg
        self.display["fg"] = color
        
    def highlight_cells(self):
        for button, coordinates in  self.cells.items():
            button.config(highlightbackground = "violet red")
        
    def play(self, event):
        clicked_btn = event.widget
        row, col = self.cells[clicked_btn]
        move = Move(row, col, self.game.current_player.label)
        
        if self.game.is_valid_move(move):
            self.update_button(clicked_btn)
            self.game.process_move(move)
            
            if self.game.is_tied(move):
                self.update_display(msg= " Its a Tie", color = "midnight blue")
                
            elif self.game._has_winner():
                self.highlight_cells()
                msg = f'Player "{self.game.current_player.label}" won!'
                color = self.game.current_player.color
                self.update_display(msg = msg, color = color)
                
            else:
                self.game.toggle_player()
                msg = f"{self.game.current_player.label}'s turn "
                self.update_display(msg= msg)
                
                
                