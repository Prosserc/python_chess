#!/usr/bin/python 

verbose = True 

class Piece:

    def __init__(self, id, type, team, x, y):
        self.id = id
        self.type = type
        self.team = team
        self.pos = [x, y]
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
        if self.team.lower() == 'black':
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

    def move(self, forward, sideways):

        valid, invalid_reason = True, []

        # check valid moves for piece
        if [forward, sideways] not in [move[:2] for move in self.valid_moves]:
            invalid_reason.append('piece')
            print(str(forward) + ' steps forward and ' + str(sideways) + 
                  ' steps right is not a valid move for this piece')

        moves_allowed = get_moves_allowed(self)

        # check board boundaries
        if [forward, sideways] not in [move[:2] for move in moves_allowed]
            invalid_reason.append('boundaries')
            print(str(forward) + ' steps forward and ' + str(sideways) + 
                  ' steps right would move outside of the boards boundaries')

    def get_moves_allowed(self):

        if verbose: print('Getting all valid moves for ' + self.id + ' from: ' + str(self.pos))

        # filter valid moves based on board boundaries
        moves_allowed = []
        for move in self.valid_moves:
            new_y = self.y + move[0] # forward
            new_x = self.x + move[1] # sideways
            if new_x in range(9) and new_y in range(9):
                moves_allowed.append([new_x, new_y])

        if verbose: print(str(len(moves_allowed)) + ' moves possible within boundaries'

        # filter based on position of other pieces (blocking)
        occupied = []
        for id, piece in game.pieces.items():
            if id != self.id:
                occupied.append(piece.pos)

        for move in moves_allowed:
            move_okay = True
            steps = get_steps(self, moves_allowed, move[0], move[1])

        # check that all any condtions on the move are satisfied

    def get_steps(self, moves_allowed, forward, sideways):

        steps = []
        for move in moves_allowed:
            # exclude any that move more than one space
            if move in self.one_space_moves:
                # handle by type to deal with exceptions
                if self.type != 'pawn' and self.type != 'knight':
                    if forward and sideways: # this means anything other than zero in both
                        # consider calcing vertical and horizontal distance before and after
                        # move and only adding step if it gets closer?
                        steps.append(move)
                    elif forward:
                        #...cond
                        steps.append(move)
                    elif sideways:
                        #... cond
                        steps.append(move)


class Game:

    def __init__(self):
        # exact order TBC..., blanks to avoid zero indexing
        #                     may come in handy for some sort of row / col totals
        start_pos = [[[]    , []   , []   , []   , []   , []   , []   , []   , []    ],
                     [[]    , 'bc1', 'bk1', 'bb1', 'bK' , 'bQ' , 'bb2', 'bk2', 'bc2' ],
                     [[]    , 'bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8' ],
                     [[]    , False, False, False, False, False, False, False, False ],
                     [[]    , False, False, False, False, False, False, False, False ],
                     [[]    , False, False, False, False, False, False, False, False ],
                     [[]    , False, False, False, False, False, False, False, False ],
                     [[]    , 'wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8' ],
                     [[]    , 'wc1', 'wk1', 'wb1', 'wK' , 'wQ' , 'wb2', 'wk2', 'wc2' ]]
                     
        self.board = Board(positions=start_pos)
        self.pieces = Game.create_pieces(self)

    def create_pieces(self):
        pieces = {}
        for y, row in enumerate(self.board.positions):
            for x, id in enumerate(row):
                if id: # not an empty list of False (no piece)
                    if id[0] == 'w':
                        team = 'white'
                    elif id[0] == 'b':
                        team = 'black'
                    else:
                        raise('Could not identify team for item (' + \
                              str(x) + ',' + str(y) + ') in start_pos, id:' + id)

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
                              str(x) + ',' + str(y) + ') in start_pos, id:' + id)                       

                    pieces[id] = Piece(id, type, team, x, y)
        return pieces


class Board:

    def __init__(self, positions):
        self.positions = positions
        self.display = Board.draw_board(self)

    def move_peice(self, piece):
        # to follow...
        pass

    def draw_board(self):

        rows = cols = range(1,9)
        row_height, col_width = 4, 9
        length = (len(cols) * col_width) + 1 # allows for boarders
        lines = range(1,(len(rows) * row_height) + 1)

        # print empty chess board
        display = "-" * length + "\n"
        for i in lines:
            y = (i/4)+1 # cell down (1-8)
            if i == max(lines):
                row = "-"*length
            elif i%row_height == 0:
                row = "|"
                for x in cols:
                    row = row + "-"*(col_width-1) + "|"
            elif i%row_height == 2: # line where a pieces would go
                row = "|"
                for x in cols:
                    if self.positions[y][x]:
                        piece = self.positions[y][x][:2]
                        pad1 = " "*(((col_width-1)/2)-1)
                        pad2 = " "*((col_width-(len(pad1)+len(piece)))-1)
                        row = row + pad1 + piece + pad2 + "|"
                    else:
                        row = row + " "*(col_width-1) + "|"
                
            else:
                row = "|"
                for x in cols:
                    row = row + " "*(col_width-1) + "|"
            display = display + row + "\n"
        return display


def main():
    
    game = Game()
    print game.board.display

    # test pieces:
    #for id, piece in game.pieces.items():
    #    print(id, piece.type, piece.team, piece.pos, piece.allowed_to_jump)
    #    print('Valid moves:', piece.valid_moves)

    ##############################################################
    ## simulate moves (to be replaced with turns and player input)
    ##############################################################

    # a valid move...
    game.pieces['wp1'].move(2, 0)

    # pause
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
