#!/usr/bin/env python3
"""
Unit test for chess.py - an automated game. As AI is not yet built
these will be purely random moves with no intelligence, but will serve
as a good test it will cover a broad array of pieces / moves.
"""
# from game import Game
from utils import WRONG_ENTRY_POINT_MSG
from random import random as rnd
from copy import deepcopy

PIECE_VALS = {'queen': 9, 'rook': 5, 'bishop': 3.5,
              'knight': 3.2, 'pawn': 1, 'check': 3, 'checkmate': 1000}


def __pick_rnd(lst, cnt=None):
    """
    Returns a random item from a list.
    """
    if not cnt:
        cnt = len(lst)
    i = int(rnd() * (cnt - 1))  # -1 needed to allow for zero based indexing
    return lst[i]


def __random_move(game, team):
    """
    Level 0 - Select a move randomly from all possible moves.
    """
    move_dict, cnt = game.get_all_possible_moves(team=team)
    obj_list = []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            obj_list.append(move_obj)
    return __pick_rnd(obj_list, cnt)


def __game_state(game, team):
    """
    Asses the values of pieces on the current team relative to the
    the value of pieces on the other team.
    """
    pass  # to follow


def __next_move(game_branch, team):
    """
    Find all possible moves, select one resulting in the
    best take available (if one is available).
    """
    raise Exception("Not implemented yet")
    # obj_list.append(move_obj)
    # if move_obj.take:
    #     take_ref = \
    #        game_branch.board.positions[move_obj.new_row][move_obj.new_col]
    #     points = piece_vals[game_branch.pieces[take_ref].name]
    #     if points > max_points:
    #         max_points, selected_move = points, move_obj

    # if max_points == 0:
    #     selected_move = __pick_rnd(obj_list, cnt)
    # return selected_move


def pick_move(game, team, level):
    """
    Create a data structure representing the state of the game for
    each branch of moves (a game object) with a points score for the 
    branch. Points should be added for the best selectable move for 
    your team and taken off for the best possible opponents move.
    """
    if level == 0:
        return __random_move(game, team)
    max_points, obj_list = 0, []

    for l in range(1, level+1):
        if l == 1:
            branch = deepcopy(game)
        
        move_dict, cnt = branch.get_all_possible_moves(team=team)
        for piece_ref, moves in move_dict.items():
            for move_obj in moves:
                ##
                pass

        move_branches = {}


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
