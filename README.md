python_chess
============

In progress... I am initially working on a basic chess game in python. Once I have finished the ascii (text) version I may make a better UI for it. This started out as just a two player game, but a basic chess engine to allow for one player games is also in progress.

Example Board:
-------------

<a href="http://tinypic.com?ref=2ro5pqo" target="_blank"><img src="http://i60.tinypic.com/2ro5pqo.png" border="0" alt="Image and video hosting by TinyPic"></a>

Left to do on basic two player ASCII mode:
-----------------------------------------

1. Swaps (pawn promotion);
2. Castling;
3. En Passant restrictions around only one opportuinity to take???
4. Draw Rules:
   1. King not in check, has not move and cannot?
   2. After 50 moves without a pawn being moved or peice being taken (50 move rule);
5. Heading above board i.e. whos turn, in_check? etc...
6. Help menu

Left to do on bacic chess engine (for one player mode):
------------------------------------------------------

1. Generalise code to look ahead x moves;
2. Improve endgame - needs to evaluate potential for checkmate (not just takes) and weight moves accordingly;
3. Create memory (tmp objects) for the moves being considered so that state of game is correct at each point of the potential move branch being considered;
