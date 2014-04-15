#!/usr/bin/python 

verbose = True 
pause_at_end = False

class Piece:

    def __init__(self, id, type, team, row, col):
        self.id = id
        self.type = type
        self.team = team
        self.row = row
        self.col = col
        self.pos = [row, col]
        self.valid_moves = Piece.get_valid_moves(self)
        self.one_space_moves = Piece.get_one_space_moves(self)
        self.move_cnt = 0
        self.taken = False

    def get_valid_moves(self):

        # valid moves for each type of piece:
        # (forward, sideways[+right/-left], <condition1>, ..., <conditionN>)
        move_dict = {'king':   [[1, 1], [1, 0], [1, -1], [0, 1],
                                [0, -1], [-1, 1], [-1, 0], [-1, -1]],
                     'castle':  [[i, 0] for i in range(1,9)] + \
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
                                [2, 1, 'on_take', 'on_first'],
                                [2, -1, 'on_take', 'on_first'],
                                [1, 0],
                                [2, 0, 'on_first']]
                     }
        move_dict['queen'] = move_dict['castle']+move_dict['bishop']
        
        valid_moves = move_dict[self.type.lower()]

        # invert direction for blacks (as they will move down board)
        if self.team.lower() == 'white':
            for move in valid_moves:
                move[0] = move[0] * -1

        # note knights ability to jump
        if self.type.lower() == 'knight':
            self.allowed_to_jump = True
        else:
            self.allowed_to_jump = False
            
        return valid_moves

    def get_one_space_moves(self):
        # done here rather than when moving so that it is only done once per piece
        one_space_moves = []
        for move in self.valid_moves:
            if min(move[:2]) >= -1 and max(move[:2]) <= 1:
                one_space_moves.append(move)

        return one_space_moves

    def move(self, forward, sideways, game):

        invalid_reasons = []

        # check valid moves for piece
        if [forward, sideways] not in [move[:2] for move in self.valid_moves]:
            invalid_reasons.append('piece')
            print(str(forward) + ' steps forward and ' + str(sideways) + 
                  ' steps right is not a valid move for this piece')

        moves_allowed = Piece.get_moves_allowed(self, game)

        if [forward, sideways] in moves_allowed:
            return True, None
        return False, invalid_reasons

    def get_moves_allowed(self, game):

        if verbose: 
            print('Getting valid moves for ' + self.id + ' from ' + str(self.pos))

        # filter valid moves based on board boundaries
        moves_allowed = []
        for move in self.valid_moves:
            new_row = self.row + move[0] # forward
            new_col = self.col + move[1] # sideways
            if new_col in range(1,9) and new_row in range(1,9):
                moves_allowed.append([new_row, new_col])

        if verbose: 
            print(str(len(moves_allowed)) + ' moves possible within boundaries')

        # get list of occupied cells
        occupied = []
        for id, piece in game.pieces.items():
            if id != self.id:
                occupied.append(piece.pos)

        # filter based on position of other pieces (blocking)
        if not self.allowed_to_jump:
            for move in moves_allowed[:]:
                move_okay = True
                steps = Piece.get_steps(self, move[0], move[1], moves_allowed)

                # go through each step, if in occupied list to check if blocked
                tmp_pos = self.pos
                for step in steps:
                    tmp_pos = [tmp_pos[0]+step[0], tmp_pos[1]+step[1]]
                    if tmp_pos in occupied:
                        move_okay = False
                        break

                if not move_okay:
                    moves_allowed.remove(move)

        # check that any conditions on the move are satisfied


        # check that move would not put your King in check


        return moves_allowed

    def get_steps(self, forward, sideways, moves_allowed):
        """Return all intermediate steps required (i.e. not inlcuding final step)"""

        # get shoretlist of single space moves allowed
        for move in moves_allowed[:]:
            if move not in self.one_space_moves:
                moves_allowed.remove(move)

        steps = []

        while abs(forward) > 1 or abs(sideways) > 1:
            fwd = -1 if forward < 0 else 1
            sdw = -1 if sideways < 0 else 1
            if abs(forward) > abs(sideways) and [fwd, 0] in moves_allowed:
                steps.append([fwd, 0])
                forward += fwd
            elif abs(forward) == abs(sideways) and [fwd, sdw] in moves_allowed:
                steps.append([fwd, sdw])
                forward += fwd
                sideways += sdw
            elif abs(forward) < abs(sideways) and [0, sdw] in moves_allowed:
                steps.append([fwd, sdw])
                forward += fwd                
            else:
                print("\nHmmm, not sure I should have ended up here. This means that I can " +
                      "not move one step in the direction that I need to? Add more debug " +
                      "messages to work out whats going on.")
                raise Exception("No valid steps available.")

        return steps


