#!/usr/bin/env python
"""
Python implementation of chess, main entry point.
"""
import json
from board import Board
from piece import Piece
from move import Move
from literals import PIECE_CODES, START_POSITIONS, TEAMS
# from chess_engine import pick_move
from utils import (shout, write_log, cell_ref_to_pos, pos_to_cell_ref,
                   col_letter_to_no, col_no_to_letter, format_msg, VERBOSE)

# constants
LOGGING = False
LOG = ''
MOVE_INSTRUCTIONS = format_msg("\nTo specify a move enter the cell reference for the piece you "
       "want to move and the cell reference for the new location. The first two characters of "
       "your prompt entry are used to identify the current cell and the last two for the new "
       "cell e.g. to move from A2 to A4 you could enter 'A2, A4' or use shorthand of 'a2a4'.")


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

    def __init__(self):
        """
        Initialise game object and create required member objects
        """

        self.board = Board(START_POSITIONS)
        self.pieces = self.__create_pieces(Game.move_dict)

        # initialise variables that will be needed later
        self.check = False
        self.checkmate = False
        self.draw = False
        self.turns = 0
        self.current_team = None

    def __to_json(self):
        """
        Output entire object contents as json.
        """
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    @staticmethod
    def __create_pieces(move_dict):
        """
        Creates a object for each piece and creates a dictionary to
        enable access to the pieces via their ref. 
        The source of this data and the refs is the positions list, in 
        the game object.
        """
        pieces = {}

        for row, row_content in START_POSITIONS.items():
            if row > 0:
                for col, piece_ref in row_content.items():
                    if piece_ref:
                        team = TEAMS[piece_ref[0]]
                        name = PIECE_CODES[piece_ref[1]]
                        pieces[piece_ref] = Piece(piece_ref, name, team, row, col, move_dict)
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
            user_feedback = shout(team + ' team in check',
                                  print_output=False, return_output=True)
        else:
            user_feedback = None

        # repeat prompt until a valid move is given...
        while not validated:
            # skip set up if a move object is passed in...
            if move:
                piece, up, right = move.piece, move.up, move.right
            else:
                if not prompt:
                    print(self.board.draw_board())
                    if user_feedback:
                        print(user_feedback + '\n')
                    prompt = input("[" + team + " move] >> ")

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
        if LOGGING:
            LOG = '\n'.join([LOG, self.__to_json()])

        # wrap up if done...
        if self.checkmate or self.turns >= 200:
            if self.turns >= 200:  # TODO - replace with self.draw once draw rules done
                shout(str(self.turns) + ' moves, lets call it a draw')
            elif self.checkmate:
                shout('game over, ' + self.current_team + ' team wins')
            if LOGGING:
                write_log(LOG)
            input('\nPress enter to close game...')
            raise Exception('Game Finished')

    def __parse_prompt(self, prompt, our_team):
        """
        Determine piece to be moved and move required from prompt.
        """
        global VERBOSE
        # setup return defaults
        piece, up, right, hold_move, user_feedback = None, None, None, True, None

        # first check for special commands
        if prompt.lower()[:5] == 'debug':
            VERBOSE = not VERBOSE
            user_feedback = "Debugging {0}".format("on" if VERBOSE else "off")
            return piece, up, right, hold_move, user_feedback
        elif prompt.lower() == 'redraw':
            print(self.board.draw_board())
            return piece, up, right, hold_move, user_feedback
        elif prompt.lower()[:4] == 'list':
            self.get_all_possible_moves(list_moves=True)
            return piece, up, right, hold_move, user_feedback

        # attempt to get details of piece to be moved (first two chars as current cell_ref)
        current_cell_ref = prompt[:2]
        [cur_rank, cur_file] = cell_ref_to_pos(current_cell_ref)
        piece_ref = self.board.get_piece_ref(cur_rank, cur_file)

        if piece_ref:
            piece = self.pieces[piece_ref]

        try:
            # todo consider more efficient ways to achieve the same
            assert ([cur_rank, cur_file] in [our_team[obj].pos for obj in our_team])
        except AssertionError:
            user_feedback = (
                'A piece in your team could not be found in cell: {0}\n' +
                '(using the first two characters from your entry)').format(current_cell_ref)
            return piece, up, right, hold_move, user_feedback

        # use last two characters as new cell_ref
        [new_rank, new_file] = cell_ref_to_pos(prompt[-2:])
        up, right = new_rank - cur_rank, new_file - cur_file

        if VERBOSE:
            print('piece_ref: {0} | up: {1} | right: {2}'.format(piece.ref), str(up), str(right))

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
        piece.col = col_no_to_letter(col_letter_to_no(piece.col) + right)
        piece.pos = [piece.row, col_letter_to_no(piece.col)]
        occupied.append(piece.pos)

        # check if anything was taken
        if move.take:
            # get ref of taken piece BEFORE board update
            taken_piece_ref = self.board.get_piece_ref(move.new_rank, move.new_file)
            taken_piece = self.pieces[taken_piece_ref]
            taken_piece.taken = True
            # tmp TEST - check piece updated is object from game ###
            assert self.pieces[taken_piece.ref].taken
            ########################################################
            if VERBOSE:
                shout('taken piece: ' + taken_piece.ref)

        # update board
        self.board.update_board(move.pos, move.new_pos, piece.ref)

        # tmp TEST - see if refresh of get_occupied is needed #############
        assert our_team[piece.ref].pos == piece.pos
        if move.take:
            assert their_team[taken_piece.ref].taken
        # occupied, our_team, their_team = self.get_occupied() # refresh
        ###################################################################

        # other player in check?
        self.check = self.__in_check(piece, occupied, our_team, their_team)
        if self.check:
            other_team = ('black' if self.current_team == 'white' else 'white')
            shout(other_team + ' team in check')
            print('looking for checkmate....\n')

            # other player in checkmate?
            self.checkmate = self.__in_checkmate(occupied, our_team, their_team)

    def __in_check(self, piece, occupied, our_team, their_team):
        """
        Determine whether the opponent's king is in check, done by
        creating a theoretical_move from the attaching piece's current 
        position to their King's position to see if the move would be 
        valid.
        """
        if VERBOSE:
            print('Checking if other player is in check...')

        # work out move required to get to their king
        their_king = (self.pieces['wK'] if self.current_team == 'black'
                      else self.pieces['bK'])
        up = their_king.row - piece.row
        right = col_letter_to_no(their_king.col) - col_letter_to_no(piece.col)
        if VERBOSE:
            print('..possible to move ' + piece.ref + ' from ' +
                  str(piece.pos) + ' to ' + str(their_king.pos) + '?')
        theoretical_move = Move(piece, up, right, occupied, our_team,
                                their_team, theoretical_move=True)
        if theoretical_move.possible:
            return True
        else:
            if VERBOSE:
                print('..invalid_reason: ' + theoretical_move.invalid_reason)
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
                                                         pieces=p_dict,
                                                         list_moves=VERBOSE)
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
            all_possible_moves[ref] = []
            for potential_move in piece.valid_moves:
                [up, right] = potential_move[:2]
                theoretical_move = Move(piece, up, right, occupied, our_team,
                                        their_team, theoretical_move=True)
                if theoretical_move.possible:
                    # T O   R E V I E W 
                    # keep list of move obj like this for later reuse in next 
                    # turn? create a unique id for each move (which reflects 
                    # the current position of every piece as well as piece_ref 
                    # and new pos). 
                    # when creating a move check for matches first?
                    # Should destroy once > 1 move old to prevent build up?
                    all_possible_moves[ref].append(theoretical_move)
                    cnt += 1
                del theoretical_move

        if list_moves:
            print('\nPossible moves:')
            for ref, moves in iter(sorted(all_possible_moves.items())):
                print(self.pieces[ref].name.ljust(6) +
                      (' (' + ref + ')').ljust(5) + ': ' +
                      ', '.join([pos_to_cell_ref(obj.new_pos) for obj in moves]))
            _ = input("Press enter to continue")

        return all_possible_moves, cnt


def main():
    """
    Main entry point for program
    """
    game = Game()  # create game object as new instance of Game class

    # add set up func for 1/2 player options etc
    print(MOVE_INSTRUCTIONS)
    # _ = input('\nPress enter to continue...')

    while not game.checkmate:
        game.take_turn('white')
        game.take_turn('black')

    # pause         
    _ = input('\nPress enter to quit')


if __name__ == '__main__':
    main()


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
