import random

import numpy as np

n = 4
m = 4


class GameOf2048:
    a = 0

    def __init__(self, diff):
        self.matrix = np.zeros((n, m), dtype=int)
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

    @staticmethod
    def get_numbers(row_pos):
        numbers = row_pos[row_pos != 0]
        sum_of_numbers = []
        ok = False  # for skipping
        for j in range(len(numbers)):
            if ok:
                ok = False
                continue
            if j != len(numbers) - 1 and numbers[j] == numbers[j + 1]:  # if we can add 2 numbers that are neighbours
                # on the same row
                new_number = numbers[j] * 2
                ok = True
            else:
                new_number = numbers[j]

            sum_of_numbers.append(new_number)
        return np.array(sum_of_numbers)

    def new_move(self, move):
        for i in range(n):
            row_pos = self.matrix[i, :]  # every number from the row
            numbers = self.get_numbers(row_pos)

            copy = np.zeros_like(row_pos)
            copy[:len(numbers)] = numbers
            self.matrix[i, :] = copy  # moving everything to left


if __name__ == '__main__':
    difficulty = str(input())
    start = GameOf2048(difficulty)
    start.putANewNumber(k=2) # firstly we take 2 poistions becuase that  is how the game starts
    print(start)
    start.putANewNumber(k=2)
    print(start)
    start.new_move(move='l')
    print(start)
