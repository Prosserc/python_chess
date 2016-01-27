#!/usr/bin/env python
"""
Called from python_chess.game
"""
import json
from utils import col_letter_to_no, WRONG_ENTRY_POINT_MSG


class Piece(object):
    """
    One instance created for each piece in the game containing all
    of the information and functionality pertaining to that piece.
    """


    def __init__(self, ref, name, team, row, col, move_dict):
        """
        Get attributes required for piece.
        """
        self.ref = ref
        self.name = name
        self.team = team
        self.row = int(row)
        self.col = col
        self.pos = [int(row), col_letter_to_no(col)]
        self.valid_moves = self.get_valid_moves(move_dict)
        self.largest = max([max([abs(i) for i in j[:2]]) for j in self.valid_moves])
        self.move_cnt = 0
        self.taken = False

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = self.get_one_space_moves()


    def __to_JSON(self):
        """
        Output entire object contents as json.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    def get_valid_moves(self, move_dict):
        """
        Returns all of the moves possible for a piece before
        considerations for the board boundaries, other pieces etc.
        """
        # valid moves for each type of piece:
        # [[-]down, [-]right, <condition1>, ..., <conditionN>]
        valid_moves = []

        # invert direction for black pieces (as they will move down through rows board)
        if self.team.lower() == 'black':
            for move in move_dict[self.name.lower()]:
                valid_moves.append([move[0] * -1] + move[1:])
        else:
            valid_moves = move_dict[self.name.lower()]
            
        return valid_moves


    def get_one_space_moves(self):
        """
        Defines all one piece moves (needed frequently to calculate the
        steps required to get from A to B).
        """
        one_space_moves = []
        for move in self.valid_moves:
            if min(move[:2]) >= -1 and max(move[:2]) <= 1:
                one_space_moves.append(move)

        return one_space_moves


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)


# TODO - REVIEW:
#  - consider whether storing row / col is the right thing? We do a lot of letter to no
#    conversions and vice versa.
#    Options
#    - Just have rank and file (use properties to calc anything else?
#    - Just have pos?
#    - Move to bitboard to save memory (probably later)