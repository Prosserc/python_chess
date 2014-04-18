#!/usr/bin/python 
"""
Python implementation of chess. Initially in ASCII mode and two player 
only.
"""
VERBOSE = True 
PAUSE_AT_END = False

class Piece(Game):
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
        self.valid_moves = Piece.get_valid_moves(self)
        self.move_cnt = 0
        self.taken = False

        # note knights ability to jump
        if self.name.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            self.one_space_moves = Piece.get_one_space_moves(self)

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

    def move(self, down, right, game):
        """
        Check the validity of a move and procedes with the move or 
        returns details of why the move could not be done.
        """
        invalid_reasons = []
        destination = [self.row+down, self.col+right]

        # check valid moves for piece
        if [down, right] not in [move[:2] for move in self.valid_moves]:
            invalid_reasons.append('piece')
            print(str(down) + ' steps down and ' + str(right) + 
                  ' steps right is not a valid move for this piece')

        poss_cells, potential_take = Piece.get_moves_allowed(self, game)

        if VERBOSE:
            print('Possible destination cells identified: ' + 
                  ', '.join([str(i) for i in poss_cells]))

        if destination in poss_cells:
            if VERBOSE: 
                print('M O V E   A L L O W E D   ! ! !')
            if potential_take:
                take_id = potential_take
                if VERBOSE: 
                    print('T A K I N G   ' + take_id)
            return True, None
        if VERBOSE: 
            print('M O V E   N O T   A L L O W E D   ! ! !')
        return False, invalid_reasons # IN PROG... need to get reasons

    def get_moves_allowed(self, game):
        """
        Get all of the legal moves for a piece from it's current 
        position. This builds on the valid moves already identified 
        when the piece is created and applies filters based on the 
        boundaries of the board, the position of other pieces etc.
        """
        potential_take = False

        if VERBOSE: 
            print('Getting valid moves for ' + self.ref + ' from ' + str(self.pos))

        
        # filter valid moves based on board boundaries
        poss_cells = []
        moves_remaining = []
        for move in self.valid_moves:
            new_row = self.row + move[0] # down
            new_col = self.col + move[1] # right
            if new_col in range(1,9) and new_row in range(1,9):
                poss_cells.append([new_row, new_col])
                moves_remaining.append(move)

        if VERBOSE: 
            print(str(len(poss_cells)) + ' moves possible within boundaries')

        # get list of occupied cells
        occupied, our_team = [], []
        for ref, piece in game.pieces.items():
            if ref != self.ref:
                occupied.append(piece.pos)
                if piece.team == self.team:
                    our_team.append(piece.pos)

        if VERBOSE:
            print('The following cells are occupied: ' + 
                  ', '.join([str(i) for i in occupied]))

        # filter based on position of other pieces (blocking) 
        if not self.allowed_to_jump: # i.e. not a knight
            for cell in poss_cells[:]:

                potential_take = False
                # only check if moving more than one space
                if (cell[0] - self.row) > 1 or (cell[1] - self.col) > 1:

                    if VERBOSE: 
                        print('.checking move to: ' + str(cell) + '...')
                    move_okay = True

                    steps = Piece.get_steps(self, 
                                            cell[0] - self.row, 
                                            cell[1] - self.col, 
                                            moves_remaining[:])
                    if VERBOSE: 
                        print('..steps found: ' + ', '.join([str(i) for i in steps]))

                    # go through each step, if in occupied list to check if blocked
                    tmp_pos = self.pos
                    for step in steps:
                        tmp_pos = [tmp_pos[0]+step[0], tmp_pos[1]+step[1]]
                        if tmp_pos in occupied:
                            move_okay = False
                            break

                    # check if final destination is occupied
                    if cell in occupied:
                        if cell in our_team:
                            move_okay = False
                        else:
                            potential_take = cell

                        # pawns blocked from forwards moves
                        if self.name == 'pawn' and (cell[1] - self.col) == 0:
                            move_okay = False


                    if not move_okay:
                        move = [cell[0] - self.row, cell[1] - self.col]
                        if VERBOSE: 
                            print('..removing cell: ' + str(cell) + ' and move ' + 
                                  str(move) + ' ... original position: ' + str(self.pos))
                            print('..from list of moves: ' + 
                                  ', '.join([str(i) for i in moves_remaining]))
                        poss_cells.remove(cell)
                        moves_remaining.remove(move) #???

        # check that any conditions on the move are satisfied


        # check for en passant rule (if you move a pawn 2 forward it can be captured by an
        # enemy pawn one square to the left or right of it on the same row, the other pawn 
        # advances one space diagonally as if the first pawn had only moved one forward)


        # check that move would not put your King in check


        return poss_cells, potential_take

    def get_steps(self, forward, right, moves_remaining):
        """
        Return all intermediate steps required to get from A to B 
        (not inlcuding final step). Used to determine if a move should
        be blocked by another piece.
        """
        i = 0 # failsafe incase of logic error leading to infinite loop

        # get shoretlist of single space moves allowed
        for move in moves_remaining[:]:
            if move not in self.one_space_moves:
                moves_remaining.remove(move)

        if VERBOSE: 
            print('..target overall move: ' + str([forward, right]))
            print('..possible steps to be reviewed: ' + 
                  ', '.join([str(move) for move in moves_remaining]))

        steps = []

        while (abs(forward) > 1 or abs(right) > 1) and i <= 8:
            if VERBOSE: 
                print('...[forward, right] moves left: ' + 
                      str([forward, right]))
            fwd = -1 if forward < 0 else 1
            sdw = -1 if right < 0 else 1
            if VERBOSE:
                print('...[fwd, sdw] set to: ' + str([fwd, sdw]))
            if abs(forward) > abs(right) and [fwd, 0] in moves_remaining:
                steps.append([fwd, 0])
                forward -= fwd
            elif abs(forward) == abs(right) and [fwd, sdw] in moves_remaining:
                steps.append([fwd, sdw])
                forward -= fwd
                right -= sdw
            elif abs(forward) < abs(right) and [0, sdw] in moves_remaining:
                steps.append([fwd, sdw])
                forward -= fwd                
            else:
                print("\nHmmm, not sure I should have ended up here. This means that I can " +
                      "not move one step in the direction that I need to? Add more debug " +
                      "messages to work out whats going on.")
                raise Exception("No valid steps available.")
            i += 1
            if VERBOSE: 
                print('...step ' + str(i) + ' added: ' + str([fwd, sdw]))

        return steps


