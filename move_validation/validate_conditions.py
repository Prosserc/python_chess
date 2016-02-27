#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, utils
from literals import INVALID_MOVE_MESSAGES as invalid_msg


class ValidateConditions(BaseMoveValidationStep):
    """
    Check if all conditions stored for the move are satisfied.
    The conditions are identified when the piece is created e.g. a
    pawn only being able to move diagonally if taking.
    """


    def perform_check(self):
        ind = [i[:2] for i in self.move_obj.piece.valid_moves].index(self.move_obj.move)
        try:
            conditions = self.move_obj.piece.valid_moves[ind][2:]
        except IndexError:
            self._is_valid = True
            return  # no conditions on move

        # todo - should only need to find one valid move to cont
        for condition in conditions:
            self.debug('Checking condition: {0}'.format(condition),
                       debug_level=utils.DebugLevel.low)

            if condition == 'on_first':
                if self.move_obj.piece.move_cnt > 0:
                    self._invalid_reason = invalid_msg['cond_on_first']
                    return
            elif condition == 'on_take':
                if self.move_obj.new_pos not in self.move_obj.occupied:
                    self._invalid_reason = invalid_msg['cond_on_take']
                    return
                else:
                    # todo - check logic seems iffy
                    self.move_obj.piece.valid_moves.remove(self.move_obj.move + [condition])
            #   T O   F O L L O W . . . (todo)
            elif condition == 'en_passant':
                self._invalid_reason = invalid_msg['cond_en_passant']
                return

        self._is_valid = True
