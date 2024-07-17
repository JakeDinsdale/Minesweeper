# Minesweeper
A Repo for my Minesweeper project, using various machine/deep learning methods to play minesweeper

~~~Minesweeper_game.py~~~

This is the base game I am using to train the models with. I wanted it to be simple, with very basic commands that were easy for a model to interperet.

It has .board, sometimes referred to as the "trueboard", which holds all the values for the minesweeper board. The .gameboard holds all the values the model/player has access to
while playing the game.

The populate function creates both boards, including generating the number of mines touching each square. A border is also created to allow easy handling of edgecases further in.

The click function just clicks on an unknown square, and handles the result of this action. The mark function does similar, but instead marks/flags a square.

There are currently 3 show methods: 

basicshow - Just shows the game board as an array.
devshow - Shows both the gameboard and trueboard as arrays
showboard - WIP. Shows the board graphically using pyplot

The file also contains a test game, requiring the user to input clicks/marks as prompted when the file is run.

~~~Kerras_mine.py~~~

This file generates a model that attempts to predict boards in their entirety. While this method is clearly flawed, it serves as a base point for future solving methods. The model is saved as Kerras_solver_1.keras. The variables below can be easily edited as required:

Game_length - Decides how many clicks should be attempted on each board before storing it for analysis. 
Datasets - Decides how many boards to start with
Boardsize - Sets the size of the boards used to train the model (variable boardsizes coming later, however im not sure they will have a substantial positive effect)
Mines - Sets the number of mines per board. Keep thhis number relatively low to ensure enough of the board is revealed per dataset.

Each board with less than the ZEROS value of 0's revealed will be culled, to allow only boards with valuable information to train the model.

Each board pair is then added to the total list of boards, and the keras model is trained on this list, by providing it with both the gameboard, and its corresponding trueboard.

The file concludes with a test board.