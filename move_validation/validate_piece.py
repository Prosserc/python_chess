#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, debug, DebugLevel
from move import Move


class ValidatePiece(BaseMoveValidationStep):
"""
Validation step to ensure that the move requests is valid for the relevant piece
"""


    def __init__(self, move_obj):
        """
        :param move_obj: The move object to be validated
        :return: None
        """
        if isinstance(move_obj, Move):
            self.move = move_obj
        else:
            raise TypeError("A move object is required to initialise this class")

        self._is_valid = False
        self._invalid_reason = "Validation not yet performed"


    def perform_check(self):
        """
        Performs the check and sets up is_valid and invalid_reason properties
        :return: None
        """
        if self.move in [move[:2] for move in self.piece.valid_moves]:
            self._is_valid = True
        else:
            self._invalid_reason = 'Move is not allowed for this piece.'
            self._is_valid = False


    def is_valid(self):
        return self._is_valid


    def invalid_reason(self):
        return None if self.is_valid else self._invalid_reason