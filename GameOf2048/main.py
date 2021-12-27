import random

import numpy as np

n = 4
m = 4


class GameOf2048:
    a = 0

    def __init__(self, diff):
        self.matrix = np.zeros((n, m))
        self.difficulty = diff

    def putANewNumber(self, k=1):
        positions = list(zip(*np.where(self.matrix == 0)))  # positions from matrix where we have 0
        for posi in random.sample(positions, k=k):  # from positions we take k random positions for starting the matrix
            self.a += 1  # used for only one time to put a big number
            if self.difficulty == "Easy" and self.a == 1:  # difficulty
                self.matrix[posi] = 128

            elif self.difficulty == "Medium" and self.a == 1:  # difficulty
                self.matrix[posi] = 512

            elif self.difficulty == "Hard" and self.a == 1:  # difficulty
                self.matrix[posi] = 1024
            else:
                if random.random() < .1:  # the chance of getting a 4 is less then 10% percent
                    self.matrix[posi] = 4
                else:
                    self.matrix[posi] = 2

    def __str__(self):
        return str(self.matrix)

    # def new_move(self,move):


if __name__ == '__main__':
    difficulty = str(input())
    start = GameOf2048(difficulty)
    start.putANewNumber(k=2) # firstly we take 2 poistions becuase that  is how the game starts
    print(start)
