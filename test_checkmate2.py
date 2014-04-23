#!/usr/bin/python 
"""Unit test for chess.py - non preventable checkmate"""
from chess import *

game = Game() 

# set up game to required position...
game.take_turn('white', 'e7e5')
game.take_turn('black', 'g2g4')
game.take_turn('white', 'e5f4')
game.take_turn('black', 'h2h3') # tmp not reqd once conds in
game.take_turn('white', 'a7a5') # time filler
game.take_turn('black', 'f2f3') # just delete two above when conds in

print('\nControl going back to user.')
print('hint: ready for checkmate if white queen does "d8h4"')

# hand back manual control...
while not game.checkmate:
    game.take_turn('white')
    game.take_turn('black')

# pause         
if PAUSE_AT_END:
    foo = raw_input('\nPress enter to quit')
    print(foo)
