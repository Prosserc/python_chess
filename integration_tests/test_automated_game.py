#!/usr/bin/env python3
"""
Integration test for chess.py - an automated game.
"""
from game import Game
from time import sleep
from chess_engine import AI


# no of seconds to sleep after a move
SLEEP_SECS = 0.2  # (less than 0.2 can cause issues with windows cmd prompt)
DRAWING_ON = True


def play(turns=50):
    """
    Launch test game
    :param turns: the number of turns before a draw is declared
    """
    # create top level object that starts the game, draws the pieces etc.
    ai = AI()
    game, team = Game(), 'None'

    # the level will hopefully just be a param in a generic function eventually
    level_function = {0: ai.random_move, 1: ai.level1_move, 2: ai.level2_move, 3: ai.level3_move}
    team_levels = {'white': 1, 'black': 0}

    while not game.checkmate and game.turns < turns:
        for team in ['white', 'black']:
            if DRAWING_ON:
                print(game.board.draw_board())

            func = level_function[team_levels[team]]
            move_obj = func(game, team)
            game.take_turn(team, prompt=None, move=move_obj)
            sleep(SLEEP_SECS)

    if game.checkmate:
        print('\n CHECKMATE, ' + team + ' team wins.')
    else:
        print('{0} turns have been taken, limit set to: {1}'.format(game.turns, turns))


if __name__ == '__main__':
    play()
