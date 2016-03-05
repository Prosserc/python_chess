#!/usr/bin/env python3
"""
Module to decide move to make for computer player
"""
from random import random as rnd
from inspect import stack
from literals import PIECE_VALUES, CHECK_POINTS, CHECKMATE_POINTS


class AI(object):
    """
    Decide on moves for computer opponent
    """


    def get_points(self, game, move_obj):
        take_ref = game.board.positions[move_obj.new_row][move_obj.new_col]
        points = PIECE_VALUES[game.pieces[take_ref].name]
        if move_obj.checkmate:
            points += CHECKMATE_POINTS
        elif move_obj.check:
            points += CHECK_POINTS
        return points


    def pick_rnd(self, lst, cnt=None):
        """Returns a random item from a list."""
        if not cnt:
            cnt = len(lst)
        i = int(rnd() * (cnt - 1))  # -1 needed to allow for zero based indexing
        return lst[i]


    def random_move(self, game, team):
        """Level 0 - Select a move randomly from all possible moves."""
        state = "ready"
        func_name = stack()[0][3]
        if state.find("ready") != 0:
            raise Exception("{0} state {1}".format(func_name, state))

        move_dict, cnt = game.get_all_possible_moves(team=team)
        obj_list = []
        for piece_ref, moves in move_dict.items():
            for move_obj in moves:
                obj_list.append(move_obj)
        return self.pick_rnd(obj_list, cnt)


    def level1_move(self, game, team):
        """Level 1 - Find all possible moves, select one resulting in the
        best take available (if one is available)."""
        state = "ready - I think"
        func_name = stack()[0][3]
        if state.find("ready") != 0:
            raise Exception("{0} state {1}".format(func_name, state))

        move_dict, cnt = game.get_all_possible_moves(team=team)
        max_points, possible_moves, selected_move = 0, [], None
        for piece_ref, moves in move_dict.items():
            for move_obj in moves:
                possible_moves.append(move_obj)
                if move_obj.take:
                    points = self.get_points(game, move_obj)
                    if points > max_points:
                        max_points, selected_move = points, move_obj

        if not selected_move:
            selected_move = self.pick_rnd(possible_moves, cnt)
        return selected_move


    def level2_move(self, game, team):
        """Level 2 - Find all possible moves, and all possible responses,
        score by value of pieces taken (minus any taken from yours),
        select one resulting in the best points."""
        # TO FOLLOW
        # re-write at some point as generic function to look any number of levels...
        state = "ready for tests - probably not working"
        func_name = stack()[0][3]
        if state.find("ready") != 0:
            raise Exception("{0} state {1}".format(func_name, state))

        move_dict, cnt = game.get_all_possible_moves(team=team)
        max_points, possible_moves, selected_move = 0, [], None
        for piece_ref, moves in move_dict.items():
            for move_obj in moves:
                points = 0
                possible_moves.append(move_obj)
                if move_obj.take:
                    take_ref = game.board.positions[move_obj.new_row][move_obj.new_col]
                    points += PIECE_VALUES[game.pieces[take_ref].name]
                resp_moves, cnt2 = game.get_all_possible_moves(team=('white' if team == 'black' else 'black'))
                for their_piece_ref, their_moves in resp_moves.items():
                    for their_mv_obj in their_moves:
                        if their_mv_obj.take:
                            if their_mv_obj.take:
                                their_take_ref = \
                                    game.board.positions[their_mv_obj.new_row][their_mv_obj.new_col]
                                points -= PIECE_VALUES[game.pieces[their_take_ref].name]
                        if points > max_points:
                            max_points, selected_move = points, move_obj

        if not selected_move:
            selected_move = self.pick_rnd(possible_moves, cnt)
        return selected_move


    def level3_move(self, game, team):
        """Level 3 - Find all possible moves to 3 turns score by value of
        pieces taken (minus any taken from yours), select one resulting in
        the best points."""
        # TO FOLLOW
        # rewrite at some point as generic function to look any number of levels...
        state = "definitely not working"
        func_name = stack()[0][3]
        if state.find("ready") != 0:
            raise Exception("{0} state {1}".format(func_name, state))

        move_dict, cnt = game.get_all_possible_moves(team=team)
        max_points, possible_moves, selected_move = 0, [], None
        for piece_ref, possible_moves in move_dict.items():
            for move_obj in possible_moves:
                points = 0
                possible_moves.append(move_obj)
                if move_obj.take:
                    take_ref = \
                        game.board.positions[move_obj.new_row][move_obj.new_col]
                    points += PIECE_VALUES[game.pieces[take_ref].name]
                resp_moves, cnt2 = game.get_all_possible_moves(team=('white' if team == 'black' else 'black'))
                for mv2_pref, mv2_lst in resp_moves.items():
                    for mv2_obj in mv2_lst:
                        if mv2_obj.take:
                            mv2_take_ref = \
                                game.board.positions[mv2_obj.new_row][mv2_obj.new_col]
                            points -= PIECE_VALUES[game.pieces[mv2_take_ref].name]
                        for mv3_pref, mv3_lst in resp_moves.items():
                            for mv3_obj in mv3_lst:
                                if mv3_obj.take:
                                    mv3_take_ref = \
                                        game.board.positions[mv3_obj.new_row][mv3_obj.new_col]
                                    points -= PIECE_VALUES[game.pieces[mv3_take_ref].name]
                            if points > max_points:
                                max_points, selected_move = points, move_obj

        if not selected_move:
            selected_move = self.pick_rnd(possible_moves, cnt)
        return selected_move
