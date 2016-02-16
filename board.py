#!/usr/bin/env python
"""
Called from python_chess.game. This version is used for ASCII mode.
"""
from utils import col_no_to_letter, WRONG_ENTRY_POINT_MSG, shout, debug
from pprint import pprint


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
        width = (len(cols[1:]) * col_width) + head_width + 1  # +1 for boarders
        lines = range((len(rows) * row_height) + 1)

        display = "\n" * 2
        for i in lines:
            row = int(i / 4)  # cell down (0-8)
            sep = "|" if row > 0 else " "

            # if at row boundary...
            if i % row_height == 0:
                # if last row or first row after headings
                if i == max(lines) or row == 1:
                    line = " " * head_width + "-" * (width - head_width)
                # if first row
                elif row == 0:
                    line = None
                else:
                    line = " " * head_width + sep
                    for _ in cols[1:]:
                        line = line + "-" * (col_width - 1) + sep

            # if line where a pieces could go
            elif i % row_height == 2:
                line = "  {0}  {1}".format(self.printable_positions[row][0][0], sep)
                for col in cols[1:]:
                    if self.printable_positions[row][col]:
                        piece = self.printable_positions[row][col][:2]
                        pad1 = " " * (int((col_width - 1) / 2) - 1)
                        pad2 = " " * ((col_width - (len(pad1) + len(piece))) - 1)
                        line = line + pad1 + piece + pad2 + sep
                    else:
                        line = line + " " * (col_width - 1) + sep

            # normal row
            else:
                line = " " * head_width + sep
                for _ in cols[1:]:
                    line = line + " " * (col_width - 1) + sep

            if line:
                display = display + line + "\n"

        return display


    def get_piece_ref(self, row, col_no):
        """
        Get a piece object from the positions list.
        """
        col = col_no_to_letter(col_no)
        debug("in board.get_piece_ref() self.positions[row][col] set to {0}".format(
            self.positions[row][col]))
        return self.positions[row][col]   


    def update_board(self, old_pos, new_pos, piece_ref):
        """
        Reflect a successful move on the board positions.
        """
        old_row, new_row = old_pos[0], new_pos[0]
        old_col_no, new_col_no = old_pos[1], new_pos[1]
        old_col, new_col = col_no_to_letter(old_col_no), col_no_to_letter(new_col_no)
        self.positions[old_row][old_col] = False
        self.positions[new_row][new_col] = piece_ref
        self.printable_positions[9 - old_row][old_col_no] = False
        self.printable_positions[9 - new_row][new_col_no] = piece_ref

        # todo cleanup:
        # - this is messed up, need to think of a better solution than printable_pos...

    def print_state(self):
        shout("\nboard positions", suffix="\n---------------")
        pprint(self.positions)
        shout("\nprintable positions", suffix="\n-------------------")
        pprint(self.printable_positions)
        print("")


if __name__ == '__main__':
    print(WRONG_ENTRY_POINT_MSG)