class Board:

    def __init__(self, positions):
        self.positions = positions
        self.display = Board.draw_board(self)

    def move_peice(self, piece):
        # to follow...
        pass

    def draw_board(self):

        rows = cols = range(9)
        row_height, col_width, head_width = 4, 9, 6
        width = (len(cols[1:]) * col_width) + head_width + 1 # allows for boarders
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


class Game:

    def __init__(self):
        # exact order TBC...
        start_pos = [[' ', 'A'  , 'B'  , 'C'  , 'D'  , 'E'  , 'F'  , 'G'  , 'H'   ],
                     ['1', 'bc1', 'bk1', 'bb1', 'bK' , 'bQ' , 'bb2', 'bk2', 'bc2' ],
                     ['2', 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8' ],
                     ['3', False, False, False, False, False, False, False, False ],
                     ['4', False, False, False, False, False, False, False, False ],
                     ['5', False, False, False, False, False, False, False, False ],
                     ['6', False, False, False, False, False, False, False, False ],
                     ['7', 'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8' ],
                     ['8', 'wc1', 'wk1', 'wb1', 'wK' , 'wQ' , 'wb2', 'wk2', 'wc2' ]]
                     
        self.board = Board(positions=start_pos)
        self.pieces = Game.create_pieces(self)

    def create_pieces(self):
        pieces = {}
        for row, row_content in enumerate(self.board.positions):
            if row == 0: continue
            for col, id in enumerate(row_content):
                if col == 0: continue
                if id: # not an empty list of False (no piece)
                    if id[0] == 'w':
                        team = 'white'
                    elif id[0] == 'b':
                        team = 'black'
                    else:
                        msg = 'Could not identify team for item (' + \
                              str(col) + ',' + str(row) + ') in start_pos, id:' + id
                        exit(msg)

                    if id[1] == 'K':
                        type = 'king'
                    elif id[1] == 'Q':
                        type = 'queen'
                    elif id[1] == 'c':
                        type = 'castle'
                    elif id[1] == 'b':
                        type = 'bishop'
                    elif id[1] == 'k':
                        type = 'knight'
                    elif id[1] == 'p':
                        type = 'pawn'
                    else:
                        raise('Could not identify type for item (' + \
                              str(col) + ',' + str(row) + ') in start_pos, id:' + id)                       

                    pieces[id] = Piece(id, type, team, row, col)
        return pieces


def main():
    
    game = Game()
    print game.board.display

    # test pieces:
    #for id, piece in game.pieces.items():
    #    print(id, piece.type, piece.team, str(piece.pos))
    #    print('Valid moves:', piece.valid_moves)

    ##############################################################
    ## simulate moves (to be replaced with turns and player input)
    ##############################################################

    # a valid move...
    game.pieces['wp2'].move(-2, 0, game)

    # pause
    if pause_at_end:
        foo = raw_input('\nPress enter to quit')

if __name__ == '__main__':
    main()


##  N O T E S :
##  =========
##  
##  Moves:
##    - all poss combs created against each piece;
##    - filter from there based on:
##      - their current position e.g. to allow for the boundaries of the display;
##      - other pieces current positions i.e. what would be blocked;
##    - make process for user turns / instructions
##    - write info to database (for future AI data)


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
