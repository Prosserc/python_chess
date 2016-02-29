#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, utils
from literals import INVALID_MOVE_MESSAGES as invalid_msg, DEFAULT_START_POSITIONS


class ValidateConditions(BaseMoveValidationStep):
    """
    Check if all conditions stored for the move are satisfied e.g. a pawn is only
    able to move diagonally if taking.
    """


    def perform_check(self):
        potential_moves = [mv for mv in self.move_obj.piece.valid_moves
                           if mv[:2] == self.move_obj.move[:2]]

        # attempt to find on valid move where there is condition or the condition is satisfied
        for move in potential_moves:

            if self._move_has_a_condition(move):
                condition = move[2]
                self.debug('Checking condition: {0}'.format(condition),
                           debug_level=utils.DebugLevel.low)

                if self._condition_is_valid(condition):
                    self._is_valid = True
                    return
                else:
                    self._invalid_reason = invalid_msg["cond_{0}".format(condition)]
                    self._is_valid = False

            else:
                self._is_valid = True
                return


    def _condition_is_valid(self, condition):
        condition_outcomes = {
            'on_first': self._on_first_applies,
            'on_take': self._on_take_applies,
            'en_passant': self._en_passant_applies
        }
        return condition_outcomes[condition]


    @property
    def _on_first_applies(self):
        return self.move_obj.piece.move_cnt == 0


    @property
    def _on_take_applies(self):
        return self.move_obj.new_pos in [pos for pos in self.move_obj.occupied]


    @property
    def _en_passant_applies(self):

        #set up
        target_pos = self.move_obj.piece.get_offset_pos(0, self.move_obj.right)
        target_piece = None
        for ref, piece in self.move_obj.their_team.items():
            if piece.pos == target_pos and piece.name == "pawn":
                target_piece = piece

        # an opponent pawn is directly to your side (in the direction you are trying to move)...
        if not target_piece:
            self.debug('En Passant condition - no pawn in required position')
            return False

        # and was the last to move...
        if not target_piece.last_to_move:
            self.debug('En Passant condition - the opposition pawn was not the not last to move')
            return False

        # and it was on their first move...
        if target_piece.move_cnt > 1:
            self.debug('En Passant condition - the opposition pawn had taken more than one move')
            return False

        # and is two squares up/down from where they started...
        row_before_last_move = target_piece.row - (2 * target_piece.forward)
        original_contents_of_cell = DEFAULT_START_POSITIONS[row_before_last_move][target_piece.col]
        if original_contents_of_cell != target_piece.ref:
            self.debug('En Passant condition - the opposition pawn moved two spaces forward')
            return False

        return True



    @staticmethod
    def _move_has_a_condition(move):
        return len(move) > 2
