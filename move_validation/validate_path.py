#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, debug, DebugLevel
from move import Move


class ValidsatePath(BaseMoveValidationStep):
"""
Validation step to ensure that no pieces are blocking the move
"""


    def __init__(self, move_obj):
        if isinstance(move_obj, Move):
            self.move = move_obj
        else:
            raise TypeError("A move object is required to initialise this class")

        self._is_valid = False
        self._invalid_reason = "Validation not yet performed"


    def perform_check(self):
        MAX_STEPS = 8
        current_step = 0

        # take steps by taking min distance to destination after each
        # of the possible one step moves

        # check steps for pieces cannot jump move more than one space
        if not self.move.piece.allowed_to_jump:
            tmp_pos = self.move.pos
            while tmp_pos != self.move.new_pos:
                # get all possible destination cells after a one space step
                poss_steps = [  # REVIEW - can we simplify this expression
                    [tmp_pos[0] + up, tmp_pos[1] + right]
                    for up, right in [mv[:2] for mv in self.move.piece.one_space_moves]
                    if tmp_pos[0] + up in range(1, 9) and tmp_pos[1] + right in range(1, 9)]
                debug('Possible steps: {0}'.format(', '.join(str(i) for i in poss_steps)),
                      level=DebugLevel.mid, filter_func=lambda: not self.move.theoretical_move)

                distances = [distance(i, self.move.new_pos) for i in poss_steps]
                debug('Distances: {0}'.format(', '.join(str(i) for i in distances)),
                      level=DebugLevel.mid, filter_func=lambda: not self.move.theoretical_move)

                correct_step = poss_steps[distances.index(min(distances))]
                debug('Min dist: {0}\nCorrect step: {1}'.format(min(distances), correct_step),
                      level=DebugLevel.mid, filter_func=lambda: not self.move.theoretical_move)

                tmp_pos = correct_step
                debug('tmp_pos: {0}'.format(tmp_pos), level=DebugLevel.mid,
                      filter_func=lambda: not self.move.theoretical_move)

                # check if cell on the way is occupied
                if tmp_pos in self.move.occupied:
                    final_step = (tmp_pos == self.move.new_pos)
                    # if it's not the final position or they are in our team block
                    if (not final_step) or (tmp_pos in self.move.our_team_cells):
                        self._invalid_reason = 'This move is blocked as {0} is occupied.'.format(
                            self.move.cell_ref)
                        return
                    # also block if it is pawn going straight forward
                    elif (self.move.piece.name == 'pawn') and (self.move.right == 0):
                        self._invalid_reason = ('Pawns cannot move straight forward ' +
                                                'when obstructed by another piece.')
                        return
                    # if on final step and above two don't apply then you can take
                    elif tmp_pos == self.move.new_pos:
                        self.move.take = True

                current_step += 1
                if current_step >= MAX_STEPS:
                    break

        # allow for knights
        else:
            if self.move.new_pos in self.move.our_team_cells:
                self._invalid_reason = ('This move is blocked as ' + self.move.new_cell_ref +
                                        ' is occupied by your team.')
            elif self.move.new_pos in self.move.their_team_cells:
                self.move.take = True

        self._is_valid


    @staticmethod
    def distance(pos1, pos2):
        """
        Distance between two collections, the two position params must be the same length
        :param pos1:
        :param pos2:
        :return: a number representing the distance
        """
        return sum([abs(pos2[i] - pos1[i]) for i in range(len(pos1))])


    def is_valid(self):
        return self._is_valid


    def invalid_reason(self):
        return None if self.is_valid else self._invalid_reason