#!/usr/bin/env python3
from move_validation.base_move_validation_step import BaseMoveValidationStep, INVALID_MSG
from utils import pos_to_cell_ref


class ValidatePath(BaseMoveValidationStep):
    """
    Check if move is blocked by another piece
    """


    def perform_check(self):
        max_steps = 8
        current_step = 0
        move_obj = self.move_obj

        # take steps by taking min distance to destination after each
        # of the possible one step moves

        # check steps for pieces cannot jump move more than one space
        if not move_obj.piece.allowed_to_jump:
            tmp_pos = move_obj.pos
            while tmp_pos != move_obj.new_pos:
                # get all possible destination cells after a one space step
                poss_steps = [  # REVIEW - can we simplify this expression
                    [tmp_pos[0] + up, tmp_pos[1] + right]
                    for up, right in [mv[:2] for mv in move_obj.piece.one_space_moves]
                    if tmp_pos[0] + up in range(1, 9) and tmp_pos[1] + right in range(1, 9)]
                self.debug('Possible steps: {0}'.format(', '.join(str(i) for i in poss_steps)))

                distances = [ValidatePath.distance(i, move_obj.new_pos) for i in poss_steps]
                self.debug('Distances: {0}'.format(', '.join(str(i) for i in distances)))

                correct_step = poss_steps[distances.index(min(distances))]
                self.debug('Min dist: {0}\nCorrect step: {1}'.format(min(distances), correct_step))

                tmp_pos = correct_step
                self.debug('tmp_pos: {0}'.format(tmp_pos))

                # check if cell on the way is occupied
                if tmp_pos in move_obj.occupied:
                    final_step = (tmp_pos == move_obj.new_pos)
                    # if it's not the final position or they are in our team block
                    if (not final_step) or (tmp_pos in move_obj.our_team_cells):
                        self._invalid_reason = INVALID_MSG['path_gen'].format(
                            pos_to_cell_ref(tmp_pos))
                        return
                    # also block if it is pawn going straight forward
                    elif (move_obj.piece.name == 'pawn') and (move_obj.right == 0):
                        self._invalid_reason = INVALID_MSG['path_pawn']
                        return
                    # if on final step and above two don't apply then you can take
                    elif tmp_pos == move_obj.new_pos:
                        move_obj.take = True

                current_step += 1
                if current_step >= max_steps:
                    break

        # allow for knights
        else:
            if move_obj.new_pos in move_obj.our_team_cells:
                self._invalid_reason = INVALID_MSG['path_knight'].format(move_obj.new_cell_ref)
                return
            elif move_obj.new_pos in move_obj.their_team_cells:
                move_obj.take = True

        self._is_valid = True


    @staticmethod
    def distance(pos1, pos2):
        """
        Distance between two collections, the two position params must be the same length
        :param pos1:
        :param pos2:
        :return: a number representing the distance
        """
        return sum([abs(pos2[i] - pos1[i]) for i in range(len(pos1))])
