python_chess
============

In progress... I am initially working on a basic two player chess game in python. Once I have finished ascii version I may make a better UI for it.  I hope to be able to create an AI version of this in the future to allow for one player games as well. I will start by collecting a record of all moves / outcomes on every game to start to build data that can be used for probabilistic models in the AI. 

Left to do on basic two player ASCII mode:
-----------------------------------------

1) Calculating moves allowed:
   a) Debugging / fixes needed on steps between source and destination for move;
   b) Filters based on additional conditions e.g. first move and if taking for pawns etc.;
   c) Filter based on moves that would put you in check (for each possible move):
      - check each player on other side whether they could move to King;
   d) Castling?;
   e) Swap pawns at other side of board;
2) Reflect moves that are allowed in board.display and game.pieces:
   a) incl takes / swaps etc;
3) Build interactive prompts for users to specify moves in turn:
   a) build menu options?:
      - Help;
      - Possible moves?;
      - Pieces taken?;
4) Record data from moves (incl other poss?) for later use in AI.
