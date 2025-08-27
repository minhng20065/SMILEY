'''This module sets up the battle grid for players.'''
import heapq
import random

class Grid:
    '''This class holds all the functionality for setting up a battle grid, including the 
    player and enemy positions, the grid size, a way to generate the grid, a way to move
    players around the grid, and the A* tracking algorithm for enemies.'''
    row = 7
    col = 10
    pl_pos_x = 0
    pl_pos_y = 0
    en_pos_x = 0
    en_pos_y = 0
    parent_i = 0
    parent_j = 0
    f = float('inf')
    g = float('inf')
    h = 0
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def is_valid(self, row, col):
        '''This method checks if the position of either the player or the enemy
        is valid.'''
        return 0 <= col < self.row and 0 <= row < self.col
    def is_destination(self, x, y):
        '''This method checks if the enemy position has reached the 
        player position.'''
        return x == self.pl_pos_x and y == self.pl_pos_y

    def calc_heur(self, x, y):
        '''This method calculates the hueristic distance between the enemy and the
        player, allowing calculation of the most optimal route.'''
        return ((x - self.pl_pos_y) ** 2 + (y - self.pl_pos_x) ** 2) ** 0.5

    def trace_path(self, cell_details):
        '''This method prints out a traced path from the enemy's current position
        to the player position.'''
        print("The Path is ")
        path = []
        row = self.en_pos_y
        col = self.en_pos_x

        # Trace the path from destination to source using parent cells
        while not (cell_details[row][col].parent_i == row and
                   cell_details[row][col].parent_j == col):
            path.append((row, col))
            temp_row = cell_details[row][col].parent_i
            temp_col = cell_details[row][col].parent_j
            row = temp_row
            col = temp_col

        # Add the source cell to the path
        path.append((row, col))
        # Reverse the path to get the path from source to destination
        path.reverse()

        # Print the path
        for i in path:
            print("->", i, end=" ")
        print()

    def a_star(self, mov):
        '''This method implements the A* tracking algorithm, allowing the 
        enemy to find the player using the most optimal set of moves.'''
        if (not self.is_valid(self.en_pos_x, self.en_pos_y)
            or not self.is_valid(self.pl_pos_x, self.pl_pos_y)):
            print("Source or destination is invalid")
            return False
        if self.is_destination(self.en_pos_x, self.en_pos_y):
            print("already there!")
            return False
        closed_list = [[False for _ in range(self.col)] for _ in range(self.row)]
        cell_details = [[Grid() for _ in range(self.col)] for _ in range(self.row)]
        i = self.en_pos_y
        j = self.en_pos_x
        cell_details[i][j].f = 0
        cell_details[i][j].g = 0
        cell_details[i][j].h = 0
        cell_details[i][j].parent_i = i
        cell_details[i][j].parent_j = j
        open_list = []
        heapq.heappush(open_list, (0.0, i, j))
        found_dest = False

        while (len(open_list) > 0 and mov > 0):
            p = heapq.heappop(open_list)
            i = p[1]
            j = p[2]
            closed_list[i][j] = True
            for new_dir in self.directions:
                new_i = i + new_dir[0]
                new_j = j + new_dir[1]
                if self.is_valid(new_j, new_i) and not closed_list[new_i][new_j]:
                    self.en_pos_y = new_i
                    self.en_pos_x = new_j
                    if self.is_destination(new_j, new_i):
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
                        self.en_pos_y = i
                        self.en_pos_x = j
                        self.trace_path(cell_details)
                        found_dest = True
                        print("destination found!")
                        return True
                    g_new = cell_details[i][j].g + 1.0
                    h_new = self.calc_heur(new_i, new_j)
                    f_new = g_new + h_new
                    if (cell_details[new_i][new_j].f == float('inf')
                        or cell_details[new_i][new_j].f > f_new):
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j
            mov = mov - 1
        self.trace_path(cell_details)
        if not found_dest:
            print("failed to find the destination cell")
            return False
        return False

    def ranger(self):
        '''This method checks whether or not players are in range for an attack.'''
        for new_dir in self.directions:
            new_x = self.pl_pos_x + new_dir[0]
            new_y = self.pl_pos_y + new_dir[1]
            if (new_x == self.en_pos_x and new_y == self.en_pos_y):
                return True
        return False

    def generate_grid(self, player, enemy):
        '''This method generates a grid, creating a grid of size row x column and placing
        the enemies and players on their positions.'''
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
        '''This method allows players to adjust the size of the grid as needed.'''
        self.row = row
        self.col = col

    def random_pos(self):
        '''This method is executed to randomize the position of the players and enemies
        at the start of the battle.'''
        self.pl_pos_x = random.randint(0, self.col-1)
        self.pl_pos_y = random.randint(0, self.row-1)
        self.en_pos_x = random.randint(0, self.col-1)
        self.en_pos_y = random.randint(0, self.row-1)
        while self.en_pos_x == self.pl_pos_x:
            self.en_pos_x = random.randint(0, self.col-1)
        while self.en_pos_y == self.pl_pos_y:
            self.en_pos_y = random.randint(0, self.row-1)

    def move(self, direction, value):
        '''This method moves players based on user commands, taking in a cardinal
        direction and the amount of tiles to move.'''
        diff = 0
        if direction == 'U':
            self.pl_pos_y -= value
            if self.pl_pos_y < 0:
                diff = 0 - self.pl_pos_y
                self.pl_pos_y = 0
                print(diff)
            return diff
        if direction == 'D':
            self.pl_pos_y += value
            if self.pl_pos_y >= self.row:
                diff = self.pl_pos_y - self.row + 1
                self.pl_pos_y = self.row - 1
                print(diff)
            return diff
        if direction == 'L':
            self.pl_pos_x -= value
            if self.pl_pos_x < 0:
                diff = 0 - self.pl_pos_x
                self.pl_pos_x = 0
                print(diff)
            return diff
        if direction == 'R':
            self.pl_pos_x += value
            if self.pl_pos_x >= self.col:
                diff = self.pl_pos_x - self.col + 1
                self.pl_pos_x = self.col - 1
                print(diff)
            return diff
        return None
