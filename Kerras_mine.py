import Minesweeper_game as M
from sklearn.model_selection import train_test_split
import numpy as np
import tensorflow as tf


# The model will first be trained with a set of random game plays.  The input will be the gameboard.
# The output needs to be a list of 3 numbers: [1 or 0, x coord, y coord].
# The model needs to be given a board, and decide what the best move is.
# Im going to train with a large board, and few mines, to decrease the chance of random solitary numbers.


# The model will have access to both the gameboard and trueboard to start, and learn to predict where mines are.
# I will then implement some form of scoring system to further inform the model, and allow it to play longer games.


GAME_LENGTH = 6
DATASETS = 5000
BOARDSIZE = 10
MINES = 10

trueboards_list = []
gameboards_list = []

def prep_data(game_length:int,
              boardsize:int,
              mines:int,
              datasets:int,
              truelist:list,
              gamelist:list
              ):
    """Outputs the desired number of gameboards and trueboards to the given list."""
    for _ in range(datasets):
        
        game = M.Minesweeper(boardsize, mines)
        game.populate(False)
        for _ in range(game_length):
            x = M.random.randint(1,boardsize)
            y = M.random.randint(1,boardsize)
            game.click(x,y, False)

        if np.sum(game.gameboard == 0) >= 6:
            truelist.append(game.board)
            gamelist.append(game.gameboard)



prep_data(GAME_LENGTH,BOARDSIZE,MINES,DATASETS,
          trueboards_list,gameboards_list)

print("Data: ", len(gameboards_list))

trueboards = np.array(trueboards_list)
gameboards = np.array(gameboards_list)


# The model is going to learn to output the coordinates of the cell it thinks is most likely to contain a mine.
# First, however, I am going to get it to just bruteforce predict the board to see how capable it will be at this.

X = gameboards
y = trueboards

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

y_train[y_train == -1] = 9  # All mines labeled as 9
y_train[y_train == 100] = 10  # All empties labeled as 10
y_train[y_train == 101] = 11  # All borders labeled as 11

input_shape = BOARDSIZE+2
num_classes = 12
# Define the model
model = tf.keras.models.Sequential([
    # Input layer
    tf.keras.layers.Input(shape=(input_shape, input_shape, 1)),
    
    # Convolutional layer
    tf.keras.layers.Conv2D(64, (5, 5), activation='relu'),
    
    # Additional layers as needed
    tf.keras.layers.Flatten(),
    
    # Dense layer before output
    tf.keras.layers.Dense(256 * num_classes, activation='relu'),  # Increase capacity

    tf.keras.layers.Dense(128 * num_classes, activation='relu'),  # Increase capacity
    
    # Output layer for a 12x12 board with num_classes per cell
    tf.keras.layers.Dense(12 * 12 * num_classes, activation='linear'),
    
    # Reshape to (12, 12, num_classes) and apply softmax over num_classes
    tf.keras.layers.Reshape((12, 12, num_classes)),
    tf.keras.layers.Softmax(axis=-1)
])
                                    


model.summary()

model.compile(optimizer=tf.optimizers.Adam(),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

y_test[y_test == -1] = 9  # All mines labeled as 9
y_test[y_test == 100] = 10  # All empties labeled as 10
y_test[y_test == 101] = 11  # All borders labeled as 11

model.fit(X_train, y_train, epochs=15)

loss, accuracy = model.evaluate(X_test, y_test)
print("Test Loss:", loss)
print("Test Accuracy:", accuracy)

test_game = M.Minesweeper(BOARDSIZE, MINES)
test_game.populate()
for _ in range(3):
        x = M.random.randint(1,BOARDSIZE)
        y = M.random.randint(1,BOARDSIZE)
        test_game.click(x,y)
        
test_game.basicshow()
input_board = np.array(test_game.gameboard)  # Ensure it's a numpy array
reshaped_board = input_board.reshape(1, 12, 12, 1)  # Reshape to include batch and channel dimensions

predictions = model.predict(reshaped_board)

# Convert probabilities to class labels
class_labels = np.argmax(predictions, axis=-1)

print(class_labels)

model.save('Keras_solver_1.keras') #  Saves the model

# This was a good start, and worked broadly how I expected it to. After some tweaking, it has grasped the idea that
# the numbers represent the number of mines touching, without this information being directly taught. It struggles
# with blending between the areas it can and cant predict, and I think I want my next model to predict in a more human 
# fashion. I am also going to try creating an extension of this model to actually play the game.
