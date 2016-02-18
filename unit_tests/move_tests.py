#!/usr/bin/env python
import unittest
from game import Game, TEAMS
from move import Move


class TestUtils(unittest.TestCase):


    def setUp(self):
        self.test_game = Game();


    def test_initial_move(self):

        # set up specific to this test...
        row, col = 2, 1
        self.test_game.current_team = TEAMS['w']
        occupied, our_team, their_team = self.test_game.get_occupied()
        piece_ref = self.test_game.board.get_piece_ref(row, col)
        piece = self.test_game.pieces[piece_ref]
        move = Move(piece, 2, 0, occupied, our_team, their_team)

        self.assertTrue(move.possible)
        self.assertEqual(move.new_cell_ref, "A4")

if __name__ == "__main__":
    unittest.main()
