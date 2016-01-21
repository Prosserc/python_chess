#!/usr/bin/python 
"""Python implementation of chess, main entry point."""
import json
from python_chess.board import Board
from python_chess.piece import Piece
from python_chess.move import Move
#from python_chess.chess_engine import pick_move
from python_chess.utils import (shout, write_log, cell_ref_to_pos, 
                                pos_to_cell_ref, format_msg, VERBOSE)

# constants
LOGGING = False
LOG = ''
MOVE_INSTRUCTIONS = format_msg("\nTo specify a move enter the cell referece " +
    "for the piece want to move and the cell referece for the new location. " +
    "The first two charcters of your prompt entry are used to identify " +
    "the current cell and the last two for the new cell e.g. to move from " +
    "A7 to A5 you could enter 'A7, A5' or use shorthand of 'a7a5'.")


class Game(object):
    """Top level class, the game object contains all of the other 
    class instances such as the pieces, the board etc."""
    PIECE_CODES = {'K': 'king', 'Q': 'queen', 'R':'rook',
                   'B':'bishop', 'N': 'knight', 'p': 'pawn'}
    TEAMS = {'w': 'white', 'b': 'black'}

    # describe piece positions by rank (row from botton up) and file (col)
    # used to instantiate Board and Piece classes
    START_POSITIONS = { 8: {'A': 'bR1', 'B': 'bN1', 'C': 'bB1', 'D': 'bQ' , 
                            'E': 'bK' , 'F': 'bB2', 'G': 'bN2', 'H': 'bR2'},
                        7: {'A': 'bp1', 'B': 'bp2', 'C': 'bp3', 'D': 'bp4', 
                            'E': 'bp5', 'F': 'bp6', 'G': 'bp7', 'H': 'bp8'},
                        6: {'A': False, 'B': False, 'C': False, 'D': False, 
                            'E': False, 'F': False, 'G': False, 'H': False},
                        5: {'A': False, 'B': False, 'C': False, 'D': False, 
                            'E': False, 'F': False, 'G': False, 'H': False},
                        4: {'A': False, 'B': False, 'C': False, 'D': False, 
                            'E': False, 'F': False, 'G': False, 'H': False},
                        3: {'A': False, 'B': False, 'C': False, 'D': False, 
                            'E': False, 'F': False, 'G': False, 'H': False},
                        2: {'A': 'wp1', 'B': 'wp2', 'C': 'wp3', 'D': 'wp4', 
                            'E': 'wp5', 'F': 'wp6', 'G': 'wp7', 'H': 'wp8'},
                        1: {'A': 'wR1', 'B': 'wN1', 'C': 'wB1', 'D': 'wQ' , 
                            'E': 'wK' , 'F': 'wB2', 'G': 'wN2', 'H': 'wR2'}
                      }
        # [
        # [' ', 'A  ', 'B  ', 'C  ', 'D  ', 'E  ', 'F  ', 'G  ', 'H  '],
        # ['8', 'br1', 'bk1', 'bb1', 'bQ' , 'bK' , 'bb2', 'bk2', 'br2'],
        # ['7', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
        # ['6', False, False, False, False, False, False, False, False],
        # ['5', False, False, False, False, False, False, False, False],
        # ['4', False, False, False, False, False, False, False, False],
        # ['3', False, False, False, False, False, False, False, False],
        # ['2', 'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
        # ['1', 'wr1', 'wk1', 'wb1', 'wQ' , 'wK' , 'wb2', 'wk2', 'wr2']]

    move_dict = {'king':   [[1, 1], [1, 0], [1, -1], [0, 1],
                            [0, -1], [-1, 1], [-1, 0], [-1, -1]], 
                 'rook':    [[i, 0] for i in range(1,9)] + \
                            [[0, i] for i in range(1,9)] + \
                            [[i*-1, 0] for i in range(1,9)] + \
                            [[0, i*-1] for i in range(1,9)], 
                 'bishop':  [[i, i] for i in range(1,9)] + \
                            [[i, i*-1] for i in range(1,9)] + \
                            [[i*-1, i] for i in range(1,9)] + \
                            [[i*-1, i*-1] for i in range(1,9)],  
                 'knight': [[2, 1], [2, -1], 
                            [1, 2], [1, -2], 
                            [-1, 2], [-1, -2], 
                            [-2, 1], [-2, -1]], 
                 'pawn':   [[1, 1, 'on_take'], 
                            [1, -1, 'on_take'], 
                            [1, 1, 'en_passant'], 
                            [1, -1, 'en_passant'], 
                            [1, 0], 
                            [2, 0, 'on_first']]
                 }
    move_dict['queen'] = move_dict['rook']+move_dict['bishop']

    def __init__(self):
        """Initialise game object and create required member objects"""
                     
        self.board = Board(Game.START_POSITIONS)
        self.pieces = self.__create_pieces(Game.move_dict)

        # initialise variables that will be needed later
        self.check = False
        self.checkmate = False
        self.draw = False
        self.turns = 0
        self.current_team = None

    def __to_JSON(self):
        """Output entire object contents as json."""
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True, indent=4)

    def __create_pieces(self, move_dict):
        """Creates a object for each piece and creates a dictionary to 
        enable access to the pieces via their ref. 
        The source of this data and the refs is the positions list, in 
        the game object."""
        pieces = {}

        for row, row_content in self.board.positions.items():
            if row > 0:
                for col, piece_ref in row_content.items():
                    if piece_ref: 
                        team = Game.TEAMS[piece_ref[0]]
                        name = Game.PIECE_CODES[piece_ref[1]]       
                        pieces[piece_ref] = Piece(piece_ref, name, team, 
                                                  row, col, move_dict)
        return pieces

    def take_turn(self, team, prompt=None, move=None):
        """ Interact with player to facilitate moves, capture data and 
        identify/store information common to all potential moves.
        Also inlcudes optional param to specify a prompt to run 
        automatically or a move object (for interface from external
        scripts)."""
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
                        user_feedback = None
                    prompt = raw_input("[" + team + " move] >> ")

                piece, up, right, found_issue, user_feedback = \
                   self.__parse_prompt(prompt, our_team)

                if not found_issue:
                    # create object for move, this evaluates potential issues etc.
                    move = Move(piece, up, right, occupied, our_team, their_team)
                    if move.possible:
                        validated = True
                    else:
                        user_feedback = move.invalid_reason
                        move = None # clear ready for next loop

            prompt = None # clear ready for next loop

        self.__process_move(piece, move, up, right, occupied, our_team, their_team)

        # log state of game
        if LOGGING:
            LOG = '\n'.join(LOG, self.__to_JSON())

        # wrap up if done...
        if self.checkmate or self.turns >= 200: ## TODO (see below)
            if self.turns >= 200: # TODO - replace with self.draw once draw rules done
                shout(str(self.turns) + ' moves, lets call it a draw')
            elif self.checkmate:
                shout('game over, ' + self.current_team + ' team wins')
            if LOGGING:
                write_log(LOG)
            raw_input('\nPress enter to close game...')
            raise Exception('Game Finished')

    def __parse_prompt(self, prompt, our_team):
        """Determine piece to be moved and move required from prompt."""
        global VERBOSE

        # first check for special commands
        if prompt.lower()[:5] == 'debug':
            VERBOSE = not VERBOSE
            user_feedback = "Debugging " + ("on" if VERBOSE else "off")
            return None, None, None, True, user_feedback
        elif prompt.lower() == 'redraw': # TODO remove if not needed
            print(self.board.draw_board())
            return None, None, None, True, None
        elif prompt.lower()[:4] == 'list':
            self.get_all_possible_moves(list_moves=True)
            return None, None, None, True, None           

        # attempt to get details of piece to be moved...
        #try:
        # use first two charcters as current cell_ref
        [cur_rank, cur_file] = cell_ref_to_pos(prompt[:2])
        print("Calling get_piece_ref, passing in cur_rank: {0} and cur_file: {1}".format(cur_rank, cur_file))
        piece_ref = self.board.get_piece_ref(cur_rank, cur_file)
        piece = self.pieces[piece_ref]
        ## TMP ################
        print("tmp debugging info........................................")
        print("piece_ref: {0}".format(piece.ref))
        print("..........................................................")
        #######################
        assert ([cur_rank, cur_file] in [our_team[obj].pos for obj in our_team])
        #except:
        #    user_feedback = ('A piece in your team could not be found ' +
        #                      'in cell: ' + prompt[:2] + '\n(using the ' +
        #                      'first two charchters from your entry)')
        #    return None, None, None, True, user_feedback

        # attempt to get destination...
        try:
            # use last two charcters as new cell_ref
            [new_rank, new_file] = cell_ref_to_pos(prompt[-2:])
            up, right = new_rank - cur_rank, new_file - cur_file

            # TMP ###############################################################
            print('Up: {0}, Right: {1} (should be 2, 0)'.format(up, right))
            print('cur_rank: {0}, cur_file: {1} (should be 2, 1)'.format(cur_rank, cur_file))
            print('new_rank: {0}, new_file: {1} (should be 4, 1)'.format(new_rank, new_file))
            #####################################################################

            if VERBOSE:
                print('piece_ref: ' + piece.ref + ' | up: ' + str(up) + 
                      ' | right: ' + str(right))
            assert up in range(-8, 9) and right in range(-8, 9)
        except:
            user_feedback = ('A valid new cell could not be identified ' +
                              'from your input: ' + prompt)
            return piece, None, None, True, user_feedback

        return piece, up, right, False, None

    def get_occupied(self):
        """Produce list of occupied cells and current teams, pieces."""
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
        """Execute and updates required as a result of a valid move."""
        # update piece attributes
        occupied.remove(piece.pos)
        piece.move_cnt += 1
        piece.row += up
        piece.col += right
        piece.pos = [piece.row, piece.col]
        occupied.append(piece.pos)

        # check if anything was taken
        if move.take:
            # get ref of taken piece BEFORE board update
            taken_piece_ref = self.board.get_piece_ref(move.new_row, move.new_col)
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
        #occupied, our_team, their_team = self.get_occupied() # refresh
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
        """Determine whether the opponent's king is in check, done by 
        creating a theoretical_move from the attaching piece's current 
        position to their King's position to see if the move would be 
        valid."""
        if VERBOSE:
            print('Checking if other player is in check...')

        # work out move required to get to their king
        their_king = (self.pieces['wK'] if self.current_team == 'black' 
                      else self.pieces['bK'])
        up, right = their_king.row - piece.row, their_king.col - piece.col
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
        """Determine whether the opponents king is in checkmate, done 
        by creating many theoretical moves for each piece on the  
        opponents team to see if any are valid i.e. end with their 
        king not in check."""
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
                      "display all poissible moves)")
                return False
        return True

    def get_all_possible_moves(self, occupied=None, our_team=None, 
                               their_team=None, pieces=None,
                               list_moves=False, team=None):
        """Try all of the valid moves for the pieces passed in, pieces 
        arg should be a dictionary of piece objects with piece_ref as 
        their key. Return a dictionary with same keys, where value is 
        a list containing a move objects for each possible move for 
        that piece (can be[]).
        If occupied, our_team or their_team are not supplied a new call
        is made to self.get_occupied.
        If pieces is not supplied this is defaulted to our_team.
        Team param is picked up from game object when not supplied."""
        # get defaults if args missing
        if not team:
            team = self.current_team
        else:
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
            tmp = raw_input("Press enter to continue")

        return all_possible_moves, cnt


def main():
    """Main entry point for program"""
    game = Game() # create game object as new instance of Game class

    # add set up func for 1/2 player options etc
    print(MOVE_INSTRUCTIONS)
    tmp = raw_input('\nPress enter to continue...')

    # tmp - will do in loop
    while not game.checkmate:
        game.take_turn('white')
        game.take_turn('black')

    # pause         
    tmp = raw_input('\nPress enter to quit')

if __name__ == '__main__':
    main()


##  N O T E S :
##  =========

##  Performance:
##    - load all possible moves for each player at the start of each turn so 
##      that they are already know by the time the player comes to move?
##      - if doing this would need a keyboardinterupt exception???
##        To pick up cases when the user was ready to make their move before  
##        all possible moves had been pre-loaded (then just get moves for the 
##        piece they select) e.g.:
##http://stackoverflow.com/questions/7180914/pause-resume-a-python-script-in-middle
##    - LOGGING needs to be fully written (lazy implementation at present)

##  Bugs:
##    - prompt not re-prompting for invalid input
##    - automated game - King seems to put itself in check with pawns (found
##      cause - game object is not updated after moves - need to make copies).
##    - option to draw board for automated game.
