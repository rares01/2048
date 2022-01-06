import random
import pygame
from pygame.locals import *
import numpy as np
from tkinter import messagebox
from tkinter import *
import sys

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


class GameOf2048:
    a = 0
    difficulty = ""

    def __init__(self):
        self.n = 4
        self.m = 4
        self.matrix = np.zeros((self.n, self.m), dtype=int)
        self.spacing = 10
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
            else:
                break
            switch = False
            if move in 'rd':
                switch = True
                row_pos = row_pos[::-1]  # we flip the list
            # why we flip ? It is easy: when we need the numbers in the opposite way
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
                # why we flip ? It is easy: when we need the numbers in the opposite way
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
                        return 'u'

                    if event.key == K_s:
                        return 'd'

                    if event.key == K_a:
                        return 'l'

                    if event.key == K_d:
                        return 'r'

    def play(self):

        check = self.meniu()
        if check == 'q':
            sys.exit()
        else:
            self.difficulty = check

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

            if self.isOver():
                self.inializeBox()

            if not all((self.matrix == past_matrix).flatten()):
                self.putANewNumber()

    def inializeBox(self):
        window = Tk()
        window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
        window.withdraw()
        if messagebox.askyesno('Question', 'You LOST! Do you want to restart the game?') == True:
            self.matrix = np.zeros((self.n, self.m), dtype=int)
            self.a = 0
            self.putANewNumber(k=1)

        else:
            sys.exit()

        window.deiconify()
        window.destroy()
        window.quit()

    def meniu(self):

        # white color
        global mouse
        color = (255, 255, 255)
        # light shade of the button
        color_light = (170, 170, 170)

        # dark shade of the button
        color_dark = (100, 100, 100)

        width = self.screen.get_width()

        height = self.screen.get_height()

        textForEasy = self.myFont.render('Easy', True, color)
        textForMedium = self.myFont.render('Medium', True, color)
        textForHard = self.myFont.render('Hard', True, color)

        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(190, 90, 140, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''

        font_nou = pygame.font.Font(None, 24)
        text_to_show = font_nou.render("Insert the numbers like this : number,number then press enter", True, color)

        textRect = text_to_show.get_rect()

        # set the center of the rectangular object.
        textRect.center = (width // 2 , height // 2 - 190)
        while True:

            for ev in pygame.event.get():

                if ev.type == pygame.QUIT:
                    return 'q'

                if ev.type == pygame.MOUSEBUTTONDOWN:

                    if input_box.collidepoint(ev.pos):
                        # Toggle the active variable.
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                    # Easy button
                    if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 - 80 <= mouse[1] <= height / 2 - 40:
                        return "Easy"

                    # Medium button
                    if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 <= mouse[1] <= height / 2 + 40:
                        return "Medium"

                    if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 + 80 <= mouse[1] <= height / 2 + 120:
                        return "Hard"

                if ev.type == pygame.KEYDOWN:
                    if active:
                        if ev.key == pygame.K_RETURN:

                            self.n = int(text[0])
                            self.m = int(text[2])
                            self.matrix = np.zeros((self.n, self.m), dtype=int)
                            text = ''

                        elif ev.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += ev.unicode

            self.screen.fill((60, 25, 60))
            self.screen.blit(text_to_show, textRect)
            txt_surface = font.render(text, True, color)
            # Resize the box if the text is too long.
            input_box.w = max(100, txt_surface.get_width() + 10)
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(self.screen, color, input_box, 2)

            mouse = pygame.mouse.get_pos()

            # changing the lighting to every button depends if it is hovered or not

            # Easy button
            if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 - 80 <= mouse[1] <= height / 2 - 40:
                pygame.draw.rect(self.screen, color_light, [width / 2 - 80, height / 2 - 80, 140, 40])

            else:
                pygame.draw.rect(self.screen, color_dark, [width / 2 - 80, height / 2 - 80, 140, 40])

            # Medium button
            if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 <= mouse[1] <= height / 2 + 40:
                pygame.draw.rect(self.screen, color_light, [width / 2 - 80, height / 2, 140, 40])

            else:
                pygame.draw.rect(self.screen, color_dark, [width / 2 - 80, height / 2, 140, 40])

            # Hard button
            if width / 2 - 80 <= mouse[0] <= width / 2 + 60 and height / 2 + 80 <= mouse[1] <= height / 2 + 120:
                pygame.draw.rect(self.screen, color_light, [width / 2 - 80, height / 2 + 80, 140, 40])

            else:
                pygame.draw.rect(self.screen, color_dark, [width / 2 - 80, height / 2 + 80, 140, 40])

            # text in buttons
            self.screen.blit(textForEasy, (width / 2 - 50, height / 2 - 80))
            self.screen.blit(textForMedium, (width / 2 - 65, height / 2))
            self.screen.blit(textForHard, (width / 2 - 50, height / 2 + 80))
            pygame.display.flip()


if __name__ == '__main__':
    start = GameOf2048()
    start.play()
