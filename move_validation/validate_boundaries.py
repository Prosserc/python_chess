#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, INVALID_MSG


class ValidateBoundaries(BaseMoveValidationStep):
    """
    Check if move is possible within board boundaries
    """


    def perform_check(self):
        if self.move_obj.new_row in range(1, 9) and self.move_obj.new_col_no in range(1, 9):
            self._is_valid = True
        else:
            self._invalid_reason = INVALID_MSG['boundaries'].format(self.move_obj.new_cell_ref)
