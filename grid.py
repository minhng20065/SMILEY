import math
import heapq
import random

class Grid:
    row = 0
    col = 0
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def generate_grid(self, player, enemy):
        grid = ""
        pl_pos_x = random.randint(0, self.col-1)
        pl_pos_y = random.randint(0, self.row-1)
        en_pos_x = random.randint(0, self.col-1)
        en_pos_y = random.randint(0, self.row-1)
        while (en_pos_x == pl_pos_x):
            en_pos_x = random.randint(0, self.col-1)
        while (en_pos_y == pl_pos_y):
            en_pos_y = random.randint(0, self.row-1)
        for i in range(self.row):
            for j in range(self.col):
                if (j == pl_pos_x and i == pl_pos_y):
                    grid = grid + player + " "
                elif (j == en_pos_x and i == en_pos_y):
                    grid = grid + enemy + " "
                else:
                    grid = grid + "- "
            grid = grid + '\n'
        return grid
    
    def adjust_size(self, row, col):
        self.row = row
        self.col = col
