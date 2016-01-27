#!/usr/bin/env python
"""
Called from python_chess.game. This version is used for ASCII mode.
"""
from utils import VERBOSE, col_no_to_letter, WRONG_ENTRY_POINT_MSG


class Board(object):
    """
    Used to represent the current state of play, record all
    current positions and interacts with display. The display is 
    intended to be logically separate from the rest of the game so 
    that the user interface can be replaced as required.
    """


    def __init__(self, pos):
        """
        Create board display based on game.positions passed in.
        """
        self.positions = pos
        self.printable_positions = []
        header_row = [' '] + [col_head.ljust(3) for col_head in sorted(pos[1].keys())]
        self.printable_positions.append(header_row)
        for row in sorted(pos.keys(), reverse=True):
            self.printable_positions.append([str(row)] +
                                            [pos[row][col] for col in sorted(pos[row].keys())])


    def draw_board(self):
        """
        ASCII display showing the current state of the game.
        """
        rows = cols = range(9)
        row_height, col_width, head_width = 4, 9, 5
        width = (len(cols[1:]) * col_width) + head_width + 1 # +1 for boarders
        lines = range((len(rows) * row_height)+1)

        display = "\n"*20 if not VERBOSE else "\n"*2
        for i in lines:
            row = int(i/4) # cell down (0-8)
            sep = "|" if row > 0 else " "

            # if at row boundary...
            if i%row_height == 0:
                # if last row or first row after headings
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
                line = "  " + self.printable_positions[row][0][0] + "  " + sep
                for col in cols[1:]:
                    if self.printable_positions[row][col]:
                        piece = self.printable_positions[row][col][:2]
                        pad1 = " "*(int((col_width-1)/2)-1)
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
        """
        Get a piece object from the positions list.
        """
        # ranks in chess start from 1 at bottom, adjust for reverse in positions
        print("In get_piece_ref, rank set to: {0}, _file set to: {1}".format(rank, _file)) #TMP
        row = rank
        col = col_no_to_letter(_file)
        if VERBOSE: print("row set to: {0}, col set to {1}".format(row, col)) #TMP
        if VERBOSE: print("self.positions[row][col] set to {0}".format(self.positions[row][col]))
        return self.positions[row][col]   


    def update_board(self, old_pos, new_pos, piece_ref):
        """
        Reflect a successful move on the board positions.
        """
        old_rank, new_rank = old_pos[0], new_pos[0]
        old_file, new_file = old_pos[1], new_pos[1]
        self.positions[old_rank][old_file] = False
        self.positions[new_rank][new_file] = piece_ref
        self.printable_positions[9-old_rank][old_file] = False
        self.printable_positions[9-new_rank][new_file] = piece_ref

        ## todo cleanup:
        ## - this is messed up, need to think of a better solution that printable_pos...


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
