import pygame
import random
from sudo import solve_sudo, is_safe, find_empty
import time
from tkinter import *

import tkinter as tk
from tkinter import messagebox
from sudo_generator import Sudoku
import os

pygame.font.init()
pygame.init()

# Game song: Yanni - In the Morning Light
music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)
clickSound = pygame.mixer.Sound('click.wav')
correctSound = pygame.mixer.Sound('correct.wav')
# win = pygame.display.set_mode((540, 600))
win = pygame.display.set_mode((540, 600))


class Grid:

    def __init__(self, rows, cols, width, height, win):
        global k, s
        k = random.randint(25, 40)
        s = Sudoku(9, k)
        s.fill_value()
        self.board = s.mat
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.update_model()
        self.width = width
        self.height = height

        self.selected = None
        self.win = win

    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()

            if is_safe(self.model, val, (row, col)) and solve_sudo(self.model):
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def select(self, row, col):
        # Reset all other

        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        clickSound.play()
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    # reset
    def reset(self):
        self.__init__(self.rows, self.cols, self.width, self.height, win)
        # pygame.display.update()

    # solver
    def solve(self):
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
        for i in range(1, 10):
            if is_safe(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, True)
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve():

                    return True
                else:
                    self.model[row][col] = 0
                    self.cubes[row][col].set(0)
                    self.update_model()
                    self.cubes[row][col].draw_change(self.win, False)
                    pygame.display.update()
                    pygame.time.delay(100)

        return False


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("Calibri", 30)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, check):
        fnt = pygame.font.SysFont("Calibri ", 30)
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if check:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def redraw_window(win, board, time, strikes):
    win.fill((255, 255, 255))

    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)

    text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (380, 560))

    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    try:
        root.destroy()
    except:
        pass


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(minute) + ":" + str(sec)
    return mat


def main():
    pygame.display.set_caption("Sudoku: by Arian")
    win = pygame.display.set_mode((540, 600))
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    while run:

        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Correct")
                            correctSound.play()
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
                # Key space for solving the gui
                elif event.key == pygame.K_SPACE:
                    board.solve()

                    if board.is_finished():
                        Tk().wm_withdraw()
                        result = messagebox.askokcancel('Game Finished', ('Would you like to play again?'))
                        if result:
                            start = time.time()
                            board.reset()
                        else:
                            pygame.quit()
                            sys.exit()

                # Key r for reseting the game
                elif event.key == pygame.K_r:
                    start = time.time()
                    board.reset()

                if board.is_finished():
                    print("Game over")
                    pygame.time.delay(50)
                    m = 'Congrats! Would you like to play again?'

                    Tk().wm_withdraw()
                    result = messagebox.askokcancel('Program Finished', m)
                    if result:
                        start = time.time()
                        board.reset()
                    else:
                        pygame.quit()
                        sys.exit()

                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
