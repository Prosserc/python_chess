#!/usr/bin/env python3
from game import Game
from literals import MOVE_INSTRUCTIONS

game = None

def start_game():
    return Game()


def prompt_user_for_turn():  # - would go to parse prompt in current CLI
    raise NotImplementedError


def update_user():  # - use for check, checkmate, pieces taken etc
    raise NotImplementedError


def refresh_board():
    raise NotImplementedError


def main(players=None, ai_player_level_array=None):
    global game
    # todo - all the set up logic is here for now, perhaps move some into a game controller?
    game = start_game()

    if not players:
        while not players:
            try:
                players = int(input("\nWould you like to play with 1 player or 2: "))
                assert(players <= 2 and players >= 0)
            except (ValueError, AssertionError):
                print("Please enter just a number 1 or 2")

    # todo refactor draft
    if players < 2:
        for ai_player_no in range(2 - players):
            if ai_player_level_array:
                ai_level = int(ai_player_level_array[ai_player_no])
            ai_level = None
            while not ai_level:
                try:
                    ai_level = int(input("\nPlease chose a difficulty level between 1 and 3"))
                    assert(ai_level >= 1 and ai_level <= 3)
                except(ValueError, AssertionError):
                    print("Please enter just a number between 1 and 3")

            


    # add set up func for 1/2 player options etc
    print(MOVE_INSTRUCTIONS)
    # _ = input('\nPress enter to continue...')

    while not game.checkmate:
        game.take_turn('white')
        game.take_turn('black')

    # pause
    _ = input('\nPress enter to quit')


if __name__ == "__main__":
    main()
