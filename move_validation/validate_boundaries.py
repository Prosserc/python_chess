#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, debug, DebugLevel
from move import Move


class ValidsateBoundaries(BaseMoveValidationStep):
"""
Validation step to ensure that the piece would remain within the board boundaries
"""


    def __init__(self, move_obj):
        if isinstance(move_obj, Move):
            self.move = move_obj
        else:
            raise TypeError("A move object is required to initialise this class")

        self._is_valid = False
        self._invalid_reason = "Validation not yet performed"


    def perform_check(self):
        if self.new_row in range(1, 9) and self.new_col_no in range(1, 9):
            self._is_valid = True
        else:
            self._invalid_reason = ('Move is not allowed as it would go outside of ' +
                                    'the board boundaries to: ' + self.new_cell_ref)
            self._is_valid = False


    def is_valid(self):
        return self._is_valid


    def invalid_reason(self):
        return None if self.is_valid else self._invalid_reason