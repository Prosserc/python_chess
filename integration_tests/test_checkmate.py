#!/usr/bin/python 
"""Unit test for chess.py - preventable checkmate"""
from game import Game

game = Game() 

# set up game to required position...
game.take_turn('white', 'a2a4')
game.take_turn('black', 'e7e5')
game.take_turn('white', 'f2f4')
game.take_turn('black', 'e5f4')
game.take_turn('white', 'a4a5')
game.take_turn('black', 'd8h4')
game.take_turn('white', 'g2g3')
game.take_turn('black', 'h4g3')

try:
    assert(game.checkmate)
except:
    print("Game should be in checkmate now!")

print("If you got this far it probably worked!")
