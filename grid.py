import math
import heapq
import random

class Grid:
    row = 0
    col = 0
    pl_pos_x = 0
    pl_pos_y = 0
    en_pos_x = 0
    en_pos_y = 0
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def generate_grid(self, player, enemy):
        grid = ""
        for i in range(self.row):
            for j in range(self.col):
                if (j == self.pl_pos_x and i == self.pl_pos_y):
                    grid = grid + player + " "
                elif (j == self.en_pos_x and i == self.en_pos_y):
                    grid = grid + enemy + " "
                else:
                    grid = grid + "- "
            grid = grid + '\n'
        return grid
    
    def adjust_size(self, row, col):
        self.row = row
        self.col = col
    
    def random_pos(self):
        self.pl_pos_x = random.randint(0, self.col-1)
        self.pl_pos_y = random.randint(0, self.row-1)
        self.en_pos_x = random.randint(0, self.col-1)
        self.en_pos_y = random.randint(0, self.row-1)
        while (self.en_pos_x == self.pl_pos_x):
            self.en_pos_x = random.randint(0, self.col-1)
        while (self.en_pos_y == self.pl_pos_y):
            self.en_pos_y = random.randint(0, self.row-1)
    
    def move(self, direction, value):
        diff = 0
        if direction == 'U':
            self.pl_pos_y -= value
            if (self.pl_pos_y < 0):
                diff = 0 - self.pl_pos_y
                self.pl_pos_y = 0
                print(diff)
            return diff
        elif direction == 'D':
            self.pl_pos_y += value
            if (self.pl_pos_y >= self.row):
                diff = self.pl_pos_y - self.row + 1
                self.pl_pos_y = self.row - 1
                print(diff)
            return diff
        elif direction == 'L':
            self.pl_pos_x -= value
            if (self.pl_pos_x < 0):
                diff = 0 - self.pl_pos_x
                self.pl_pos_x = 0
                print(diff)
            return diff
        elif direction == 'R':
            self.pl_pos_x += value
            if (self.pl_pos_x >= self.col):
                diff = self.pl_pos_x - self.col + 1
                self.pl_pos_x = self.col - 1
                print(diff)
            return diff
    def enemy_mov(self, mov):
        self.en_pos_x  = self.en_pos_x - mov