class Board(Game):
    """
    Used to represent the current state of play, records all current 
    positions and interacts with display.

    The display is intended to be logically separate from the rest of 
    the game so that the user interface can be replaced as required.
    """
    def __init__(self, positions):
        self.positions = positions
        self.display = Board.draw_board(self)

    def move_peice(self, piece):
        """
        Update the board to reflect a move that has been perfomed on a 
        piece."""
        pass

    def draw_board(self):
        """
        Creates the display to show the users the current state of the
        game.
        """
        rows = cols = range(9)
        row_height, col_width, head_width = 4, 9, 6
        width = (len(cols[1:]) * col_width) + head_width + 1 # +1 for boarders
        lines = range((len(rows) * row_height)+1)

        display = ""
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
                line = "  " + self.positions[row][0][0] + "   " + sep
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


class Game(object):
    """
    Top level class, the game object contains all of the other class 
    instances such as the pieces, the board etc.
    """

    def __init__(self):
        """Initialise game object and create required member objects"""
        start_pos = [
            [' ', 'A'  , 'B'  , 'C'  , 'D'  , 'E'  , 'F'  , 'G'  , 'H'   ],
            ['1', 'br1', 'bk1', 'bb1', 'bQ' , 'bK' , 'bb2', 'bk2', 'br2' ],
            ['2', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8' ],
            ['3', False, False, False, False, False, False, False, False ],
            ['4', False, False, False, False, False, False, False, False ],
            ['5', False, False, False, False, False, False, False, False ],
            ['6', False, False, False, False, False, False, False, False ],
            ['7', 'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8' ],
            ['8', 'wr1', 'wk1', 'wb1', 'wQ' , 'wK' , 'wb2', 'wk2', 'wr2' ]]
                     
        self.board = Board(positions=start_pos)
        self.pieces = Game.create_pieces(self)

    def create_pieces(self):
        """
        Creates a object for each piece and stores them in dictionary 
        which can be used later to access pieces by their ref. 

        The source of this data and the refs is the start_pos list, in 
        the game object.
        """
        pieces = {}
        for row, row_content in enumerate(self.board.positions):
            if row == 0: 
                continue
            for col, ref in enumerate(row_content):
                if col == 0: 
                    continue
                if ref: # not an empty list of False (no piece)
                    if ref[0] == 'w':
                        team = 'white'
                    elif ref[0] == 'b':
                        team = 'black'
                    else:
                        msg = ('Could not identify team for item (' + 
                               str(col) + ',' + str(row) + 
                               ') in start_pos, ref:' + ref)
                        exit(msg)

                    if ref[1] == 'K':
                        name = 'king'
                    elif ref[1] == 'Q':
                        name = 'queen'
                    elif ref[1] == 'c':
                        name = 'rook'
                    elif ref[1] == 'b':
                        name = 'bishop'
                    elif ref[1] == 'k':
                        name = 'knight'
                    elif ref[1] == 'p':
                        name = 'pawn'
                    else:
                        raise 'Could not identify name for item (' + \
                              str(col) + ',' + str(row) + ') in start_pos, ref:' + ref                  

                    pieces[ref] = Piece(ref, name, team, row, col)
        return pieces

    def take_turn(self):
        """Initiate prompt to use to take their turn."""
        pass # to follow

def main():
    """Main entry point for program"""
    game = Game()
    print game.board.display

    # test pieces:
    #for ref, piece in game.pieces.items():
    #    print(ref, piece.name, piece.team, str(piece.pos))
    #    print('Valid moves:', piece.valid_moves)

    ##############################################################
    ## simulate moves (to be replaced with turns and player input)
    ##############################################################

    # a valid move...
    game.pieces['wp1'].move(down=-2, right=0, game=game)

    # an invalid move (blocked)...
    game.pieces['bc1'].move(down=-2, right=2, game=game)

    # pause
    if PAUSE_AT_END:
        foo = raw_input('\nPress enter to quit')
        print foo

if __name__ == '__main__':
    main()


##  N O T E S :
##  =========
##  
##  Moves:
##    - all poss combs created against each piece;
##    - filter from there based on conditions, check etc;
##    - make process for user turns / instructions
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


##  Design:
##    - any better way to factor in conditions (on_first etc.) inline with OO style


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
##    - maybe pass occupied into steps function to stop looping once an occiped cell has 
##      cell has been reached?


##  Strategy:
##  maybe I should reconsider approach of calculating all moves allowed?
##  - computationally expensive:
##    - O = MSP (M = valid moves for piece; S = intermediate steps; P = occipied cells;)
##      just for blocking checks
##    - checking if a move puts king in check would also be huge as you would need to
##      consider: 
##      - all of the moves that may be made by each piece on other team (or shorten by
##        checking just if the move from each piece to where King is is possible)
