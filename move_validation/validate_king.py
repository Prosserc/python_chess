#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, INVALID_MSG
from move import Move
from copy import deepcopy


class ValidateKing(BaseMoveValidationStep):
    """
    Check if a move would leave the player's king in check
    """


    def perform_check(self):
        self._is_valid = True

        # define base case as the move object is created recursively below
        if self.move_obj.stop_recursion:
            return

        # need to temporarily update move to see if it puts king in danger. Updating a tmp copy
        tmp_move_obj = deepcopy(self.move_obj)

        # reflect move in position
        tmp_move_obj.piece.row = self.move_obj.new_row
        tmp_move_obj.piece.col_no = self.move_obj.new_col_no

        # update occupied to reflect new position
        occ_index = tmp_move_obj.occupied.index(tmp_move_obj.pos)
        tmp_move_obj.occupied[occ_index] = tmp_move_obj.new_pos

        # if taking anything adjust their_team and occupied accordingly
        if tmp_move_obj.take:
            taken_piece = [piece for _, piece in tmp_move_obj.their_team.items()
                           if piece.pos == tmp_move_obj.new_pos][0]
            if taken_piece.name != 'king':
                del tmp_move_obj.their_team[taken_piece.ref]
                tmp_move_obj.occupied.remove(taken_piece.pos)


        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for _, their_piece in tmp_move_obj.their_team.items():
            self._create_theoretical_move(their_piece, tmp_move_obj)


    def _create_theoretical_move(self, their_piece, tmp_move_obj):

        # work out move required to get to our king...
        our_king_ref = 'wK' if tmp_move_obj.piece.team == 'white' else 'bK'
        our_king = tmp_move_obj.our_team[our_king_ref]
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
            self._invalid_reason = INVALID_MSG['king'].format(their_piece.name,
                                                              theoretical_move.cell_ref)
            return
        del theoretical_move
