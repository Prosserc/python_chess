#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep
from move import Move
from literals import INVALID_MOVE_MESSAGES as invalid_msg
from copy import deepcopy


class ValidateKing(BaseMoveValidationStep):
    """
    Check if a move would put your king in check
    """


    def perform_check(self):
        self._is_valid = True
        self._team = self.move_obj.piece.team

        # need to temporarily update move to see if it puts king in danger. Updating a tmp copy
        tmp_move_obj = deepcopy(self.move_obj)

        # define base case as the move object is created recursively below
        if tmp_move_obj.stop_recursion:
            return

        # reflect move in position
        tmp_move_obj.piece.row = self.move_obj.new_row
        tmp_move_obj.piece.col_no = self.move_obj.new_col_no

        # update occupied to reflect new position
        occ_index = tmp_move_obj.occupied.index(tmp_move_obj.pos)
        tmp_move_obj.occupied[occ_index] = (tmp_move_obj.new_pos)

        # if taking anything adjust their_team and occupied accordingly
        if tmp_move_obj.take:
            taken_piece = [piece for ref, piece in tmp_move_obj.their_team.items()
                           if piece.pos == tmp_move_obj.new_pos][0]
            if taken_piece.name != 'king':
                del tmp_move_obj.their_team[taken_piece.ref]
                tmp_move_obj.occupied.remove(taken_piece.pos)


        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for ref, their_piece in tmp_move_obj.their_team.items():
            self._create_theoretical_move(ref, their_piece, tmp_move_obj)


    def _create_theoretical_move(self, ref, their_piece, tmp_move_obj):

        # work out move required to get to our king...
        our_king = tmp_move_obj.our_team[self._our_king_ref]
        up = our_king.row - their_piece.row
        right = our_king.col_no - their_piece.col_no

        # switching teams in the move constructor args to simulate their move...
        theoretical_move = Move(their_piece, up, right, tmp_move_obj.occupied,
                                our_team=tmp_move_obj.their_team,
                                their_team=tmp_move_obj.our_team,
                                theoretical_move=True, stop_recursion=True)

        if theoretical_move.possible:
            # we can't make this move as it would put us in check...
            self._is_valid = False
            self._invalid_reason = invalid_msg['king'].format(their_piece.name,
                                                              theoretical_move.cell_ref)
            return
        del theoretical_move


    @property
    def _our_king_ref(self):
        return 'wK' if self._team == 'white' else 'bK'
