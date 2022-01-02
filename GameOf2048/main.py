import random
import pygame
from pygame.locals import *
import numpy as np

colors = {
    'backgorund': (189, 172, 161),
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),

}


# n mai mare pcia sus jos
# m mai mare pica drpt stanga

class GameOf2048:
    a = 0

    def __init__(self, diff):
        self.n = 4
        self.m = 5
        self.matrix = np.zeros((self.n, self.m), dtype=int)
        self.spacing = 10
        self.difficulty = diff
        self.w = 500
        self.h = 500
        pygame.init()
        pygame.display.set_caption("2048")
        pygame.font.init()
        self.myFont = pygame.font.SysFont('Comic Sans MS', 30)

        self.screen = pygame.display.set_mode((self.w, self.h))

    def print_game(self):
        self.screen.fill(colors['backgorund'])

        for i in range(self.n):
            for j in range(self.m):
                num = self.matrix[i][j]
                if self.m >= self.n:
                    x_axis = j * self.w // self.m + self.spacing
                    y_axis = i * self.h // self.n + self.spacing
                    width = self.w // self.m - 2 * self.spacing
                    height = self.h // self.m - 2 * self.spacing
                elif self.n > self.m:
                    x_axis = j * self.w // self.m + self.spacing
                    y_axis = i * self.h // self.n + self.spacing
                    width = self.w // self.n - 2 * self.spacing
                    height = self.h // self.n - 2 * self.spacing

                pygame.draw.rect(self.screen, colors[num], pygame.Rect(x_axis, y_axis, height, width),
                                 border_radius=8)

                if num == 0:
                    continue
                text = self.myFont.render(f'{num}', True, (0, 0, 0))
                rect_text = text.get_rect(center=(x_axis + width / 2, y_axis + height / 2))
                self.screen.blit(text, rect_text)

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
        numbers = row_pos[row_pos != 0]  # numbers different from 0
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
        global row_pos
        ok = 0

        for i in range(self.n):
            if move in 'lr':
                row_pos = self.matrix[i, :]  # every number from the row
                ok = 1
            else :
                break
            switch = False
            if move in 'rd':
                switch = True
                row_pos = row_pos[::-1]  # we flip the list
            # why we flip ? It is easy: when we take the numbers in horizontal way
            numbers = self.get_numbers(row_pos)

            copy = np.zeros_like(row_pos)
            copy[:len(numbers)] = numbers

            if switch:
                copy = copy[::-1]

            if move in 'lr':
                self.matrix[i, :] = copy

        if ok == 0:
            for i in range(self.m):
                if move in 'du':
                    row_pos = self.matrix[:, i]  # every number from the col

                switch = False
                if move in 'rd':
                    switch = True
                    row_pos = row_pos[::-1]  # we flip the list
                # why we flip ? It is easy: when we take the numbers in horizontal way
                numbers = self.get_numbers(row_pos)

                copy = np.zeros_like(row_pos)
                copy[:len(numbers)] = numbers

                if switch:
                    copy = copy[::-1]
                if move in 'du':
                    self.matrix[:, i] = copy

    def isOver(self):
        copy_matrix = self.matrix.copy()
        for move in 'lrdu':
            self.new_move(move)
            if not all((self.matrix == copy_matrix).flatten()):
                self.matrix = copy_matrix
                return False
        return True

    @staticmethod
    def key():

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'q'
                if event.type == KEYDOWN:

                    if event.key == K_w:
                        print(1)
                        return 'u'

                    if event.key == K_s:
                        return 'd'

                    if event.key == K_a:
                        return 'l'

                    if event.key == K_d:
                        return 'r'

    def play(self):
        self.putANewNumber(k=2)
        while True:
            print(self.matrix)
            self.print_game()
            pygame.display.flip()
            cmd = self.key()
            if cmd == 'q':
                break
            past_matrix = self.matrix.copy()
            self.new_move(cmd)
            # if all((self.matrix == past_matrix).flatten()):
            # continue

            if self.isOver():
                print("Game over!")
                break
            self.putANewNumber()




if __name__ == '__main__':
    difficulty = str(input())
    start = GameOf2048(difficulty)
    start.play()
