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
        self.col = col
        self.pos = [row, col]
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
