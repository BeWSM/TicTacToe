import tkinter as tk
from tkinter import font
from typing import NamedTuple

class Player(NamedTuple):
    label: str
    color: str
    moves: int
    
class Move(NamedTuple):
    row: int
    col: int
    label: str = ""
    BOARD_SIZE = 3
    DEFAULT_PLAYERS = (
        Player(label = "X", color = "maroon3", moves = 0),
        Player(label = "O", color = "light sea green", moves = 0)
        
    )