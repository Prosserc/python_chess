#!/usr/bin/env python3
from game import Game
from player import Player, PlayerType
from literals import MOVE_INSTRUCTIONS
from chess_engine import AI

game = None

def start_game():
    return Game()


def prompt_user_for_turn():  # - would go to parse prompt in current CLI
    raise NotImplementedError


def update_user():  # - use for check, checkmate, pieces taken etc
    raise NotImplementedError


def refresh_board():
    raise NotImplementedError


def main(no_of_players=None, ai_player_level_array=None):
    global game
    # todo - all the set up logic is here for now, perhaps move some into a game controller?
    game = start_game()

    if not no_of_players:
        while not no_of_players:
            try:
                no_of_players = int(input("\nWould you like to play with 1 player or 2: "))
                assert(no_of_players <= 2 and no_of_players >= 0)
            except (ValueError, AssertionError):
                print("Please enter just a number 1 or 2")


    players = []
    #create players
    for ai_player_no in range(2):

        # create object for human player if needed...
        if len([p for p in players if p.player_type == PlayerType.human]) < no_of_players:
            players.append(Player(PlayerType.human, game.take_turn()))

        # else create AI player...
        ai_level = None
        if ai_player_level_array:
            ai_level = int(ai_player_level_array[ai_player_no])
        while not ai_level:
            try:
                ai_level = int(input("\nPlease chose a difficulty level between 1 and 3"))
                assert(ai_level >= 1 and ai_level <= 3)
            except(ValueError, AssertionError):
                print("Please enter just a number between 1 and 3")

        ai = AI()
        level_function = {1: ai.random_move,
                          2: ai.level1_move,
                          3: ai.level2_move,
                          4: ai.level3_move}
        players.append(Player(PlayerType.ai, level_function[ai_level]))

    print(MOVE_INSTRUCTIONS)

    while True:
        for player in players:
            if not game.checkmate:
                player.take_move()
            else:
                break

    # pause
    _ = input('\nPress enter to quit')


if __name__ == "__main__":
    main()
