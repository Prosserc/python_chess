#!/usr/bin/env python
import unittest, game, move


class TestUtils(unittest.TestCase):


    def setUp(self):
        self.test_game = Game();


    def check_initial_move(self):

        # set up specific to this test...
        self.test_game.current_team = game.TEAMS['w']
        occupied, our_team, their_team = self.test_game.get_occupied()
        piece_ref = selftest_game.board.get_piece_ref(2, 1)

        if piece_ref:
            piece = self.test_game.pieces[piece_ref]

if __name__ == "__main__":
    unittest.main()
