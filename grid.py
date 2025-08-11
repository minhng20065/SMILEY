import math
import heapq

class Grid:
    row = 0
    col = 0
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def generate_grid(self):
        grid = ""
        for _ in range(self.row):
            for _ in range(self.col):
                grid = grid + "- "
            grid = grid + '\n'
        return grid
    
    def adjust_size(self, row, col):
        self.row = row
        self.col = col
