#!/usr/bin/env python
"""Constants etc for the game"""
from utils import format_msg

PIECE_CODES = {'K': 'king', 'Q': 'queen', 'R': 'rook',
               'B': 'bishop', 'N': 'knight', 'p': 'pawn'}
TEAMS = {'w': 'white', 'b': 'black'}

# describe piece positions by rank (row from bottom up) and file (col)
# used to instantiate Board and Piece classes
START_POSITIONS = {
    8: dict(A='bR1', B='bN1', C='bB1', D='bQ', E='bK', F='bB2', G='bN2', H='bR2'),
    7: dict(A='bp1', B='bp2', C='bp3', D='bp4', E='bp5', F='bp6', G='bp7', H='bp8'),
    6: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    5: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    4: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    3: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    2: dict(A='wp1', B='wp2', C='wp3', D='wp4', E='wp5', F='wp6', G='wp7', H='wp8'),
    1: dict(A='wR1', B='wN1', C='wB1', D='wQ', E='wK', F='wB2', G='wN2', H='wR2')}

LOGGING = True

MOVE_INSTRUCTIONS = format_msg("\nTo specify a move enter the cell reference for the piece you "
        "want to move and the cell reference for the new location. The first two characters of "
        "your prompt entry are used to identify the current cell and the last two for the new "
        "cell e.g. to move from A2 to A4 you could enter 'A2, A4' or use shorthand of 'a2a4'.")
