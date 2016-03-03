#!/usr/bin/env python3


def start_game():
    raise NotImplementedError


def prompt_user_for_turn():  # - would go to parse prompt in current CLI
    raise NotImplementedError


def update_user():  # - use for check, checkmate, pieces taken etc
    raise NotImplementedError


def refresh_board():
    raise NotImplementedError


if __name__ == "__main__":
    start_game()
