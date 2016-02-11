#!/usr/bin/env python
"""
Called from python_chess.game
"""
from utils import (pos_to_cell_ref, col_no_to_letter, shout, VERBOSE, WRONG_ENTRY_POINT_MSG)


# noinspection PyProtectedMember
# (_file is not protected, just avoids conflict with file)
class Move(object):
    """
    Capture characteristics of actual or potential moves e.g. amount 
    to go up and right, new rank/_file etc. for easy comparison. 
    """


    def __init__(self, piece, up, right, occupied, our_team, their_team,
                 theoretical_move=False, stop_recursion=False):
        """
        Define move attributes, determine if move is possible and the 
        outcomes resulting from the move or an invalid_reason.
        """
        self.piece = piece  # store piece object against move
        self.up = up
        self.right = right

        # not done as properties as these should not move with the piece
        self.rank = piece.rank
        self._file = piece._file

        # REVIEW - pass the following three in as func(s) from Game if need to save RAM
        self.occupied = occupied
        self.our_team = our_team
        self.their_team = their_team

        self.theoretical_move = theoretical_move
        self.stop_recursion = stop_recursion

        # REVIEW - convert to props if need to save ram (used twice so keeping for CPU for now)
        self.our_team_cells = [our_team[piece_ref].pos for piece_ref in our_team]
        self.their_team_cells = [their_team[piece_ref].pos for piece_ref in their_team]

        # initialise variables to be set later...
        self.check, self.take = None, False

        # validate move
        self.possible, self.invalid_reason = self.check_move()

        if not self.possible:
            if VERBOSE and not self.theoretical_move: 
                shout('move not allowed')
        else:
            if VERBOSE and not self.theoretical_move: 
                shout('move allowed')


    @property
    def move(self):
        return [self.up, self.right]

    @property
    def pos(self):
        return [self.rank, self._file]

    @property
    def row(self):
        return self.rank

    @property
    def col(self):
        return col_no_to_letter(self._file)

    @property
    def cell_ref(self):
        return pos_to_cell_ref(self.pos)

    @property
    def new_rank(self):
        return self.rank + self.up

    @property
    def new_file(self):
        return self._file + self.right

    @property
    def new_pos(self):
        return [self.new_rank, self.new_file]

    @property
    def new_row(self):
        return self.new_rank

    @property
    def new_col(self):
        return col_no_to_letter(self.new_file)

    @property
    def new_cell_ref(self):
        return pos_to_cell_ref(self.new_pos)

    @property
    def _id(self):
        """
        Generate unique moveID based on piece_ref being moved and position of every other piece.
        """
        _id = ('mv:' + self.piece.ref + "-" + str(self.rank * self._file) + "-" +
               str(self.new_rank * self.new_file) + ",oth:")
        for ref, piece in self.their_team.items():
            if not piece.taken and ref != self.piece.ref:
                _id = '+'.join([_id, (ref + '-' + str(piece.rank * piece._file))])
        return _id


    def check_move(self):
        """
        Run checks to see whether a move is possible.
        """
        filters = [self.__valid_for_piece,
                   self.__within_boundaries,
                   self.__path_clear,
                   self.__conditions_satisfied,
                   self.__king_safe]

        for func in filters:
            result = func()
            if VERBOSE and not self.theoretical_move:
                print(func.__doc__ + ' - ' + result)
            if result != 'okay':
                return False, result  # stop at first invalid reason for performance
                                      # (most expensive checks last)
        return True, None


    def __valid_for_piece(self):
        """
        Check move against piece.valid_moves
        """
        invalid_msg = 'Move is not allowed for this piece.'
        if VERBOSE and not self.theoretical_move:
            print(str(self.move) + ' in ' + 
                  str([move[:2] for move in self.piece.valid_moves]) + '?')
        if self.move in [move[:2] for move in self.piece.valid_moves]:
            return 'okay'
        return invalid_msg


    def __within_boundaries(self):
        """
        Check if move is possible within board boundaries
        """
        invalid_msg = ('Move is not allowed as it would go outside of ' +
                       'the board boundaries to: ' + self.new_cell_ref)
        if self.new_rank in range(1, 9) and self.new_file in range(1, 9):
            return 'okay'
        return invalid_msg


    def __path_clear(self):
        """
        Check if move is blocked by another piece
        """
        distance = lambda pos1, pos2: sum([abs(pos2[i] - pos1[i]) for i in range(len(pos1))])
        max_steps = 8
        current_step = 0

        # take steps by taking min distance to destination after each
        # of the possible one step moves

        # check steps for pieces cannot jump move more than one space
        if not self.piece.allowed_to_jump:
            tmp_pos = self.pos
            while tmp_pos != self.new_pos:
                # get all possible destination cells after a one space step
                poss_steps = [  # REVIEW - can we simplify this expression
                    [tmp_pos[0] + up, tmp_pos[1] + right]
                    for up, right in [mv[:2] for mv in self.piece.one_space_moves]
                    if tmp_pos[0] + up in range(1, 9) and tmp_pos[1] + right in range(1, 9)]
                if VERBOSE and not self.theoretical_move:
                    print('Possible steps: ' + ', '.join(str(i) for i in poss_steps))

                distances = [distance(i, self.new_pos) for i in poss_steps]
                if VERBOSE and not self.theoretical_move:
                    print('Distances: ' + ', '.join(str(i) for i in distances))

                correct_step = poss_steps[distances.index(min(distances))]
                if VERBOSE and not self.theoretical_move:
                    print('Min dist: ' + str(min(distances)))
                    print('Correct step: ' + str(correct_step))

                tmp_pos = correct_step
                if VERBOSE and not self.theoretical_move:
                    print('tmp_pos: ' + str(tmp_pos))

                # check if cell on the way is occupied
                if tmp_pos in self.occupied:
                    final_step = (tmp_pos == self.new_pos)
                    # if it's not the final position or they are in our team block
                    if (not final_step) or (tmp_pos in self.our_team_cells):
                        invalid_msg = 'This move is blocked as {0} is occupied.'.format(
                            self.cell_ref)
                        return invalid_msg
                    # also block if it is pawn going straight forward
                    elif (self.piece.name == 'pawn') and (self.right == 0):
                        invalid_msg = ('Pawns cannot move straight forward ' +
                                       'when obstructed by another piece.')
                        return invalid_msg
                    # if on final step and above two don't apply then you can take
                    elif tmp_pos == self.new_pos:
                        self.take = True

                current_step += 1
                if current_step >= max_steps:
                    break

        # allow for knights
        else: 
            if self.new_pos in self.our_team_cells:
                invalid_msg = ('This move is blocked as ' + self.new_cell_ref +
                               ' is occupied by your team.')
                return invalid_msg
            elif self.new_pos in self.their_team_cells:
                self.take = True

        return 'okay'


    def __conditions_satisfied(self):
        """
        Check if all conditions stored for the move are satisfied.
        The conditions are identified when the piece is created e.g. a
        pawn only being able to move diagonally if taking.
        """
        ind = [i[:2] for i in self.piece.valid_moves].index(self.move)
        try:
            conditions = self.piece.valid_moves[ind][2:]
        except IndexError:
            return 'okay'  # no conditions on move

        for condition in conditions:
            if VERBOSE and not self.theoretical_move:
                print('Checking condition: ' + str(condition))
            
            if condition == 'on_first':
                if self.piece.move_cnt > 0:
                    invalid_msg = ("A pawn can only move two spaces on it's " +
                                   "first move.")
                    return invalid_msg
            elif condition == 'on_take':
                if self.new_pos not in self.occupied:
                    invalid_msg = 'A pawn can only move diagonally when taking.'
                    return invalid_msg
                else:
                    self.piece.valid_moves.remove(self.move + [condition])
            #   T O   F O L L O W . . . (todo)
            elif condition == 'en_passant':
                invalid_msg = "Sorry " + condition + " rule not coded yet."
                return invalid_msg
        return 'okay'


    def __king_safe(self):
        """
        Check if a move would put your king in check
        """
        # define base case as the move object is created recursively below
        invalid_msg = None
        if self.stop_recursion:
            return 'okay'

        # need to temporarily update piece object, so that all of the theoretical
        # moves checked below will recognise the new position (i.e. as if you had
        # made the move).
        self.piece.rank, self.piece._file = self.new_rank, self.new_file
        if self.take:
            take_ref = [ref for ref in self.their_team.keys() 
                        if self.their_team[ref].pos == self.new_pos][0]
            taken_piece = self.their_team[take_ref]
            if taken_piece.name != 'king':
                del self.their_team[take_ref]
        self.occupied[self.occupied.index([self.rank, self._file])] = (
            [self.new_rank, self.new_file])

        if self.piece.team == 'white':
            our_king, their_king = self.our_team['wK'], self.their_team['bK']
        else:
            our_king, their_king = self.our_team['bK'], self.their_team['wK']

        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for ref, their_piece in self.their_team.items(): 
            up = our_king.row - their_piece.row
            right = our_king._file - their_piece._file
            # reverse our_team and their team args to switch
            theoretical_move = Move(their_piece, up, right, self.occupied, 
                                    self.their_team, self.our_team, 
                                    theoretical_move=True,
                                    stop_recursion=True)
            if theoretical_move.possible:
                invalid_msg = ('You cannot move to this space as it would put ' +
                               'your king in check with the ' + their_piece.name +
                               ' in cell ' + theoretical_move.cell_ref)
                break  # cannot return here as need to revert position etc.
            del theoretical_move

        # revert piece to original position
        self.piece.rank, self.piece._file = self.rank, self._file # revert to original pos
        self.occupied[self.occupied.index(self.new_pos)] = [self.rank, self._file]
        if self.take:
            self.occupied.append(self.new_pos)  # re-instate taken piece
            # noinspection PyUnboundLocalVariable
            if taken_piece.name != 'king':
                # noinspection PyUnboundLocalVariable
                self.their_team[take_ref] = taken_piece


        if not invalid_msg:
            return 'okay'
        return invalid_msg


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
