#!/usr/bin/python 
"""Unit test for chess.py - preventable checkmate"""
from chess import *

game = Game() 

# set up game to required position...
game.take_turn('white', 'e7e5')
game.take_turn('black', 'f2f4')
game.take_turn('white', 'e5f4')
game.take_turn('black', 'a2a4')

print('\nControl going back to user.')
print('hint: ready for check if white queen does "d8h4"')
print('hint: an be stopped if black does g2g3\n')

# hand back manual control...
while not game.checkmate:
    game.take_turn('white')
    game.take_turn('black')

# pause         
if PAUSE_AT_END:
    foo = raw_input('\nPress enter to quit')
    print(foo)
