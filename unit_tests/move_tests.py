#!/usr/bin/env python
import unittest
from game import Game, TEAMS
from move import Move


class TestUtils(unittest.TestCase):


    def test_initial_move(self):
        test = Game()

        # set up specific to this test...
        row, col = 2, 1
        test.current_team = TEAMS['w']
        occupied, our_team, their_team = test.get_occupied()
        piece_ref = test.board.get_piece_ref(row, col)
        piece = test.pieces[piece_ref]
        move = Move(piece, 2, 0, occupied, our_team, their_team)

        self.assertTrue(move.possible)
        self.assertEqual(move.new_cell_ref, "A4")


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

        test = Game(custom_start_positions=start_pos)


    @staticmethod
    def __helper_get_piece(game, piece_ref):
        pass # todo


if __name__ == "__main__":
    unittest.main()
