#!/usr/bin/python 
"""
Python implementation of chess. Initially in ASCII mode and two player 
only.
"""
VERBOSE = False 
PAUSE_AT_END = False
ASCII_OFFSET = 64 # used to convert numbers to ascii letter codes


class Game(object):
    """
    Top level class, the game object contains all of the other class 
    instances such as the pieces, the board etc.
    """
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
                     
        self.board = Board(positions=positions)
        self.pieces = self.create_pieces()
        self.check = False
        self.checkmate = False
        self.turns = 0

    def create_pieces(self):
        """
        Creates a object for each piece and stores them in dictionary 
        which can be used later to access pieces by their ref. 

        The source of this data and the refs is the positions list, in 
        the game object.
        """
        pieces = {}

        for row, row_content in enumerate(self.board.positions):
            if row > 0: 
                for col, piece_ref in enumerate(row_content):
                    if col > 0 and piece_ref: 
                        team = Game.TEAMS[piece_ref[0]]
                        name = Game.PIECE_CODES[piece_ref[1]]                
                        pieces[piece_ref] = Piece(piece_ref, name, team, row, col)
        return pieces

    def take_turn(self, team):
        """
        Interact with player to facilitate moves, capture data and 
        identify/store information common to all potential moves.
        """
        print("Team " + team + ":\nplease specify your move e.g. to move " +
              "from A7 to A5 just enter: A7, A5")
        occupied, our_team = Game.get_occupied(self, team)
        valid = False
        while not valid:
            prompt = raw_input(">> ")
            piece, down, right = self.parse_prompt(prompt, our_team)

            if not piece:
                invalid_reason = ('A piece in your team could not be found ' +
                                  'in cell: ' + prompt[:2] + '\n(using the ' +
                                  'first two charchters from your entry)')
            elif down not in range(-8, 9) or right not in range(-8, 9):
                invalid_reason = ('A new cell could not be identified from ' +
                                  'your input: ' + prompt)
            else:
                if team == 'white':
                    our_king, their_king = self.pieces['wK'], self.pieces['bK']
                else:
                    our_king, their_king = self.pieces['bK'], self.pieces['wK']

                # create object for move, this evaluates potential issues etc.
                move = Move(piece, down, right, occupied, our_team, our_king)

                if move.possible:
                    valid = True

                    # update piece attributes
                    piece.move_cnt += 1
                    piece.row += down
                    piece.col += right
                    piece.pos = [piece.row, piece.col]

                    # check if anything was taken
                    if move.take:
                        taken_ref = self.board.positions[piece.row][piece.col]
                        self.pieces[taken_ref].taken = True

                    # update board
                    self.board.positions[piece.row][piece.col] = piece.ref
                    self.board.positions[piece.row-down][piece.col-right] = False
                    print self.board.draw_board()
                else:
                    invalid_reason = move.invalid_reason

            if not valid:
                print('Please try again: ' + invalid_reason)

        # other player in check?
        if VERBOSE:
            print('Checking if other player is in check...')
        occupied, our_team = Game.get_occupied(self, team)
        # work out move required to get to their king
        down, right = their_king.row - piece.row, their_king.col - piece.col
        theoretical_move = Move(piece, down, right, occupied, our_team, our_king)
        if theoretical_move.possible:
            self.check = True
            if VERBOSE:
                print('Team ' + ('white' if team == 'black' else 'black') + 
                      ' in check!!!')

    def get_occupied(self, team):
        """Produce list of occupied cells and current teams, pieces."""
        occupied, our_team = [], []
        for ref, piece in self.pieces.items():
            if not piece.taken:
                occupied.append(piece.pos)
                if piece.team == team:
                    our_team.append(piece.pos)
        return occupied, our_team

    def parse_prompt(self, prompt, our_team):
        """Determine piece to be moved and move required from prompt."""
        # attempt to get details of piece to be moved
        try:
            cur_col= ord(prompt[0].upper())-ASCII_OFFSET
            cur_row = int(prompt[1])
            piece_ref = self.board.positions[cur_row][cur_col]
            assert [cur_row, cur_col] in our_team
        except:
            return None, None, None

        try:
            new_col, new_row = ord(prompt[-2].upper())-ASCII_OFFSET, int(prompt[-1])
            down, right = new_row - cur_row, new_col - cur_col
            if VERBOSE:
                print('piece_ref: ' + piece_ref + ' | down: ' + str(down) + 
                      ' | right: ' + str(right))
        except:
            return self.pieces[piece_ref], None, None
        print('returning: ' + piece_ref + ', ' + str(down) + ', ' + str(right))
        return self.pieces[piece_ref], down, right


