#!/usr/bin/python 
"""Unit test for chess.py - an automated game. As AI is not yet built
these will be purely random moves with no intellegence, but will serve 
as a good test it will cover a broad array of pieces / moves."""
from chess import *
from random import random as rnd
from time import sleep
import traceback

piece_vals = {'king': 1000, 'queen': 9, 'rook': 5, 'bishop': 3.5,
              'knight': 3.2, 'pawn': 1}

# no of seconds to sleep after a move
SLEEP_SECS = 0.2 # (less than 0.2 can cause issues with windows cmd prompt)

def pick_rnd(lst, cnt=None):
    """Returns a random item from a list."""
    if not cnt:
        cnt = len(lst)
    i = int(rnd()*(cnt-1)) # -1 needed to allow for zero based indexing
    return lst[i]

def random_move(game, team):
    """Level 0 - Select a move randomly from all possible moves."""
    move_dict, cnt = game.get_all_possible_moves(team=team)
    obj_list = []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            obj_list.append(move_obj)
    return pick_rnd(obj_list, cnt)

def level1_move(game, team):
    """Level 1 - Find all possible moves, select one resulting in the 
    best take available (if one is available)."""
    move_dict, cnt = game.get_all_possible_moves(team=team)
    max_points, obj_list = 0, []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            obj_list.append(move_obj)
            if move_obj.take:
                take_ref = \
                   game.board.positions[move_obj.new_row][move_obj.new_col]
                points = piece_vals[game.pieces[take_ref].name]
                if points > max_points:
                    max_points, selected_move = points, move_obj

    if max_points == 0:
        selected_move = pick_rnd(obj_list, cnt)
    return selected_move

def play(turns=400):
    """Launch moves"""
    # create top level object that starts the game, draws the pieces etc.
    game, team = Game(), 'None'

    level_fuction = {0: random_move, 1: level1_move}
    team_levels = {'white': 1, 'black': 0}

    while not game.checkmate and game.turns < turns:
        try:
            for team in ['white', 'black']:
                func = level_fuction[team_levels[team]]
                move_obj = func(game, team)
                game.take_turn(team, prompt=None, move=move_obj)
                sleep(SLEEP_SECS)
        except:
            pass # to follow...

    if game.checkmate:
        print('\n CHECKMATE, ' + team + ' team wins.')
    else:
        print(game.turns + ' turns have been taken, limit set to: ' + turns)

if __name__ == '__main__':
    play()
