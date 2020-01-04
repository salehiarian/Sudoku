import math
import random
from sudo import solve_sudo

#Sudoku generator

class Sudoku:

    blank_elements = []

    def __init__(self, nor, k):
        self.k = k
        self.nor = nor
        self.srn = math.floor(math.sqrt(self.nor))
        # self.mat = [[0] * self.nor] * self.nor
        self.mat = [[0 for i in range(self.nor)] for j in range(self.nor)]
        for k in range(nor):
            for l in range(nor):
                self.mat[k][l] = 0
        self.blank_elements = [0 for i in range(self.k)]

    def fill_value(self):
        self.fill_diagonal()
        self.fill_rest()
        self.remove_k_elements()

    def fill_diagonal(self):
        for i in range(0, self.nor, self.srn):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        for k in range(self.srn):
            for j in range(self.srn):
                num = random.randint(1, self.nor)
                while not self.check(num, row, col):
                    num = random.randint(1, self.nor)

                self.mat[row + k][col + j] = num

    def check(self, num, row, col):
        for i in range(self.srn):
            for j in range(self.srn):
                if self.mat[row + i][col + j] == num:
                    return False

        return True

    def print_board(self):
        for i in range(len(self.mat)):
            if i % self.srn == 0 and i != 0:
                print("- - - - - - - - - - - - -")

            for j in range(len(self.mat[0])):
                if j % self.srn == 0 and j != 0:
                    print(" | ", end="")

                if j == self.nor - 1:
                    print(self.mat[i][j])
                else:
                    print(str(self.mat[i][j]) + " ", end="")

    def fill_rest(self):
        solve_sudo(self.mat)

    def remove_k_elements(self):

        for i in range(self.k):
            x = random.randint(0, self.nor-1)
            y = random.randint(0, self.nor-1)
            while self.mat[x][y] == 0:
                x = random.randint(0, self.nor-1)
                y = random.randint(0, self.nor-1)

            self.mat[x][y] = 0
            self.blank_elements[i] = (x, y)





