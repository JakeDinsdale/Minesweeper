import numpy as np
import random
import math
from matplotlib import pyplot as plt

from itertools import product

class Minesweeper(): #  Needs tidying up
    def __init__(self,boardsize,mines):
        self.boardsize = boardsize
        self.mines = mines
        self.mines_left = mines
        self.gamestate = True

        self.board = np.zeros([self.boardsize+2,self.boardsize+2])
        self.gameboard = np.zeros([self.boardsize+2,self.boardsize+2])
        self.countarray = np.zeros([self.boardsize+2,self.boardsize+2])
        

    def populate(self, verbose:bool = True):
        
        while self.mines > 0:
            x = math.floor(random.random() * (self.boardsize)) + 1
            y = math.floor(random.random() * (self.boardsize)) + 1
            

            if self.board[x, y] != -1:  # Ensure we don't place a mine where there's already one
                self.board[x, y] = -1
                self.mines -= 1

            
        
        self.board[:,0] = 101
        self.board[:,-1] = 101
        self.board[0,:] = 101
        self.board[-1,:] = 101

        self.gameboard[:,:] = 100
        self.gameboard[:,0] = 101
        self.gameboard[:,-1] = 101
        self.gameboard[0,:] = 101
        self.gameboard[-1,:] = 101
        if verbose:
            print(self.gameboard)

        for x in range(1,self.boardsize+1):
            for y in range(1,self.boardsize+1):
                count = 0
                if not self.board[x,y] == -1:
                    
                
                    for i,j in product(range(-1,2), repeat=2):
                        if not (i == 0 and j == 0):
                            if self.board[x+i, y+j] == -1:
                                count += 1
                        
                    self.board[x,y] = count
            
        

    def showboard(self):
        plt.figure(figsize=(8,8))
        plt.imshow(self.board, cmap = "coolwarm", interpolation=None)
        plt.colorbar(label = "Mines nearby")
        plt.title("Minesweeper Board")
        plt.show()

    def basicshow(self):
        print(self.gameboard)

    def devshow(self):
        print(self.gameboard,"\n")
        print(self.board)

    def mark(self,x,y):
        if self.gameboard[x,y] == 100:
            self.gameboard[x,y] = -100

        if self.board[x,y] == -1:
            self.mines_left -= 1

        if self.mines_left == 0:
            print("You Win!!")

    def click(self,x,y, verbose:bool = True):
        
        
        
        if self.board[x,y] == 0:
            
            for i,j in product(range(-1,2), repeat=2):
                self.gameboard[x+i,y+j] = self.board[x+i,y+j]
                
                if self.board[x+i,y+j] == 0 and self.countarray[x+i,y+j] == 0:
                    self.countarray[x+i,y+j] = 1
                    self.click(x+i, y+j)
                    
            

        elif self.board[x,y] == -1:
            self.gameboard[x,y] = self.board[x,y] 
            self.gamestate = False
            

        else:
            self.gameboard[x,y] = self.board[x,y]
            if verbose:
                print(self.gameboard[x,y])
                print(self.board[x,y])
            
                                
    def get_state_action(self):
        state = self.gameboard[1:self.boardsize+1, 1:self.boardsize+1].copy()
        actions = []
        for x in range(1, self.boardsize+1):
            for y in range(1, self.boardsize+1):
                if self.gameboard[x, y] == 100:
                    actions.append((x-1, y-1))  # Adjust coordinates to 0-based indexing
        return state, actions
    

def playgame():
    correct_response = True
    print("Hello there! Welcome to Minesweeper")
    boardsize = int(input("Please input the size of the board you would like to play on: "))
    mines = int(input("Please input the number of mines you like to play against: "))
    
    if mines >= (boardsize**2)-boardsize: correct_response = False
    else: correct_response = True

    while correct_response != True:
        mines = int(input(f"{mines} mines is too many, please pick a smaller number: "))
        if mines >= (boardsize**2)-boardsize: correct_response = False
        else: correct_response = True
        

    game = Minesweeper(boardsize,mines)
    game.populate()

    game.basicshow()

    

    while game.gamestate != False:
        go = True
        while go == True:
            P_input = str(input("Please choose wether to mark or click: ")).lower()
            if P_input == "mark": 
                coords_input = str(input("Please input the co-ordinates of your click separated by a space: "))
                coords = coords_input.split()
                x = int(coords[1])
                y = int(coords[0])
                

                game.mark(x,y)
                game.basicshow()
                go = False

            elif P_input == "click":
                coords_input = str(input("Please input the co-ordinates of your click separated by a space: "))
                coords = coords_input.split()
                x = int(coords[1])
                y = int(coords[0])
                

                game.click(x,y)
                game.basicshow()
                go = False
            
            else:
                print("That was not a valid input, try again: ")

    print("Game Over")

if __name__ == "__main__":
    playgame()