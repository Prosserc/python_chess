#!/usr/bin/env python3
"""Constants etc for the game"""
from utils import format_msg

PIECE_CODES = {'K': 'king', 'Q': 'queen', 'R': 'rook',
               'B': 'bishop', 'N': 'knight', 'p': 'pawn'}

TEAMS = {'w': 'white', 'b': 'black'}

# describe piece positions by rank (row from bottom up) and file (col)
# used to instantiate Board and Piece classes
DEFAULT_START_POSITIONS = {
    8: dict(A='bR1', B='bN1', C='bB1', D='bQ', E='bK', F='bB2', G='bN2', H='bR2'),
    7: dict(A='bp1', B='bp2', C='bp3', D='bp4', E='bp5', F='bp6', G='bp7', H='bp8'),
    6: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    5: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    4: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    3: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
    2: dict(A='wp1', B='wp2', C='wp3', D='wp4', E='wp5', F='wp6', G='wp7', H='wp8'),
    1: dict(A='wR1', B='wN1', C='wB1', D='wQ', E='wK', F='wB2', G='wN2', H='wR2')
}

LOGGING = False

MOVE_INSTRUCTIONS = format_msg("\nTo specify a move enter the cell reference for the piece you "
        "want to move and the cell reference for the new location. The first two characters of "
        "your prompt entry are used to identify the current cell and the last two for the new "
        "cell e.g. to move from A2 to A4 you could enter 'A2, A4' or use shorthand of 'a2a4'.")

ep_conditions = [
    "A pawn can only move en_passant if all of the following conditions apply:",
    "  - an opposition pawn to your side (in the direction you are trying to move)",
    "  - this pawn has just taken it's first move (on the games last turn)",
    "  - this pawn's first move was two spaces forward"]

INVALID_MOVE_MESSAGES = {
    "piece": 'Move is not allowed for this piece.',
    "boundaries": "Move is not allowed as it would go outside of the board boundaries.",
    "path_gen": "This move is blocked as {0} is occupied.",
    "path_pawn": "Pawns cannot move straight forward when obstructed by another piece.",
    "path_knight": "This move is blocked as {0} is occupied by your team.",
    "cond_on_first": "A pawn can only move two spaces on it's first move.",
    "cond_on_take": "A pawn can only take when an opposition piece is diagonally in-front.",
    "cond_en_passant": "\n".join(ep_conditions),
    "king": "Move not allowed as it would leave your king in check with the {0} in cell {1}"
}

PIECE_VALUES = {'king': float("inf"), 'queen': 9, 'rook': 5, 'bishop': 3.5,
              'knight': 3.2, 'pawn': 1}
CHECK_POINTS = 0.1
CHECKMATE_POINTS = float("inf")
PAWN_FORWARD_POINTS = 0.04
