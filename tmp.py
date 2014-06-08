#!/usr/bin/python
"""Called from python_chess.game. This version is used for ASCII mode."""

class Board(object):
    """Used to represent the current state of play, record all 
    current positions and interacts with display. The display is 
    intended to be logically separate from the rest of the game so 
    that the user interface can be replaced as required."""
    def __init__(self, positions):
        """Create board display based on game.positions passed in."""
        self.positions = positions

    def draw_board(self):
        """ASCII display showing the current state of the game."""
        rows = cols = range(9)
        row_height, col_width, head_width = 4, 9, 5
        width = (len(cols[1:]) * col_width) + head_width + 1 # +1 for boarders
        lines = range((len(rows) * row_height)+1)

        display = "\n"*20
        for i in lines:
            row = (i/4) # cell down (0-8)
            sep = "|" if row > 0 else " "

            # if at row boundary...
            if i%row_height == 0:
                # if last row or frst row after headings
                if i == max(lines) or row == 1:
                    line = " "*head_width + "-"*(width-head_width)
                # if first row
                elif row == 0:
                    line = None
                else:
                    line = " " * head_width + sep
                    for col in cols[1:]:
                        line = line + "-"*(col_width-1) + sep

            # if line where a pieces could go
            elif i%row_height == 2:
                line = "  " + self.positions[row][0][0] + "  " + sep
                for col in cols[1:]:
                    if self.positions[row][col]:
                        piece = self.positions[row][col][:2]
                        pad1 = " "*(((col_width-1)/2)-1)
                        pad2 = " "*((col_width-(len(pad1)+len(piece)))-1)
                        line = line + pad1 + piece + pad2 + sep
                    else:
                        line = line + " "*(col_width-1) + sep

            # normal row
            else:
                line = " "* head_width + sep
                for col in cols[1:]:
                    line = line + " "*(col_width-1) + sep

            if line:
                display = display + line + "\n"

        return display

    def get_piece_ref(self, rank, _file):
        """Get a piece object from the positions list."""
        # ranks in chess start from 1 at bottom, adjust for reverse in positions
        print("In get_piece_ref, rank set to: {0}, _file set to: {1}".format(rank, _file)) #TMP
        row = 9 - rank
        col = _file
        print("row set to: {0}, col set to {1}".format(row, col)) #TMP
        print("self.positions[row][col] set to {0}".format(self.positions[row][col]))
        return self.positions[row][col]   

    def update_board(self, old_pos, new_pos, piece_ref):
        """Reflect a successful move on the board positions."""
        old_rank, new_rank = 9 - old_pos[0], 9 - new_pos[1]
        old_file, new_file = old_pos[0], new_pos[1]
        self.positions[old_rank][old_file] = False
        self.positions[new_rank][new_file] = piece_ref

if __name__ == '__main__':
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
#!/usr/bin/python 
"""Unit test for chess.py - an automated game. As AI is not yet built
these will be purely random moves with no intellegence, but will serve 
as a good test it will cover a broad array of pieces / moves."""
from python_chess.game import Game
from random import random as rnd
from copy import deepcopy

PIECE_VALS = {'queen': 9, 'rook': 5, 'bishop': 3.5,
              'knight': 3.2, 'pawn': 1, 'check': 3, 'checkmate': 1000}

def __pick_rnd(lst, cnt=None):
    """Returns a random item from a list."""
    if not cnt:
        cnt = len(lst)
    i = int(rnd()*(cnt-1)) # -1 needed to allow for zero based indexing
    return lst[i]
 
def __random_move(game, team):
    """Level 0 - Select a move randomly from all possible moves."""
    move_dict, cnt = game.get_all_possible_moves(team=team)
    obj_list = []
    for piece_ref, moves in move_dict.items():
        for move_obj in moves:
            obj_list.append(move_obj)
    return __pick_rnd(obj_list, cnt)

def __game_state(game, team):
    """Asses the values of pieces on the current team relative to the 
    the value of pieces on the other team."""
    pass # to follow

def __next_move(game_branch, team):
    """Find all possible moves, select one resulting in the 
    best take available (if one is available)."""
    obj_list.append(move_obj)
    if move_obj.take:
        take_ref = \
           game_branch.board.positions[move_obj.new_row][move_obj.new_col]
        points = piece_vals[game_branch.pieces[take_ref].name]
        if points > max_points:
            max_points, selected_move = points, move_obj

    if max_points == 0:
        selected_move = __pick_rnd(obj_list, cnt)
    return selected_move

