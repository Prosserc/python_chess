#!/usr/bin/env python3
from enum import Enum


class PlayerType(Enum):
    human = 0,
    ai = 1


class Player(object):


    def __init__(self, player_type, move_func):
        self.player_type = player_type
        self.move_func = move_func


    def take_move(self):
        self.move_func()
