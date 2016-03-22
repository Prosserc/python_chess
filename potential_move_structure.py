#!/usr/bin/env python3
from literals import PIECE_VALUES, CHECK_POINTS, CHECKMATE_POINTS, PAWN_FORWARD_POINTS


class PotentialMove(object):


    def __init__(self, move_obj):
        self.move_obj = move_obj
        self.score = self.get_score


    def get_score(self, game):
        take_ref = game.board.positions[self.move_obj.new_row][self.move_obj.new_col]
        points = PIECE_VALUES[game.pieces[take_ref].name]

        if self.move_obj.checkmate:
            points += CHECKMATE_POINTS
        elif self.move_obj.check:
            points += CHECK_POINTS

        if self.move_obj.piece.name == 'pawn':  # todo consider enum?
            # up can be +/-, multiplying by piece.forward (-1 or 1) will convert to positive
            steps_forward = self.move_obj.piece.forward * self.move_obj.up
            points += PAWN_FORWARD_POINTS * steps_forward

        return points


class PotentialMoveTree(object):


    def __init__(self, game, team, level):
        self.game = game
        self.team = team
        self.level = level
        self.children = [] # list of potential_moves
        self.traversed = False # needed?
        self.expected_score = None # will get best if our team, worst if theirs


    @property
    def best_score_on_level(self):
        max([mv.get_score(self.game)] for mv in self.children])


# move cache?
# -----------
# dict move_id: move, turn, level, @prop relative_lvl
# prune method to clear old relative levels
# (this could store theoretical moves, then have method to convert theoretical move to full - if valid
