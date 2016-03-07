#!/usr/bin/env python3
from enum import Enum


class PlayerType(Enum):
    human = 0,
    ai = 1


class Player(object):


    def __init__(self, player_type, team, game, pre_move_func=None):
        """
        :param player_type: must be of type player.PlayerType
        :param team: 'white' or 'black'
        :param game: must be of type game.Game
        :param pre_move_func: a function to be called before the turn to generate a move_obj
        """
        self.player_type = player_type
        self.team = team
        self.game = game
        self.move_func = self.game.take_turn
        self.pre_move_func = pre_move_func


    def take_move(self):
        move=None
        if self.pre_move_func:
            move = self.pre_move_func(self.game, self.team)
        self.move_func(team=self.team, move=move)
