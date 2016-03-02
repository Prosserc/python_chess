#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, INVALID_MSG


class ValidatePiece(BaseMoveValidationStep):
    """
    Check move against piece.valid_moves
    """


    def perform_check(self):
        """
        Performs the check and sets up is_valid and invalid_reason properties
        :return: None
        """
        if self.move_obj.move in [move[:2] for move in self.move_obj.piece.valid_moves]:
            self._is_valid = True
        else:
            self._invalid_reason = INVALID_MSG['piece']
