python_chess
============

In progress... I am initially working on a basic two player chess game in python. Once I have finished ascii version I may make a better UI for it.  I hope to be able to create an AI version of this in the future to allow for one player games as well. I will start by collecting a record of all moves / outcomes on every game to start to build data that can be used for probabilistic models in the AI. 

Example Board:
-------------

<a href="http://tinypic.com?ref=2ro5pqo" target="_blank"><img src="http://i60.tinypic.com/2ro5pqo.png" border="0" alt="Image and video hosting by TinyPic"></a>

Left to do on basic two player ASCII mode:
-----------------------------------------

1. Swaps (pawn promotion)
2. Castling
3. En Passant restrictions around only one opportuinity to take???
4. Draw Rules:
   1. King not in check, has not move and cannot?
   2. After 50 moves without a pawn being moved or peice being taken (50 move rule)
5. Record data from moves (incl other poss?) for later use in AI.
6. Heading above board i.e. whos turn, in_check? etc...
7. Help menu
