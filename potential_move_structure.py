#!/usr/bin/env python3

# potential move:
# --------------
# * move, score,

# move cache?
# -----------
# dict move_id: move, turn, level, @prop relative_lvl
# prune method to clear old relative levels
# (this could store theoretical moves, then have method to convert theoretical move to full - if valid

# potential move level:
# -------------------------
# * game_obj,
# * coll of child moves (order by score?) - could look at most promoising branches first?
# * parent? - leave for now
# * traversed marker?
# * team?
# * tree level?


class PotentialMove(object):


    def __init__(self, move_obj):
        self.move_obj = move_obj
        self.score = self.get_score


    def get_score(self):
        #to follow


class PotentialMoveTree(object):


    def __init__(self, game, team, level):
        self.game = game
        self.team = team
        self.level = level
        self.children = [] # list of potential_moves
        self.traversed = False
        self.expected_score = None # will get best if our team, worst if theirs

