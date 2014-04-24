#!/usr/bin/python 
"""Python implementation of chesss, in ASCII mode, two player only. """
VERBOSE = True 
PAUSE_AT_END = False
ASCII_OFFSET = 64 # used to convert numbers to ascii letter codes


class Game(object):
    """Top level class, the game object contains all of the other 
    class instances such as the pieces, the board etc."""
    PIECE_CODES = {'K': 'king', 'Q': 'queen', 'r':'rook',
                   'b':'bishop', 'k': 'knight', 'p': 'pawn'}
    TEAMS = {'w': 'white', 'b': 'black'}

    def __init__(self):
        """Initialise game object and create required member objects"""
        positions = [
            [' ', 'A  ', 'B  ', 'C  ', 'D  ', 'E  ', 'F  ', 'G  ', 'H  '], 
            ['1', 'br1', 'bk1', 'bb1', 'bQ' , 'bK' , 'bb2', 'bk2', 'br2'],
            ['2', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
            ['3', False, False, False, False, False, False, False, False],
            ['4', False, False, False, False, False, False, False, False],
            ['5', False, False, False, False, False, False, False, False],
            ['6', False, False, False, False, False, False, False, False],
            ['7', 'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
            ['8', 'wr1', 'wk1', 'wb1', 'wQ' , 'wK' , 'wb2', 'wk2', 'wr2']]

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
                     
        self.board = Board(positions)
        self.pieces = self.create_pieces(move_dict)
        self.check = False
        self.checkmate = False
        self.turns = 0
        self.current_team = None

    def create_pieces(self, move_dict):
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

    # def start_turn(self, team):
    #     """Allows you to register a turn withour going through all of 
    #     the code in take_turn, useful for using as a programming 
    #     interface when selecting moves from outside of this module."""
    #     self.current_team = team
    #     self.turns += 1

    def take_turn(self, team, prompt=None, move=None):
        """ Interact with player to facilitate moves, capture data and 
        identify/store information common to all potential moves.
        Also inlcudes optional param to specify a prompt to run 
        automatically or a move object (for interface from external
        scripts)."""
        global VERBOSE
        self.turns += 1
        self.current_team = team
        print("Team " + team + ":\nplease specify your move e.g. to move " +
              "from A7 to A5 just enter: A7, A5")
        occupied, our_team, their_team = self.get_occupied()
        valid = False

        # repeat prompt until a valid move is given...
        while not valid:
            # skip set up if a move object is passed in...
            if move:
                piece, down, right = move.piece, move.down, move.right
            else:
                if not prompt:
                    prompt = raw_input(">> ")

                # ability to switch debugging on/off
                if prompt.lower()[:5] == 'debug':
                    prompt = None
                    VERBOSE = not VERBOSE
                    continue
                elif prompt.lower() == 'redraw':
                    prompt = None
                    print(self.board.draw_board())
                    continue
                elif prompt.lower() == 'list':
                    prompt = None
                    self.get_all_possible_moves(list_moves=True)
                    continue

                piece, down, right = self.parse_prompt(prompt, our_team)

                if not piece:
                    invalid_reason = ('A piece in your team could not be found ' +
                                      'in cell: ' + prompt[:2] + '\n(using the ' +
                                      'first two charchters from your entry)')
                    continue
                elif down not in range(-8, 9) or right not in range(-8, 9):
                    invalid_reason = ('A new cell could not be identified from ' +
                                      'your input: ' + prompt)
                    continue

                # create object for move, this evaluates potential issues etc.
                move = Move(piece, down, right, occupied, our_team, their_team)

            if move.possible:
                 # reset flag (if able to move they are not in check) 
                self.check = False
                valid = True

                # update piece attributes
                piece.move_cnt += 1
                piece.row += down
                piece.col += right
                piece.pos = [piece.row, piece.col]

                # check if anything was taken
                if move.take:
                    # get ref of taken piece BEFORE board update
                    take_ref = self.board.positions[move.new_row][move.new_col]
                    self.pieces[take_ref].taken = True
                    if VERBOSE:
                        shout('taken piece: ' + take_ref)

                # update board
                self.board.positions[piece.row][piece.col] = piece.ref
                self.board.positions[piece.row-down][piece.col-right] = False
                print(self.board.draw_board())
            else:
                invalid_reason = move.invalid_reason

            if not valid:
                prompt = None
                print(invalid_reason + '\nPlease try again:')

        # other player in check?
        occupied, our_team, their_team = self.get_occupied() # refresh
        self.check = self.in_check(piece, occupied, our_team, their_team)
        if self.check:
            other_team = ('black' if self.current_team == 'white' else 'white')
            shout(other_team + ' team in check')
            print('looking for checkmate....\n')

            # other player in checkmate?
            self.checkmate = self.in_checkmate(occupied, our_team, their_team)
            if self.checkmate:
                shout('game over, ' + self.current_team + ' team wins')
                raw_input('\nPress enter to close game...')
                raise Exception('Game Finished')
            else:
                print('not checkmate, moves are possible.')

    def get_occupied(self):
        """Produce list of occupied cells and current teams, pieces."""
        occupied, our_team, their_team = [], {}, {}
        for ref, piece in self.pieces.items():
            if not piece.taken:
                occupied.append(piece.pos)
                # build up dict of piece objects for each team
                if piece.team == self.current_team:
                    our_team[ref] = piece
                else:
                    their_team[ref] = piece
        return occupied, our_team, their_team

    def parse_prompt(self, prompt, our_team):
        """Determine piece to be moved and move required from prompt."""
        # attempt to get details of piece to be moved
        try:
            # use first two charcters as current piece cell_ref...
            [cur_row, cur_col] = cell_ref_to_pos(prompt[:2])
            piece_ref = self.board.positions[cur_row][cur_col]
            assert ([cur_row, cur_col] in [our_team[i].pos for i in our_team])
        except:
            return None, None, None

        try:
            # use last two charcters as new cell_ref
            [new_row, new_col] = cell_ref_to_pos(prompt[-2:])
            down, right = new_row - cur_row, new_col - cur_col
            if VERBOSE:
                print('piece_ref: ' + piece_ref + ' | down: ' + str(down) + 
                      ' | right: ' + str(right))
        except:
            return self.pieces[piece_ref], None, None
        return self.pieces[piece_ref], down, right

    def in_check(self, piece, occupied, our_team, their_team):
        """Determine whether the opponent's king is in check, done by 
        creating a theoretical_move from the attaching piece's current 
        position to their King's position to see if the move would be 
        valid."""
        if VERBOSE:
            print('Checking if other player is in check...')

        # work out move required to get to their king
        their_king = (self.pieces['wK'] if self.current_team == 'black' 
                      else self.pieces['bK'])
        down, right = their_king.row - piece.row, their_king.col - piece.col
        if VERBOSE:
            print('..possible to move ' + piece.ref + ' from ' + 
                  str(piece.pos) + ' to ' + str(their_king.pos) + '?')
        theoretical_move = Move(piece, down, right, occupied, our_team, 
                                their_team, theoretical_move=True)
        if theoretical_move.possible:
            return True
        else:
            if VERBOSE:
                print('..invalid_reason: ' + theoretical_move.invalid_reason)
            return False

    def in_checkmate(self, occupied, our_team, their_team):
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
                [down, right] = potential_move[:2]
                theoretical_move = Move(piece, down, right, occupied, our_team, 
                                        their_team, theoretical_move=True)
                if theoretical_move.possible:
                    # T O   R E V I E W 
                    # keep list of move obj like this for later reuse in next 
                    # turn? create a unique id for each move (which reflects 
                    # the current position of every piece as well as piece_ref 
                    # and new pos). 
                    # hen creating a move check for matches first?
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

        return all_possible_moves, cnt


class Board(object):
    """Used to represent the current state of play, record all 
    current positions and interacts with display. The display is 
    intended to be logically separate from the rest of the game so 
    that the user interface can be replaced as required."""
    def __init__(self, positions):
        """Create board display based on game.positions passed in."""
        self.positions = positions
        self.display = self.draw_board()
        print(self.display)

    def draw_board(self):
        """ASCII display showing the current state of the game."""
        rows = cols = range(9)
        row_height, col_width, head_width = 4, 9, 5
        width = (len(cols[1:]) * col_width) + head_width + 1 # +1 for boarders
        lines = range((len(rows) * row_height)+1)

        display = "\n"*60
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


class Piece(object):
    """One instance created for each piece in the game containing all 
    of the information and functionality pertaining to that piece."""
    def __init__(self, ref, name, team, row, col, move_dict):
        """Get attributes required for piece."""
        self.ref = ref
        self.name = name
        self.team = team
        self.row = row
        self.col = col
        self.pos = [row, col]
        self.valid_moves = self.get_valid_moves(move_dict)
        self.largest = max([max([abs(i) for i in j[:2]]) for j in self.valid_moves])
        self.move_cnt = 0
        self.taken = False

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = self.get_one_space_moves()

    def get_valid_moves(self, move_dict):
        """Returns all of the moves possible for a piece before 
        considerations for the board boundaries, other pieces etc."""
        # valid moves for each type of piece:
        # [[-]down, [-]right, <condition1>, ..., <conditionN>]
        valid_moves = []

        # invert direction for whites (as they will move up board)
        if self.team.lower() == 'white':
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


class Move(object):
    """
    Capture characteristics of actual or potential moves e.g. amount 
    to go down and right, new row/col etc. for easy comparison. 
    """
    def __init__(self, piece, down, right, occupied, our_team, their_team,
                 theoretical_move=False, stop_recursion=False):
        """
        Define move attributes, determine if move is possible and the 
        outcomes reslting from the move or an invalid_reason.
        """
        self.piece = piece # store piece object against move
        self.down = down
        self.right = right
        self.move = [down, right]
        self.row = piece.row
        self.col = piece.col
        self.pos = piece.pos
        self.cell_ref = pos_to_cell_ref(self.pos)
        self.new_row = self.row + down
        self.new_col = self.col + right
        self.new_pos = [self.new_row, self.new_col]
        self.new_cell_ref = pos_to_cell_ref(self.new_pos)
        self.occupied = occupied
        self.our_team = our_team
        self.their_team = their_team
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
        filters = [self.valid_for_piece,
                   self.within_boundaries,
                   self.path_clear,
                   self.conditions_satisfied,
                   self.king_safe]

        for func in filters:
            result = func()
            if VERBOSE and not self.theoretical_move:
                print(func.__doc__ + ' - ' + result)
            if result != 'okay':
                return False, result

        return True, None

    def valid_for_piece(self):
        """Check move against piece.valid_moves"""
        invalid_msg = 'Move is not allowed for this piece.'
        if VERBOSE and not self.theoretical_move:
            print(str(self.move) + ' in ' + 
                  str([move[:2] for move in self.piece.valid_moves]) + '?')
        if self.move in [move[:2] for move in self.piece.valid_moves]:
            return 'okay'
        return invalid_msg

    def within_boundaries(self):
        """Check if move is possible within board boundaries"""
        invalid_msg = ('Move is not allowed as it would go outside of ' +
                       'the board boundaries to: ' + self.new_cell_ref)
        if self.new_row in range(1, 9) and self.new_col in range(1, 9):
            return 'okay'
        return invalid_msg

    def path_clear(self):
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

    def conditions_satisfied(self):
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

    def king_safe(self):
        """Check if a move would put your king in check"""
        # define base case as the move object is created recursively below
        invalid_msg = None
        if self.stop_recursion:
            return 'okay'

        # need to temporarily update piece object, so that all of the theoretical
        # moves checked below will recognise the new position (i.e. as if you had
        # made the move).
        old_row, old_col, old_pos = self.row, self.col, self.pos # copy for reverting
        self.piece.row, self.piece.col = self.new_row, self.new_col
        self.piece.pos = self.new_pos 
        if self.take:
            take_ref = [ref for ref in self.their_team.keys() 
                         if self.their_team[ref].pos == self.new_pos][0]
            taken_piece = self.their_team[take_ref]
            if taken_piece.name != 'king':
                del self.their_team[take_ref]
        self.occupied[self.occupied.index([old_row, old_col])] = (
            [self.new_row, self.new_col])

        if self.piece.team == 'white':
            our_king, their_king = self.our_team['wK'], self.their_team['bK']
        else:
            our_king, their_king = self.our_team['bK'], self.their_team['wK']

        # iterate through dictionary of their pieces creating theoretical moves
        # attempting to take king, if possible then move would put you in check.
        for ref, their_piece in self.their_team.items(): 
            down = our_king.row - their_piece.row
            right = our_king.col - their_piece.col
            # reverse our_team and their team args to switch
            theoretical_move = Move(their_piece, down, right, self.occupied, 
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
        self.piece.row, self.piece.col, self.piece.pos = old_row, old_col, old_pos
        self.occupied[self.occupied.index(self.new_pos)] = [old_row, old_col]
        if self.take:
            self.occupied.append(self.new_pos) # re-instate taken piece
            if taken_piece.name != 'king':
                self.their_team[take_ref] = taken_piece


        if not invalid_msg:
            return 'okay'
        return invalid_msg


################   G E N E R A L   U T I L I T I E S   ################

def pos_to_cell_ref(pos):
    """converts and [row, col] list into a cell reference where the
    cell is described as a letter for the column followed by a number 
    for the row e.g. [1, 1] becomes 'A1' or [4, 8] becomes 'H4'."""
    return chr(pos[1]+ ASCII_OFFSET)+str(pos[0])

def cell_ref_to_pos(cell_ref):
    """converts a cell_ref as given by the user (e.g. 'B6' to describe
    column B, row 6) into a [row, col] list e.g. 'E2' => [2, 5]."""
    return [int(cell_ref[1]), ord(cell_ref[0].upper())-ASCII_OFFSET]

def listsum(opperator='+', *args):
    """Perform an aggregation of lists by the opperator supplied e.g. 
    listsum('+'. [3, 6], [2, 2]) would return [5, 7]. The number of 
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

def shout(msg, suffix=' !!!'):
    """print message in all caps with spaces between and a suffix"""
    adj_msg = ' '.join([str(i).upper() for i in str(msg)+str(suffix)])
    print(adj_msg)

def main():
    """Main entry point for program"""
    game = Game()

    # tmp - will do in loop
    while not game.checkmate:
        game.take_turn('white')
        game.take_turn('black')

    # pause         
    if PAUSE_AT_END:
        foo = raw_input('\nPress enter to quit')
        print(foo)

if __name__ == '__main__':
    main()


##  N O T E S :
##  =========
##  
##    - write info to database (for future AI data):
##      - just get all raw data here (incl possible moves?):
##        - feature engineering can then be done in batch to enrich data e.g.:
##          - move preceding a take (on which side / by how many moves)
##          - other performance metrics e.g. short, mid and long term prospects
##            after move, i.e. how overall position in game improved / declined
##            over next x, y, z moves and who eventually won.
##          - move direction
##          - piece value
##          - some measure of the moves risk level?


##  Features:
##    - help feature to list shortcuts / features etc.


##  Performance:
##    - load all possible moves for each player at the start of each turn so 
##      that they are already know by the time the player comes to move?
##      - if doing this would need a keyboardinterupt exception???
##        To pick up cases when the user was ready to make their move before  
##        all possible moves had been pre-loaded (then just get moves for the 
##        piece they select) e.g.:
##http://stackoverflow.com/questions/7180914/pause-resume-a-python-script-in-middle
