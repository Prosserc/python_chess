#!/usr/bin/env python3
import unittest
from game import Game, TEAMS, DEFAULT_START_POSITIONS
from move import Move
from copy import deepcopy
from literals import INVALID_MOVE_MESSAGES as invalid_move_msg


class TestMove(unittest.TestCase):


    def setUp(self):
        self.game, self.piece, self.move = None, None, None
        self.maxDiff = None


    def tearDown(self):
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
            self.game = Game(custom_start_positions=custom_start_pos, default_logging=False)
        self.game.current_team = TEAMS[piece_ref[0]]
        self.piece = self.game.get_piece(piece_ref)
        occupied, our_team, their_team = self.game.get_occupied()
        self.move = Move(self.piece, up, right, occupied, our_team, their_team)


    def test_invalid_move_for_piece(self):
        self.custom_set_up('wp7', 5, -2)
        self.assertFalse(self.move.possible)
        self.assertEqual(self.move.invalid_reason, invalid_move_msg['piece'])


    def test_out_of_boundaries(self):
        start_pos = TestMove.helper_switch_cells(["B1", "B8"], ["A3", "A6"])
        self.custom_set_up('wN1', 2, -1, custom_start_pos=start_pos)
        self.assertFalse(self.move.possible)
        self.assertEqual(self.move.invalid_reason, invalid_move_msg['boundaries'])


    def test_pawn_initial_two_step_move(self):
        self.custom_set_up('wp1', 2, 0)
        self.assertTrue(self.move.possible)
        self.assertEqual(self.move.new_cell_ref, "A4")


    def test_pawn_subsequent_two_step_move(self):
        start_pos = TestMove.helper_switch_cells(["A2", "E7"], ["A4", "E5"])
        self.custom_set_up('wp1', 2, 0, custom_start_pos=start_pos)
        self.assertFalse(self.move.possible)
        self.assertEqual(self.move.invalid_reason, invalid_move_msg["cond_on_first"])


    def test_pawn_taking(self):
        start_pos = TestMove.helper_switch_cells(["A2", "B7"], ["A4", "B5"])
        self.custom_set_up('wp1', 1, 1, custom_start_pos=start_pos)
        self.assertTrue(self.move.possible,
                        msg="invalid reason: {0}".format(self.move.invalid_reason))
        self.assertEqual(self.move.new_cell_ref, "B5")
        # can't test affect on game.pieces here as this is controller from game.


    def test_move_not_allowed_as_it_puts_you_in_check(self):
        moves_from = ["A2", "C7", "C2", "D8"]
        moves_to = ["A4", "C5", "C4", "A5"]
        start_pos = TestMove.helper_switch_cells(moves_from, moves_to)

        self.custom_set_up("wp4", 1, 0, custom_start_pos=start_pos)
        self.assertFalse(self.move.possible)
        self.assertEqual(self.move.invalid_reason, invalid_move_msg['king'].format('queen', 'A5'))


    # -----------------------------------------------------------------------------------------
    # --------------------   W h o   t e s t s   t h e   t e s t s ?   ------------------------
    # -----------------------------------------------------------------------------------------


    def test_the_test_helper_func_switch_cell_contents(self):

        expected_result = {
            8: dict(A='bR1', B='bN1', C='bB1', D='bQ', E='bK', F='bB2', G='bN2', H='bR2'),
            7: dict(A='bp1', B=False, C='bp3', D='bp4', E='bp5', F='bp6', G='bp7', H='bp8'),
            6: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            5: dict(A=False, B='bp2', C=False, D=False, E=False, F=False, G=False, H='wQ'),
            4: dict(A='wp1', B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            3: dict(A=False, B=False, C=False, D=False, E=False, F=False, G=False, H=False),
            2: dict(A=False, B='wp2', C='wp3', D='wp4', E='wp5', F='wp6', G='wp7', H='wp8'),
            1: dict(A='wR1', B='wN1', C='wB1', D=False, E='wK', F='wB2', G='wN2', H='wR2')}

        # note this helper function allows any board moves (not restricted by game rules)
        adjusted_positions = TestMove.helper_switch_cells(["A2", "B7", "D1"], ["A4", "B5", "H5"])
        self.assertEqual(adjusted_positions, expected_result)


    @staticmethod
    def helper_switch_cells(old_cell_refs, new_cell_refs, positions=DEFAULT_START_POSITIONS):
        """
        Switch each cell in old_cell_refs with the corresponding cell in new_cell_refs.
        :param positions: a dict of dicts in the format of DEFAULT_START_POSITIONS
        :param old_cell_refs: a collection of cell refs containing start positions
        :param new_cell_refs: a collection of the same size, with the new positions
        :return: a new positions object (deep copy of original)
        """
        adj_pos = deepcopy(positions)
        for i, old_cell_ref in enumerate(old_cell_refs):
            old_row, old_col = int(old_cell_ref[1]), old_cell_ref[0].upper()
            new_row, new_col = int(new_cell_refs[i][1]), new_cell_refs[i][0].upper()
            tmp = adj_pos[old_row][old_col]
            adj_pos[old_row][old_col] = adj_pos[new_row][new_col]
            adj_pos[new_row][new_col] = tmp

        return adj_pos


if __name__ == "__main__":
    unittest.main()
