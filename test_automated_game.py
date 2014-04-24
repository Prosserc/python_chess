#!/usr/bin/python 
"""Unit test for chess.py - an automated game. As AI is not yet built
these will be purely random moves with no intellegence, but will surve 
as a good test it will cover a broad array of pieces / moves."""
from chess import *
from random import random as rnd

# To Do
# -----
# bhild in customisable delay after each turn

def random_move(game, team):
    """Select a move randomly from all possible moves."""
    move_dict, cnt = game.get_all_possible_moves(team=team)
    obj_list = []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            obj_list.append(move_obj)
    #moves = [move_obj for move_obj in [move_dict[piece_ref] for piece_ref in move_dict.keys]]

    # get random index
    i = int(rnd()*cnt)
    print i, len(obj_list)
    return obj_list[i]

def play():
    """Launch moves"""
    MAX_TURNS = 400 # necessary until I have put draw rules into game

    # create top level object that starts the game, draws the pieces etc.
    game = Game() 

    while not game.checkmate and game.turns < MAX_TURNS:
        for team in ['white', 'black']:
            move_obj = random_move(game, team)
            game.take_turn(team, prompt=None, move=move_obj)

if __name__ == '__main__':
    play()
