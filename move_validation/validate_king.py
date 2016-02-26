#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep
from move import Move
from literals import INVALID_MOVE_MESSAGES as invalid_msg


class ValidateKing(BaseMoveValidationStep):
    """
    Check if a move would put your king in check
    """


    def perform_check(self):
        move_obj = self.move_obj
        self._is_valid = True

        # define base case as the move object is created recursively below
        if move_obj.stop_recursion:
            return

        # need to temporarily update piece object, so that all of the theoretical
        # moves checked below will recognise the new position (i.e. as if you had
        # made the move).
        # TODO - review, consider making a tmp copy of their team to work with instead
        move_obj.piece.row = move_obj.new_row
        move_obj.piece.col_no = move_obj.new_col_no
        if move_obj.take:
            take_ref = [ref for ref in move_obj.their_team.keys()
                        if move_obj.their_team[ref].pos == move_obj.new_pos][0]
            taken_piece = move_obj.their_team[take_ref]
            if taken_piece.name != 'king':
                del move_obj.their_team[take_ref]
        move_obj.occupied[move_obj.occupied.index([move_obj.row, move_obj.col_no])] = (
            [move_obj.new_row, move_obj.new_col_no])

        if move_obj.piece.team == 'white':
            our_king, their_king = move_obj.our_team['wK'], move_obj.their_team['bK']
        else:
            our_king, their_king = move_obj.our_team['bK'], move_obj.their_team['wK']

        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for ref, their_piece in move_obj.their_team.items():
            up = our_king.row - their_piece.row
            right = our_king.col_no - their_piece.col_no
            # reverse our_team and their team args to switch
            theoretical_move = Move(their_piece, up, right, move_obj.occupied,
                                    move_obj.their_team, move_obj.our_team,
                                    theoretical_move=True, stop_recursion=True)
            if theoretical_move.possible:
                self._invalid_reason = invalid_msg['king'].format(their_piece.name,
                                                                  theoretical_move.cell_ref)
                self._is_valid = False
                break  # cannot return here as need to revert position etc.
            del theoretical_move

        # revert piece to original position
        move_obj.piece.row, move_obj.piece.col_no = move_obj.row, move_obj.col_no  # revert to original pos
        move_obj.occupied[move_obj.occupied.index(move_obj.new_pos)] = [move_obj.row, move_obj.col_no]
        if move_obj.take:
            move_obj.occupied.append(move_obj.new_pos)  # re-instate taken piece
            # noinspection PyUnboundLocalVariable
            if taken_piece.name != 'king':
                # noinspection PyUnboundLocalVariable
                move_obj.their_team[take_ref] = taken_piece
