#!/usr/bin/python
"""Unit test for chess.py - an automated game. As AI is not yet built
these will be purely random moves with no intelligence, but will serve
as a good test it will cover a broad array of pieces / moves."""
from game import Game
from random import random as rnd
from time import sleep

piece_vals = {'king': float("inf"), 'queen': 9, 'rook': 5, 'bishop': 3.5,
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

def level2_move(game, team):
    """Level 2 - Find all possible moves, and all possible responses,
    score by value of pieces taken (minus any taken from yours),
    select one resulting in the best points."""
    ## TO FOLLOW
    ## wrewrite at some point as generic function to look any number of levels...
    move_dict, cnt = game.get_all_possible_moves(team=team)
    max_points, obj_list = 0, []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            points = 0
            obj_list.append(move_obj)
            if move_obj.take:
                take_ref = \
                   game.board.positions[move_obj.new_row][move_obj.new_col]
                points += piece_vals[game.pieces[take_ref].name]
            resp_moves, cnt2 = game.get_all_possible_moves(team=('white' if team == 'black' else 'black'))
            for their_piece_ref, their_moves in resp_moves.items():
                for their_mv_obj in their_moves:
                    if their_mv_obj.take:
                        if their_mv_obj.take:
                            their_take_ref = \
                               game.board.positions[their_mv_obj.new_row][their_mv_obj.new_col]
                            points -= piece_vals[game.pieces[their_take_ref].name]
                    if points > max_points:
                        max_points, selected_move = points, move_obj

    if max_points == 0:
        selected_move = pick_rnd(obj_list, cnt)
    return selected_move

def level3_move(game, team):
    """Level 3 - Find all possible moves to 3 turns score by value of
    pieces taken (minus any taken from yours), select one resulting in
    the best points."""
    ## TO FOLLOW
    ## wrewrite at some point as generic function to look any number of levels...
    move_dict, cnt = game.get_all_possible_moves(team=team)
    max_points, obj_list = 0, []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            points = 0
            obj_list.append(move_obj)
            if move_obj.take:
                take_ref = \
                   game.board.positions[move_obj.new_row][move_obj.new_col]
                points += piece_vals[game.pieces[take_ref].name]
            resp_moves, cnt2 = game.get_all_possible_moves(team=('white' if team == 'black' else 'black'))
            for mv2_pref, mv2_lst in resp_moves.items():
                for mv2_obj in mv2_lst:
                    if mv2_obj.take:
                        mv2_take_ref = \
                           game.board.positions[mv2_obj.new_row][mv2_obj.new_col]
                        points -= piece_vals[game.pieces[mv2_take_ref].name]
                    for mv3_pref, mv3_lst in resp_moves.items():
                        for mv3_obj in mv3_lst:
                            if mv3_obj.take:
                                mv3_take_ref = \
                                   game.board.positions[mv3_obj.new_row][mv3_obj.new_col]
                                points -= piece_vals[game.pieces[mv3_take_ref].name]
                        if points > max_points:
                            max_points, selected_move = points, move_obj

    if max_points == 0:
        selected_move = pick_rnd(obj_list, cnt)
    return selected_move


def play(turns=200):
    """Launch moves"""
    # create top level object that starts the game, draws the pieces etc.
    game, team = Game(), 'None'

    level_fuction = {0: random_move, 1: level1_move, 2: level2_move, 3: level3_move}
    team_levels = {'white': 3, 'black': 0}

    while not game.checkmate and game.turns < turns:
        # try:
        for team in ['white', 'black']:
            func = level_fuction[team_levels[team]]
            move_obj = func(game, team)
            game.take_turn(team, prompt=None, move=move_obj)
            sleep(SLEEP_SECS)
        # except:
        # pass # to follow...

    if game.checkmate:
        print('\n CHECKMATE, ' + team + ' team wins.')
    else:
        print(game.turns + ' turns have been taken, limit set to: ' + turns)

if __name__ == '__main__':
    play()
