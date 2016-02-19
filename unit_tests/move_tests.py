#!/usr/bin/env python
import unittest
from game import Game, TEAMS, DEFAULT_START_POSITIONS
from move import Move
from copy import deepcopy


class TestUtils(unittest.TestCase):


    def setUp(self):
        self.game, self.piece, self.move = None, None, None


    def custom_set_up(self, piece_ref, up, right, custom_start_pos=None):
        """
        Creates a move object for the specified piece and sets self.move
        :param piece_ref: e.g. 'bR1' | 'wN1' | 'bB1' | 'wQ' | 'bK' | 'wp1'
        :param up: an int for the number of rows to move forward
                   (note: negative numbers will move forward for black pieces)
        :param right: an int for the number of columns to move right (negative for left)
        :param custom_start_pos: optional: leave empty for default game start
        """
        if not self.game:
            self.game = Game(custom_start_positions=custom_start_pos)
        self.game.current_team = TEAMS[piece_ref[0]]
        self.piece = self.game.get_piece(piece_ref)
        occupied, our_team, their_team = self.game.get_occupied()
        self.move = Move(self.piece, up, right, occupied, our_team, their_team)


    def test_pawn_initial_two_step_move(self):

        start_pos = deepcopy(DEFAULT_START_POSITIONS)
        start_pos[2]["A"] = False
        start_pos[4]["A"] = 'wp1'

        self.custom_set_up('wp1', 2, 0, custom_start_pos=start_pos)
        self.assertFalse(self.move.possible)


    def test_pawn_subsequent_two_step_move(self):
        self.custom_set_up('wp1', 2, 0)
        self.assertTrue(self.move.possible)
        self.assertEqual(self.move.new_cell_ref, "A4")


    def test_pawn_taking(self):

        start_pos = {
            8: dict(A='bR1', B='bN1', C='bB1', D='bQ', E='bK', F='bB2', G='bN2', H='bR2'),
            7: dict(A='bp1', B=False, C='bp3', D='bp4', E='bp5', F='bp6', G='bp7', H='bp8'),
            6: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            5: dict(A=False, B='bp2', C=False, D=False, E=False, F=False, G=False, H=False),
            4: dict(A='wp1', B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            3: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            2: dict(A=False, B='wp2', C='wp3', D='wp4', E='wp5', F='wp6', G='wp7', H='wp8'),
            1: dict(A='wR1', B='wN1', C='wB1', D='wQ', E='wK', F='wB2', G='wN2', H='wR2')}

        self.custom_set_up('wp1', 1, 1, custom_start_pos=start_pos)
        self.assertTrue(self.move.possible,
                        msg="invalid reason: {0}".format(self.move.invalid_reason))
        self.assertEqual(self.move.new_cell_ref, "B5")


    @staticmethod
    def switch_cell_contents(positions, old_cell_refs, new_cell_refs):
        """
        Switch each cell in old_cell_refs with the corresponding cell in new_cell_refs.
        :param positions: a dict of dicts in the format of DEFAULT_START_POSITIONS
        :param old_cell_refs: a collection of cell refs containing start positions
        :param new_cell_refs: a collection of the same size, with the new positions
        :return: None
        """
        for i, old_cell_ref in Enumerate(old_cell_refs):
            old_row, old_col = old_cell_ref[1].Upper()
            new_row, new_col = new_cell_refs[i][0], new_cell_refs[i][0]
            tmp = positions[old_row][old_col]
            positions[old_row, old_col] = positions[new_row, new_col]
            positions[new_row, new_col] = tmp


if __name__ == "__main__":
    unittest.main()
