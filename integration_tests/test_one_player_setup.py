#!/usr/bin/env python
import api, unittest


class TestAPI(unittest.TestCase):


    def in_prog_test_one_player_setup_ai_l1(self):
        api.main(no_of_players=1, ai_player_level_array=[1])