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
        # set up game to required position...
        self.game.take_turn('white', 'a2a4')
        self.game.take_turn('black', 'e7e5')
        self.game.take_turn('white', 'f2f4')
        self.game.take_turn('black', 'e5f4')
        self.game.take_turn('white', 'a4a5')
        self.game.take_turn('black', 'd8h4')
        self.game.take_turn('white', 'g2g3')
        self.game.take_turn('black', 'h4g3')

        self.assertTrue(self.game.checkmate)
        self.assertTrue(self.game.current_team, "white")


    def test_list_moves_for_pawn_first_move(self):
        ref = 'wp2'
        piece_dict = { ref: self.game.get_piece(ref) }
        possible_moves, cnt = self.game.get_all_possible_moves(pieces=piece_dict,
                                                               team='white',
                                                               list_moves=True)
        self.assertEqual(cnt, 2)
        expected_refs = ['B3', 'B4']
        found_refs = sorted([mv.new_cell_ref for mv in possible_moves[ref]])
        self.assertEqual(found_refs, expected_refs)


if __name__ == "__main__":
    unittest.main()
