#!/usr/bin/env python3
"""
Called from python_chess.game
"""
from utils import (pos_to_cell_ref, col_no_to_letter, shout, debug, DebugLevel, WRONG_ENTRY_POINT_MSG)


class Move(object):
    """
    Capture characteristics of actual or potential moves e.g. amount 
    to go up and right, new row/col_no etc. for easy comparison.
    """


    def __init__(self, piece, up, right, occupied, our_team, their_team,
                 theoretical_move=False, stop_recursion=False):
        """
        Define move attributes, determine if move is possible and the 
        outcomes resulting from the move or an invalid_reason.
        """
        self.piece = piece  # store piece object against move
        self.up = up
        self.right = right

        # not done as properties as these should not move with the piece
        self.row = piece.row
        self.col_no = piece.col_no

        # REVIEW - pass the following three in as func(s) from Game if need to save RAM
        self.occupied = occupied
        self.our_team = our_team
        self.their_team = their_team

        self.theoretical_move = theoretical_move
        self.stop_recursion = stop_recursion

        # REVIEW - convert to props if need to save ram (used twice so keeping for CPU for now)
        self.our_team_cells = [our_team[piece_ref].pos for piece_ref in our_team]
        self.their_team_cells = [their_team[piece_ref].pos for piece_ref in their_team]

        # initialise variables to be set later...
        self.take, self.check, self.checkmate = False, False, False

        # validate move
        self.possible, self.invalid_reason = self.__check_move()

        if not self.possible:
            debug('move not allowed', print_func=shout,
                  filter_func=lambda: not self.theoretical_move)
        else:
            debug('move allowed', print_func=shout,
                  filter_func=lambda: not self.theoretical_move)


    @property
    def move(self):
        return [self.up, self.right]

    @property
    def pos(self):
        return [self.row, self.col_no]

    @property
    def col(self):
        return col_no_to_letter(self.col_no)

    @property
    def cell_ref(self):
        return pos_to_cell_ref(self.pos)

    @property
    def new_row(self):
        return self.row + self.up

    @property
    def new_col_no(self):
        return self.col_no + self.right

    @property
    def new_pos(self):
        return [self.new_row, self.new_col_no]

    @property
    def new_col(self):
        return col_no_to_letter(self.new_col_no)

    @property
    def new_cell_ref(self):
        return pos_to_cell_ref(self.new_pos)

    @property
    def is_theoretical_move(self):
        return self.theoretical_move

    @property
    def _id(self):
        """
        Generate unique moveID based on piece_ref being moved and position of every other piece.
        """
        _id = ('mv:' + self.piece.ref + "-" + str(self.row * self.col_no) + "-" +
               str(self.new_row * self.new_col_no) + ",oth:")
        for ref, piece in self.their_team.items():
            if not piece.taken and ref != self.piece.ref:
                _id = '+'.join([_id, (ref + '-' + str(piece.row * piece.col_no))])
        return _id


    def __check_move(self):
        """
        Run checks to see whether a move is possible.
        """
        # review - think about whether we could / should discover all
        #          BaseMoveValidationStep subclasses dynamically
        from move_validation.validate_piece import ValidatePiece
        from move_validation.validate_boundaries import ValidateBoundaries
        from move_validation.validate_path import ValidatePath
        from move_validation.validate_conditions import ValidateConditions
        from move_validation.validate_king import ValidateKing

        validation_steps = [ValidatePiece(self),
                            ValidateBoundaries(self),
                            ValidatePath(self),
                            ValidateConditions(self),
                            ValidateKing(self)]

        for validation_step in validation_steps:
            validation_step.perform_check()
            debug("{0} - is valid: {1}".format(validation_step.__doc__, validation_step.is_valid),
                  level = DebugLevel.low, filter_func=lambda: not self.theoretical_move)
            if not validation_step.is_valid:
                # stop at first invalid reason for performance (most expensive checks last)
                return validation_step.is_valid, validation_step.invalid_reason
        return True, None


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
