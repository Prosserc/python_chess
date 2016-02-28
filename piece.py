#!/usr/bin/env python3
"""
Called from python_chess.game
"""
import json
from utils import col_letter_to_no, col_no_to_letter, pos_to_cell_ref, WRONG_ENTRY_POINT_MSG


class Piece(object):
    """
    One instance created for each piece in the game containing all
    of the information and functionality pertaining to that piece.
    """


    def __init__(self, ref, name, team, row, col, piece_moves, move_cnt=0):
        """
        Get attributes required for piece.
        """
        self.ref = ref
        self.name = name
        self.team = team
        self.row = int(row)
        self.col_no = col_letter_to_no(col)
        self.valid_moves = self.get_valid_moves(piece_moves)
        self.move_cnt = move_cnt
        self.taken = False
        self.last_to_move = False

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = self.get_one_space_moves()


    @property
    def col(self):
        return col_no_to_letter(self.col_no)

    @property
    def pos(self):
        return [self.row, self.col_no]

    @property
    def cell_ref(self):
        return pos_to_cell_ref(self.pos)

    @property
    def forward(self):
        return 1 if self.team.lower() == 'white' else -1


    def __to_json(self):
        """
        Output entire object contents as json.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    def get_valid_moves(self, piece_moves):
        """
        Returns all of the moves possible for a piece before
        considerations for the board boundaries, other pieces etc.
        """
        # valid moves for each type of piece:
        # [[-]down, [-]right, <condition1>, ..., <conditionN>]

        # self.forward used to invert direction for black...
        return [[move[0] * self.forward] + move[1:] for move in piece_moves]


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


    def get_offset_pos(self, up, right):
        return [self.row + up, self.col_no + right]


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
