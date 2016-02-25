#!/usr/bin/env python3
import unittest
from game import Game

class TestGame(unittest.TestCase):


    def setUp(self):
        self.game = Game(default_logging=False)
        self.maxDiff = None


    def tearDown(self):
        del self.game


    def test_full_game(self):
        self.helper_setup_checkmate()
        self.assertTrue(self.game.checkmate)
        self.assertTrue(self.game.current_team, "white")


    def test_list_moves_for_pawn_first_move(self):
        ref = 'wp2'
        pieces = { ref: self.game.get_piece(ref) }
        print("Getting all possible moves ({0}) from pawns 1st move...".format(ref))
        moves, _ = self.game.get_all_possible_moves(pieces=pieces, list_moves=True, team='white')
        expected_refs = ['B3', 'B4']
        found_refs = sorted([mv.new_cell_ref for mv in moves[ref]])
        self.assertEqual(found_refs, expected_refs)


    def test_list_moves_for_pawn_second_move(self):
        self.game.take_turn('white', 'a2a4')
        self.game.take_turn('black', 'e7e5')
        ref = 'wp1'
        pieces = { ref: self.game.get_piece(ref) }
        print("Getting all possible moves ({0}) from pawns 2nd move...".format(ref))
        moves, _ = self.game.get_all_possible_moves(pieces=pieces, list_moves=True, team='white')

        expected_refs = ['A5']
        found_refs = sorted([mv.new_cell_ref for mv in moves[ref]])
        self.assertEqual(found_refs, expected_refs)


    def test_list_moves_for_check(self):
        self.helper_setup_check()
        print("Getting all possible moves (any piece) from check...")
        moves, _ = self.game.get_all_possible_moves(list_moves=True, team='white')

        expected_piece_ref = 'wp7'
        found_piece_refs = sorted(list(moves.keys()))
        self.assertEqual([expected_piece_ref], found_piece_refs)

        expected_cell_refs = ['G3']
        found_cell_refs = sorted([mv.new_cell_ref for mv in moves[expected_piece_ref]])
        self.assertEqual(found_cell_refs, expected_cell_refs)





    # ---------------------------------------------------------------------------------------
    # -------------------------   H E L P E R   F U N CT I O N S   --------------------------
    # ---------------------------------------------------------------------------------------

    def helper_setup_check(self):
        # set up game to required position...
        self.game.take_turn('white', 'a2a4')
        self.game.take_turn('black', 'e7e5')
        self.game.take_turn('white', 'f2f4')
        self.game.take_turn('black', 'e5f4')
        self.game.take_turn('white', 'a4a5')
        self.game.take_turn('black', 'd8h4')


    def helper_setup_checkmate(self):
        self.helper_setup_check()
        self.game.take_turn('white', 'g2g3')
        self.game.take_turn('black', 'h4g3')


if __name__ == "__main__":
    unittest.main()
