python_chess
============

In progress... 
I am initially working on a basic text based chess game in python. Once I have finished the ascii (text) version I may make a better UI for it or interface with an existing open source UI. This started out as just a two player game, but a basic chess engine to allow for one player games is also in progress.

You can track the development progress on [this Trello board](https://trello.com/b/noOlB5EE/python-chess-current)

Example Board:
-------------

<a href="http://tinypic.com?ref=behd8z" target="_blank"><img src="http://i67.tinypic.com/behd8z.jpg" border="0" alt="Image and video hosting by TinyPic"></a>

The game should be working in it's present state (in 2 player mode with the exception of the rules listed below)...

Usage Instructions:
------------------
Follow the GitHub instructions to clone the project to your desktop and save to somewhere accessible to your PYTHONPATH e.g. C:\Program Files\Python35 if you are running python 3.5 in a Windows environment.
(I will create a setup.py file etc once there is a finished version 1).

To start a game execute `python game.py` from the command line

Detailed instructions for users who do not have python installed or are not familiar with command line interfaces to follow shortly.

Left to do on basic two player ASCII mode:
-----------------------------------------

1. Swaps (pawn promotion);
2. Castling;
3. Draw Rules:
   1. King not in check, has not move and cannot?
   2. After 50 moves without a pawn being moved or peice being taken (50 move rule);
4. Help menu

Left to do on basic chess engine (for one player mode):
------------------------------------------------------

1. Generalise code to look ahead x moves;
2. Improve endgame - needs to evaluate potential for checkmate (not just takes) and weight moves accordingly;
3. Create memory (tmp objects) for the moves being considered so that state of game is correct at each point of the potential move branch being considered;!