def pick_move(game, team, level):
    """Create a data structure representing the state of the game for 
    each branch of moves (a game object) with a points score for the 
    branch. Points should be added for the best selectable move for 
    your team and taken off for the best possible opponents move."""
    if level == 0:
        return __random_move(game, team)
    max_points, obj_list = 0, []

    for l in range(1,level+1):
        if l ==1:
            branch = deepcopy(game)
        
        move_dict, cnt = branch.get_all_possible_moves(team=team)
        for piece_ref, moves in move_dict.items():
            for move_obj in moves:
                ##
                pass

        move_branches = {}

if __name__ == '__main__':
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
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
    START_POSITIONS = {
        8: {'A': 'bR', 'B': 'bN', 'C': 'bB', 'D': 'bQ', 'E': 'bK', 'F': 'bB', 'G': 'bN', 'H': 'bR'},
        7: {'A': 'bp', 'B': 'bp', 'C': 'bp', 'D': 'bp', 'E': 'bp', 'F': 'bp', 'G': 'bp', 'H': 'bp'},
        6: {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None},
        5: {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None},
        4: {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None},
        3: {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None, 'G': None, 'H': None},
        2: {'A': 'wp', 'B': 'wp', 'C': 'wp', 'D': 'wp', 'E': 'wp', 'F': 'wp', 'G': 'wp', 'H': 'wp'},
        1: {'A': 'wR', 'B': 'wN', 'C': 'wB', 'D': 'wQ', 'E': 'wK', 'F': 'wB', 'G': 'wN', 'H': 'wR'}
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

        for row, row_content in enumerate(self.board.positions):
            if row > 0:
                for col, piece_ref in enumerate(row_content):
                    if col > 0 and piece_ref: 
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
#!/usr/bin/python
"""Called from python_chess.game"""
from python_chess.utils import pos_to_cell_ref, shout, VERBOSE

class Move(object):
    """
    Capture characteristics of actual or potential moves e.g. amount 
    to go up and right, new rank/_file etc. for easy comparison. 
    """
    def __init__(self, piece, up, right, occupied, our_team, their_team,
                 theoretical_move=False, stop_recursion=False):
        """
        Define move attributes, determine if move is possible and the 
        outcomes reslting from the move or an invalid_reason.
        """
        self.piece = piece # store piece object against move
        self.up = up
        self.right = right
        self.move = [up, right]
        self.rank = piece.rank
        self._file = piece._file
        self.pos = piece.pos
        self.cell_ref = pos_to_cell_ref(self.pos)
        self.new_rank = self.rank + up
        self.new_file = self._file + right
        self.new_pos = [self.new_rank, self.new_file]
        self.new_cell_ref = pos_to_cell_ref(self.new_pos)
        self.occupied = occupied
        self.our_team = our_team
        self.their_team = their_team
        #self._id = self.__generate_id() # REVIEW - Needed?
        self.our_team_cells = [our_team[piece_ref].pos 
                               for piece_ref in our_team]
        self.their_team_cells = [their_team[piece_ref].pos 
                                 for piece_ref in their_team]
        self.theoretical_move = theoretical_move                     
        self.stop_recursion = stop_recursion

        # initialise variable to be set later...
        self.check, self.take = None, False
        # performance consideration to stop at first invalid reason
        self.possible, self.invalid_reason = self.check_move()

        if not self.possible:
            if VERBOSE and not self.theoretical_move: 
                shout('move not allowed')
        else:
            if VERBOSE and not self.theoretical_move: 
                shout('move allowed')

    def check_move(self):
        """Run checks to see whether a move is possible."""
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
                return False, result

        return True, None

    def __valid_for_piece(self):
        """Check move against piece.valid_moves"""
        invalid_msg = 'Move is not allowed for this piece.'
        if VERBOSE and not self.theoretical_move:
            print(str(self.move) + ' in ' + 
                  str([move[:2] for move in self.piece.valid_moves]) + '?')
        if self.move in [move[:2] for move in self.piece.valid_moves]:
            return 'okay'
        return invalid_msg

    def __within_boundaries(self):
        """Check if move is possible within board boundaries"""
        invalid_msg = ('Move is not allowed as it would go outside of ' +
                       'the board boundaries to: ' + self.new_cell_ref)
        if self.new_rank in range(1, 9) and self.new_file in range(1, 9):
            return 'okay'
        return invalid_msg

    def __path_clear(self):
        """Check if move is blocked by another piece"""
        def distance(pos1, pos2):
            """Calculate the distance between two sets of coordinates."""
            return sum([abs(pos2[i] - pos1[i]) for i in range(len(pos1))])
        MAX_STEPS = 8
        current_step = 0

        # take steps by taking min distance to destination after each
        # of the possible one step moves

        # check steps for pieces cannot jump move more than one space
        if not self.piece.allowed_to_jump:
            tmp_pos = self.pos
            while tmp_pos != self.new_pos:
                # get all possible destination cells after a one space step
                poss_steps = [[i[0] + tmp_pos[0], i[1] + tmp_pos[1]]
                              for i in self.piece.one_space_moves
                              if i[0] + tmp_pos[0] in range(1, 9) and
                                 i[1] + tmp_pos[1] in range(1, 9)]
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
                        invalid_msg = ('This move is blocked as ' + 
                                       pos_to_cell_ref(tmp_pos) + ' is occupied.')
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
                if current_step >= MAX_STEPS:
                    break

        # allow for knights
        else: 
            if self.new_pos in self.our_team_cells:
                invalid_msg = ('This move is blocked as ' + 
                                self.new_cell_ref + ' is occupied.')
                return invalid_msg
            elif self.new_pos in self.their_team_cells:
                self.take = True

        return 'okay'

    def __conditions_satisfied(self):
        """Check if all conditions stored for the move are satisfied. 
        The conditions are identified when the piece is created e.g. a 
        pawn only being able to move diagonally if taking."""
        ind = [i[:2] for i in self.piece.valid_moves].index(self.move)
        try:
            conditions = self.piece.valid_moves[ind][2:]
        except IndexError:
            return 'okay' # no conditions on move

        for cond in conditions:
            if VERBOSE and not self.theoretical_move:
                print('Checking condition: ' + str(cond)) 
            
            if cond == 'on_first':
                if self.piece.move_cnt > 0:
                    invalid_msg = ("A pawn can only move two spaces on it's " +
                                   "first move.")
                    return invalid_msg
            elif cond == 'on_take':
                if self.new_pos not in self.occupied:
                    invalid_msg = 'A pawn can only move diagonally when taking.'
                    return invalid_msg
                else:
                    self.piece.valid_moves.remove(self.move+[cond])
            #   T O   F O L L O W . . .
            elif cond == 'en_passant':
                invalid_msg = "Sorry " + cond + " rule not coded yet."
                return invalid_msg
        return 'okay'

    def __king_safe(self):
        """Check if a move would put your king in check"""
        # define base case as the move object is created recursively below
        invalid_msg = None
        if self.stop_recursion:
            return 'okay'

        # need to temporarily update piece object, so that all of the theoretical
        # moves checked below will recognise the new position (i.e. as if you had
        # made the move).
        old_rank, old_file, old_pos = self.rank, self._file, self.pos # copy for reverting
        self.piece.rank, self.piece._file = self.new_rank, self.new_file
        self.piece.pos = self.new_pos 
        if self.take:
            take_ref = [ref for ref in self.their_team.keys() 
                         if self.their_team[ref].pos == self.new_pos][0]
            taken_piece = self.their_team[take_ref]
            if taken_piece.name != 'king':
                del self.their_team[take_ref]
        self.occupied[self.occupied.index([old_rank, old_file])] = (
            [self.new_rank, self.new_file])

        if self.piece.team == 'white':
            our_king, their_king = self.our_team['wK'], self.their_team['bK']
        else:
            our_king, their_king = self.our_team['bK'], self.their_team['wK']

        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for ref, their_piece in self.their_team.items(): 
            up = our_king.rank - their_piece.rank
            right = our_king._file - their_piece._file
            # reverse our_team and their team args to switch
            theoretical_move = Move(their_piece, up, right, self.occupied, 
                                    self.their_team, self.our_team, 
                                    theoretical_move=True,
                                    stop_recursion=True)
            if theoretical_move.possible:
                invalid_msg = ('You cannot move to this space as it would put ' +
                               'your king in check with the ' + their_piece.name +
                               ' in cell ' + pos_to_cell_ref(theoretical_move.pos))
                break # cannot return here as need to revert position etc.
            del theoretical_move

        # revert piece to original position
        self.piece.rank, self.piece._file, self.piece.pos = old_rank, old_file, old_pos
        self.occupied[self.occupied.index(self.new_pos)] = [old_rank, old_file]
        if self.take:
            self.occupied.append(self.new_pos) # re-instate taken piece
            if taken_piece.name != 'king':
                self.their_team[take_ref] = taken_piece


        if not invalid_msg:
            return 'okay'
        return invalid_msg

    def generate_id(self):
        """Generate unique moveID based on piece_ref being moved and 
        position of every other piece."""
        # Error - new/old showing as same
        _id = ('mv:' + self.piece.ref + "-" + str(self.rank*self._file) + "-" + 
               str(self.new_rank*self.new_file) + ",oth:") 
        for piece_ref, piece in self.their_team.items():
            if not piece.taken and piece_ref != self.piece.ref:
                _id = '+'.join([_id, (piece_ref + '-' + str(piece.rank*piece._file))])
        return _id

if __name__ == '__main__':
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
        #!/usr/bin/python
"""Called from python_chess.game"""
import json

class Piece(object):
    """One instance created for each piece in the game containing all 
    of the information and functionality pertaining to that piece."""
    def __init__(self, ref, name, team, row, col, move_dict):
        """Get attributes required for piece."""
        self.ref = ref
        self.name = name
        self.team = team
        self.row = int(row)
        self.rank = 9 - int(row)
        self.col = self._file = int(col)
        self.pos = [self.rank, self._file]
        self.valid_moves = self.get_valid_moves(move_dict)
        self.largest = max([max([abs(i) for i in j[:2]]) for j in self.valid_moves])
        self.move_cnt = 0
        self.taken = False

        # TMP ##############################################################
        sample_ref = 'wp1'
        if self.ref == sample_ref:
            obj_dict = self.__to_JSON()
            print("obj_dict is type: {0}".format(type(obj_dict)))
            print("obj_dict contents for {0}\n".format(sample_ref))
            print(obj_dict)
            #for key, val in obj_dict.items:
                #print("Key: {0}, value: {1}".format(key, val))
        ####################################################################     

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = self.get_one_space_moves()

    def __to_JSON(self):
        """Output entire object contents as json."""
        return json.dumps(self, default=lambda o: o.__dict__, 
                          sort_keys=True, indent=4)

    def get_valid_moves(self, move_dict):
        """Returns all of the moves possible for a piece before 
        considerations for the board boundaries, other pieces etc."""
        # valid moves for each type of piece:
        # [[-]down, [-]right, <condition1>, ..., <conditionN>]
        valid_moves = []

        # invert direction for whites (as they will move up board)
        if self.team.lower() == 'black':
            for move in move_dict[self.name.lower()]:
                valid_moves.append([move[0] * -1] + move[1:])
        else:
            valid_moves = move_dict[self.name.lower()]
            
        return valid_moves

    def get_one_space_moves(self):
        """
        Defines all one piece moves (needed frequently to calculate the
        steps required to get from A to B).
        """
        one_space_moves = []
        for move in self.valid_moves:
            if min(move[:2]) >= -1 and max(move[:2]) <= 1:
                one_space_moves.append(move)

        return one_space_moves


if __name__ == '__main__':
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
#!/usr/bin/python
"""General utility functions / constants for python_chess"""
LOG_FILE_PATH = 'log.json'
ASCII_OFFSET = 64 # used to convert numbers to ascii letter codes
VERBOSE = False 

def pos_to_cell_ref(pos):
    """converts and [row, col] list into a cell reference where the
    cell is described as a letter for the column followed by a number 
    for the row e.g. [1, 1] becomes 'A1' or [4, 8] becomes 'H4'."""
    return chr(pos[1]+ ASCII_OFFSET)+str(pos[0])

def cell_ref_to_pos(cell_ref):
    """converts a cell_ref as given by the user (e.g. 'B6' to describe
    column B, row 6) into a [row, col] list e.g. 'E2' => [2, 5]."""
    return [int(cell_ref[1]), ord(cell_ref[0].upper())-ASCII_OFFSET]

def write_log(log):
    """write json log data to a file."""
    file_obj = open(LOG_FILE_PATH, 'wb')
    print('\nLogging game data...')
    file_obj.writelines(log)
    file_obj.close()

def listagg(opperator='+', *args):
    """Perform an aggregation of lists by the opperator supplied e.g. 
    listagg('+'. [3, 6], [2, 2]) would return [5, 7]. The number of 
    lists supplied is arbitrary, but each list must have the same 
    number of elements."""
    l = len(args[1])
    res = args[0]
    for i, arg in enumerate(args[1:]):
        if len(arg) != l:
            raise Exception("The length of all arguements must be the same")
        for j, item in enumerate(arg):
            cmd = "res[j] " + opperator + "= " + str(item)
            exec(cmd)
    return res

def shout(msg, suffix=' !!!', print_output=True, return_output=False):
    """Output message in all caps with spaces between and a suffix."""
    adj_msg = ' '.join([str(i).upper() for i in str(msg)+str(suffix)])
    if print_output:
        print(adj_msg)
    if return_output:
        return adj_msg

def format_msg(msg, line_width=80):
    """Formats a message into chuncks to avoid splitting words."""
    line_pos, result = 0, ""
    for word in msg.split(' '):
        line_pos += len(word) + 1
        if line_pos < line_width:
            result += word + ' '
        else:
            result += '\n' + word + ' '
            line_pos = len(word) + 1
    return result

if __name__ == '__main__':
    print("This module is not intended to be the main entry point for the " +
          "program, call python_chess.game to start a new game.")