class Board(object):
    """
    Used to represent the current state of play, records all current 
    positions and interacts with display.

    The display is intended to be logically separate from the rest of 
    the game so that the user interface can be replaced as required.
    """
    def __init__(self, positions):
        """Create board display based on game.positions passed in."""
        self.positions = positions
        self.display = self.draw_board()
        print self.display

    # def show_board(self):
    #     """Display board to user."""
    #     print self.display

    def draw_board(self):
        """
        Creates the display to show the users the current state of the
        game.
        """
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
    """
    One instance created for each piece in the game containing all of 
    the information and functionality pertaining to that piece.
    """
    def __init__(self, ref, name, team, row, col):
        """Get attributes required for piece."""
        self.ref = ref
        self.name = name
        self.team = team
        self.row = row
        self.col = col
        self.pos = [row, col]
        self.valid_moves = self.get_valid_moves()
        self.largest = max([max([abs(i) for i in j[:2]]) for j in self.valid_moves])
        self.move_cnt = 0
        self.taken = False

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = self.get_one_space_moves()

    def get_valid_moves(self):
        """
        Returns all of the moves possible for a piece before 
        considerations for the board boundaries, other pieces etc.
        """
        # valid moves for each type of piece:
        # [[-]forward, [-]right, <condition1>, ..., <conditionN>]
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
        
        valid_moves = move_dict[self.name.lower()]

        # invert direction for blacks (as they will move down board)
        if self.team.lower() == 'white':
            for move in valid_moves:
                move[0] = move[0] * -1
            
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
    def __init__(self, piece, down, right, occupied, our_team, our_king):
        """
        Define move attributes, determine if move is possible and the 
        outcomes reslting from the move or an invalid_reason.
        """
        self.piece = piece
        self.down = down
        self.right = right
        self.move = [down, right]
        self.row = piece.row
        self.col = piece.col
        self.pos = [piece.row, piece.col]
        self.cell_ref = chr(piece.col + ASCII_OFFSET)+str(piece.row)
        self.new_row = self.row + down
        self.new_col = self.col + right
        self.new_pos = [self.new_row, self.new_col]
        self.new_cell_ref = chr(self.new_col + ASCII_OFFSET)+str(self.new_row)
        self.occupied = occupied
        self.our_team = our_team

        # initialise variable to be set later...
        self.check, self.take = None, False
        # performance consideration to stop at first invalid reason
        self.possible, self.invalid_reason = self.check_move()

        #tmp
        if not self.possible:
            if VERBOSE: 
                print('M O V E   N O T   A L L O W E D   ! ! !' + '\n' + 
                      self.invalid_reason)
        else:
            if VERBOSE: 
                print('M O V E   A L L O W E D   ! ! !')

    def check_move(self):
        """Run checks to see whether a move is possible."""
        filters = [self.valid_for_piece,
                   self.within_boundaries,
                   self.path_clear,
                   self.conditions_satisfied,
                   self.king_safe]

        for func in filters:
            result = func()
            if VERBOSE:
                print(func.__doc__ + ' - ' + result)
            if result != 'okay':
                return False, result

        return True, None

    def valid_for_piece(self):
        """Check move against the piece.valid_moves."""
        invalid_msg = 'This move is not allowed for this piece.'
        if self.move in [move[:2] for move in self.piece.valid_moves]:
            return 'okay'
        return invalid_msg

    def within_boundaries(self):
        """Check if move is possible within board boundaries."""
        invalid_msg = ('This move is not allowed as it would go outside of ' +
                       'the board boundaries to: ' + self.new_cell_ref)
        if self.new_row in range(1, 9) and self.new_col in range(1, 9):
            return 'okay'
        return invalid_msg

    def path_clear(self):
        """Check if move is blocked by another piece."""
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
                if VERBOSE:
                    print('Possible steps: ' + ', '.join(str(i) for i in poss_steps))

                distances = [distance(i, self.new_pos) for i in poss_steps]
                if VERBOSE:
                    print('Distances: ' + ', '.join(str(i) for i in distances))

                correct_step = poss_steps[distances.index(min(distances))]
                if VERBOSE:
                    print('Min dist: ' + str(min(distances)))
                    print('Correct step: ' + str(correct_step))

                tmp_pos = correct_step
                if VERBOSE:
                    print('tmp_pos: ' + str(tmp_pos))

                # check if cell on the way is occupied
                if tmp_pos in self.occupied:
                    final_step = (tmp_pos == self.new_pos)
                    # if it's not the final position or they are in our team block
                    if (not final_step) or (tmp_pos in self.our_team):
                        invalid_msg = ('This move is blocked as ' + 
                            chr(tmp_pos[1] + ASCII_OFFSET)+str(tmp_pos[0]) + 
                            ' is occupied.')
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

        # stop knights jumping onto own pieces
        if self.piece.allowed_to_jump and self.new_pos in self.our_team:
            invalid_msg = ('This move is blocked as ' + 
                chr(tmp_pos[1] + ASCII_OFFSET)+str(tmp_pos[0]) + ' is occupied.')
            return invalid_msg            

        return 'okay'

    def conditions_satisfied(self):
        """Check if all conditions stored for the move are satisfied. 
        The conditions are identified when the piece is created e.g. a 
        pawn only being able to move diagonally if taking."""
        conditions = [i[:2] for i in self.piece.valid_moves].index(self.move)
        return 'okay'

    def king_safe(self):
        """Check if a move would put you in check"""
        invalid_msg = 'You cannot move to this space as it would put your king in check'
        return 'okay'


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
        print foo

if __name__ == '__main__':
    main()


##  N O T E S :
##  =========
##  
##    - write info to database (for future AI data):
##      - just get all raw data here (incl possible moves?):
##        - feature engineering can then be done in batch to enrich data e.g.:
##          - move preceding a take (on which side / by how many moves)
##          - other performance metrics e.g. short, mid and long term prospects after 
##            move, i.e. how overall position in game improved / declined over next 
##            x, y, z moves and who eventually won.
##          - move direction
##          - piece value
##          - some measure of the moves risk level?


##  Features:
##    - consider option to list legal moves for a piece
##    - help feature to list shortcuts / features etc.


##  Performance:
##    - load all possible moves for each player at the start of each turn so that
##      they are already know by the time the player comes to move?
##      - if doing this would need a keyboardinterupt exception e.g.
##        http://stackoverflow.com/questions/7180914/pause-resume-a-python-script-in-middle
##        to pick up cases when the user was ready to make their move before all 
##        possible moves had been pre-loaded (then just get moves for the piece they
##        select.)
##    - consider concept of piece type so that each type on parses it's moves etc once?
##    - move occupied list to get once per turn
