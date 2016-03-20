#!/usr/bin/env python3
"""
Python implementation of chess, main entry point.
"""
import json
from board import Board
from piece import Piece
from move import Move
from literals import PIECE_CODES, DEFAULT_START_POSITIONS, TEAMS, LOGGING
# from chess_engine import pick_move
from utils import shout, write_log, cell_ref_to_pos, pos_to_cell_ref, debug, DebugLevel, \
    set_debugging_level
from copy import deepcopy

LOG = ''


class Game(object):
    """
    Top level class, the game object contains all of the other
    class instances such as the pieces, the board etc.
    """
    move_dict = {'king': [[i, j] for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0],
                 'rook': [[i, 0] for i in range(-8, 9) if i != 0] +
                         [[0, i] for i in range(-8, 9) if i != 0],
                 'bishop': [[i, i] for i in range(-8, 9) if i != 0] +
                           [[i, i * -1] for i in range(-8, 9) if i != 0],
                 'knight': [[i, j] for i in range(-2, 3) for j in range(-2, 3)
                            if abs(i) + abs(j) == 3],
                 'pawn': [[1, i, msg] for i in [-1, 1] for msg in ['on_take', 'en_passant']] +
                         [[2, 0, 'on_first'], [1, 0]]
                 }
    move_dict['queen'] = move_dict['rook'] + move_dict['bishop']

    def __init__(self, turn_limit=200, custom_start_positions=None, default_logging=False):
        """
        Initialise game object and create required member objects
        """
        start_pos = custom_start_positions or deepcopy(DEFAULT_START_POSITIONS)
        # need a copy here otherwise DEFAULT_START_POSITIONS gets changes and reused in next game
        self.logging = default_logging if default_logging else LOGGING

        self.board = Board(start_pos)
        self.pieces = self.__create_pieces(Game.move_dict, start_pos)

        # initialise variables that will be needed later
        self.check = False
        self.checkmate = False
        self.draw = False
        self.turns = 0
        self.current_team = None
        self.last_piece_to_move = None
        self.turn_limit = turn_limit


    def __to_json(self):
        """
        Output entire object contents as json.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


    @staticmethod
    def __create_pieces(move_dict, start_pos):
        """
        Creates a object for each piece and creates a dictionary to
        enable access to the pieces via their ref. 
        The source of this data and the refs is the positions list, in 
        the game object.
        """
        pieces = {}

        for row, row_content in start_pos.items():
            if row > 0:
                for col, piece_ref in row_content.items():
                    if piece_ref:
                        team = TEAMS[piece_ref[0]]
                        name = PIECE_CODES[piece_ref[1]]

                        # doesn't matter what actual move_cnt is, just needs to be >= 1 if moved
                        if DEFAULT_START_POSITIONS[row][col] == start_pos[row][col]:
                            move_cnt = 0
                        else:
                            move_cnt = 1

                        pieces[piece_ref] = Piece(piece_ref, name, team, row, col,
                                                  move_dict[name], move_cnt)
        return pieces


    def take_turn(self, team, prompt=None, move=None):
        """
        Interact with player to facilitate moves, capture data and
        identify/store information common to all potential moves.
        Also includes optional param to specify a prompt to run
        automatically or a move object (for interface from external
        scripts).
        """
        global LOG

        self.turns += 1
        self.current_team = team
        occupied, our_team, their_team = self.get_occupied()
        validated, found_issue = False, False
        if self.check:
            user_feedback = shout('{0} team in check'.format(self.current_team),
                                  print_output=False, return_output=True)
        else:
            user_feedback = None

        # repeat prompt until a valid move is given...
        while not validated:

            # skip set up if a move object is passed in...
            if move:
                piece, up, right = move.piece, move.up, move.right
            else:
                if user_feedback:
                    print(user_feedback + '\n')

                if not prompt:
                    prompt = input("[{0} move] >> ".format(self.current_team))

                piece, up, right, hold_move, user_feedback = \
                    self.__parse_prompt(prompt, our_team)

                if not hold_move:
                    # create object for move, this evaluates potential issues etc.
                    move = Move(piece, up, right, occupied, our_team, their_team)

            if move:
                if move.possible:
                    validated = True
                else:
                    user_feedback = move.invalid_reason
                    move = None  # clear ready for next loop

            prompt = None  # clear ready for next loop

        # noinspection PyUnboundLocalVariable
        self.__process_move(piece, move, up, right, occupied, our_team, their_team)

        # log state of game
        if self.logging:
            LOG = '\n'.join([LOG, self.__to_json()])

        # wrap up if done...
        if self.checkmate or self.turns >= 200:
            if self.turns >= self.turn_limit:
                shout('{0} moves, lets call it a draw'.format(self.turns))
            elif self.checkmate:
                move.checkmate = True
                shout('game over, {0} team wins'.format(self.current_team))
            if self.logging:
                write_log(LOG)


    def __parse_prompt(self, prompt, our_team):
        """
        Determine piece to be moved and move required from prompt.
        """
        # setup return defaults
        piece, up, right, hold_move, user_feedback = None, None, None, True, None

        # first check for special commands
        if prompt.lower()[:5] == 'debug':
            level_text = prompt[5:].strip()
            user_feedback = set_debugging_level(level_text, feedback_required=True)
            return piece, up, right, hold_move, user_feedback
        elif prompt.lower() == 'redraw':
            print(self.board.draw_board())
            return piece, up, right, hold_move, user_feedback
        elif prompt.lower()[:4] == 'list':
            piece_ref_text = prompt[4:].strip()
            piece = self.get_piece(piece_ref_text)
            if piece:
                self.get_all_possible_moves(list_moves=True, pieces={piece.ref: piece})
            else:
                self.get_all_possible_moves(list_moves=True)
            return piece, up, right, hold_move, user_feedback
        elif prompt.lower() == 'log':
            if self.logging:
                write_log(LOG)
                user_feedback = "Log written to current working directory"
            else:
                user_feedback = "Logging not currently enabled, change in literals.py"
            return piece, up, right, hold_move, user_feedback

        # attempt to get details of piece to be moved (first two chars as current cell_ref)
        try:
            current_cell_ref = prompt[:2]
            [cur_row, cur_col_no] = cell_ref_to_pos(current_cell_ref)
            assert(cur_row in range(1, 9) and cur_col_no in range(1, 9))
        except (IndexError, ValueError, AssertionError):
            user_feedback = ('A valid cell for your current position could not be found\n' +
                '(using the first two characters from your entry: "{0}")').format(prompt)
            return piece, up, right, hold_move, user_feedback

        piece_ref = self.board.get_piece_ref(cur_row, cur_col_no)

        if piece_ref:
            piece = self.get_piece(piece_ref)

        try:
            # todo consider more efficient ways to achieve the same
            assert ([cur_row, cur_col_no] in [our_team[obj].pos for obj in our_team])
        except AssertionError:
            user_feedback = ('A piece in your team could not be found in cell: {0}\n' +
                '(using the first two characters from your entry)').format(current_cell_ref)
            return piece, up, right, hold_move, user_feedback

        # use last two characters as new cell_ref
        try:
            [new_row, new_col_no] = cell_ref_to_pos(prompt[-2:])
        except ValueError:
            user_feedback = (
                'A valid new cell could not be identified from your input: {0}'.format(prompt))
            return piece, up, right, hold_move, user_feedback

        up, right = new_row - cur_row, new_col_no - cur_col_no

        debug('piece_ref: {0} | up: {1} | right: {2}'.format(piece.ref, up, right),
              DebugLevel.mid)

        # attempt to get destination...
        try:
            assert up in range(-8, 9) and right in range(-8, 9)
        except AssertionError:
            user_feedback = (
                'A valid new cell could not be identified from your input: {0}'.format(prompt))
            return piece, up, right, hold_move, user_feedback

        hold_move = False
        return piece, up, right, hold_move, user_feedback


    def get_occupied(self):
        """
        Produce list of occupied cells and current teams, pieces.
        """
        occupied, our_team, their_team = [], {}, {}
        # iterate through piece objects in pieces dictionary
        for ref, piece in self.pieces.items():
            if not piece.taken:
                occupied.append(piece.pos)
                # build up dict of piece objects for each team
                if piece.team == self.current_team:
                    our_team[ref] = piece
                else:
                    their_team[ref] = piece
        return occupied, our_team, their_team


    def __process_move(self, piece, move, up, right, occupied, our_team, their_team):
        """
        Execute and updates required as a result of a valid move.
        """
        # update piece attributes
        global taken_piece
        occupied.remove(piece.pos)
        piece.move_cnt += 1
        piece.row += up
        piece.col_no += right
        occupied.append(piece.pos)

        # check if anything was taken
        if move.take:
            # get ref of taken piece BEFORE board update
            taken_piece_ref = self.board.get_piece_ref(move.new_row, move.new_col_no)
            taken_piece = self.get_piece(taken_piece_ref)
            taken_piece.taken = True
            assert self.get_piece(taken_piece.ref).taken  # todo -replace with unit test
            shout('taken piece: {0}'.format(taken_piece.ref))

        # update board
        self.board.update_board(move.pos, move.new_pos, piece.ref)
        print(self.board.draw_board())

        assert our_team[piece.ref].pos == piece.pos  # todo -replace with unit test
        if move.take:
            assert their_team[taken_piece.ref].taken

        # other player in check?
        self.check = self.__in_check(piece, occupied, our_team, their_team)
        if self.check:
            move.check = True
            other_team = ('black' if self.current_team == 'white' else 'white')
            shout(other_team + ' team in check')
            debug('looking for checkmate....\n')

            # other player in checkmate?
            self.checkmate = self.__in_checkmate(occupied, our_team, their_team)

        last_piece = self.get_piece(self.last_piece_to_move)
        if last_piece:
            last_piece.last_to_move = False
        move.piece.last_to_move = True


    def __in_check(self, piece, occupied, our_team, their_team):
        """
        Determine whether the opponent's king is in check, done by
        creating a theoretical_move from the attaching piece's current 
        position to their King's position to see if the move would be 
        valid.
        """
        debug('Checking if other player is in check...', DebugLevel.mid)

        # work out move required to get to their king
        their_king = (self.get_piece('wK') if self.current_team == 'black'
                      else self.get_piece('bK'))
        up = their_king.row - piece.row
        right = their_king.col_no - piece.col_no
        debug('..possible to move ' + piece.ref + ' from ' +
              str(piece.pos) + ' to ' + str(their_king.pos) + '?', DebugLevel.mid)
        theoretical_move = Move(piece, up, right, occupied, our_team,
                                their_team, theoretical_move=True)
        if theoretical_move.possible:
            return True
        else:
            debug('..invalid_reason: ' + theoretical_move.invalid_reason, DebugLevel.mid)
            return False


    def __in_checkmate(self, occupied, our_team, their_team):
        """
        Determine whether the opponents king is in checkmate, done
        by creating many theoretical moves for each piece on the  
        opponents team to see if any are valid i.e. end with their 
        king not in check.
        """
        for ref, piece in their_team.items():
            # call one piece at a time to stop after first piece found with
            # possible moves
            p_dict = {ref: piece}
            # intentionally reverse our team and their team params as 
            # we want to simulate all possible moves for opponent
            all_moves, cnt = self.get_all_possible_moves(occupied=occupied,
                                                         our_team=their_team,
                                                         their_team=our_team,
                                                         pieces=p_dict)
            if cnt > 0:
                print("Not checkmate (type list at prompt if you want to " +
                      "display all possible moves)")
                return False
        return True


    def get_all_possible_moves(self, occupied=None, our_team=None,
                               their_team=None, pieces=None,
                               list_moves=False, team=None):
        """
        Try all of the valid moves for the pieces passed in, pieces
        arg should be a dictionary of piece objects with piece_ref as 
        their key. Return a dictionary with same keys, where value is 
        a list containing a move object for each possible move for
        that piece (can be[]).
        If occupied, our_team or their_team are not supplied a new call
        is made to self.get_occupied.
        If pieces is not supplied this is defaulted to our_team.
        Team param is picked up from game object when not supplied.
        """
        # get defaults if args missing
        if team:
            self.current_team = team
        if (not occupied) or (not our_team) or (not their_team):
            occupied, our_team, their_team = self.get_occupied()
        if not pieces:
            pieces = our_team

        all_possible_moves, cnt = {}, 0
        for ref, piece in iter(sorted(pieces.items())):
            tmp_moves = []
            for potential_move in piece.valid_moves:
                [up, right] = potential_move[:2]
                try:
                    theoretical_move = Move(piece, up, right, occupied, our_team,
                                            their_team, theoretical_move=True)
                    if theoretical_move.possible:
                        tmp_moves.append(theoretical_move)
                        cnt += 1
                except KeyError:
                    pass
                finally:
                    del theoretical_move

            if len(tmp_moves) > 0:
                all_possible_moves[ref] = tmp_moves

        if list_moves:
            print('\nPossible moves:')
            for ref, moves in iter(sorted(all_possible_moves.items())):
                piece = self.get_piece(ref)
                piece_text = "{0} in {1} to".format(piece.name, piece.cell_ref).rjust(17)
                possible_destinations = sorted([pos_to_cell_ref(obj.new_pos) for obj in moves])
                print("{0}:  {1}".format(piece_text, ', '.join(possible_destinations)))

        return all_possible_moves, cnt


    def get_piece(self, piece_ref):
        """
        Takes a piece_ref e.g. 'wp1' and returns the corresponding piece object
        """
        try:
            return self.pieces[piece_ref]
        except KeyError:
            return None


if __name__ == '__main__':
    import api
    api.main()


    #  N O T E S :
    #  =========

    #  Performance:
    #    - load all possible moves for each player at the start of each turn so
    #      that they are already know by the time the player comes to move?
    #      - if doing this would need a keyboardinterupt exception???
    #        To pick up cases when the user was ready to make their move before
    #        all possible moves had been pre-loaded (then just get moves for the
    #        piece they select) e.g.:
    #        http://stackoverflow.com/questions/7180914/pause-resume-a-python-script-in-middle
    #    - LOGGING needs to be fully written (lazy implementation at present)
