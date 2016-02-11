#!/usr/bin/python
"""Unit test for chess.py - preventable checkmate"""
from game import Game
from time import sleep
from utils import shout

SLEEP_SECS = 0.2  # (less than 0.2 can cause issues with windows cmd prompt)
game = Game()


def main():

    # set up game to required position...
    simulate_turn('white', 'a2a4')
    simulate_turn('black', 'e7e5')
    simulate_turn('white', 'f2f4')
    simulate_turn('black', 'e5f4')
    simulate_turn('white', 'a4a5')
    simulate_turn('black', 'd8h4')
    simulate_turn('white', 'g2g3')
    simulate_turn('black', 'h4g3')

    try:
        assert game.current_team == 'black'
        assert game.checkmate
        shout("Test worked")
    except AssertionError:
        print("Tests did not work - the game should be in checkmate now!")


def simulate_turn(team, prompt_input):
    game.take_turn(team, prompt_input)
    sleep(SLEEP_SECS)


if __name__ == "__main__":
    main()
