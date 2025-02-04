# ==============================CS-199==================================
# FILE:			MyAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the MyAI class. You will implement your
#				agent in this file. You will write the 'getAction' function,
#				the constructor, and any additional helper functions.
#
# NOTES: 		- MyAI inherits from the abstract AI class in AI.py.
#
#				- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
from collections import deque
from typing import List, Tuple, Set


class MyAI(AI):
    # Constants
    COVERED = '_'
    UNKNOWN = ' '
    MINE = -1

    def __init__(self, rowDimension: int, colDimension: int, totalMines: int, startX: int, startY: int):
        self.rowDimension = rowDimension
        self.colDimension = colDimension
        self.totalMines = totalMines
        self.remainMines = totalMines
        self.current_x = startX  # X represents the column
        self.current_y = startY  # Y represents the row
        
        """
        self.board where each cell contains:
        The state of the tile (self.board[y][x][0])
        The effective label or number on the tile (self.board[y][x][1])
        The number of adjacent covered tiles (self.board[y][x][2])
        """
        # Initialize the board: [state, effective_label, adjacent_covered_count]
        self.board = [[[self.COVERED, self.UNKNOWN, 8] for _ in range(colDimension)] for _ in range(rowDimension)]
        
        self.to_be_uncovered = deque()
        self.uncovered_count = 0
        self.adjacent_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def getAction(self, number: int) -> "Action Object":
        # Update the state of the current tile with the given number
        self.board[self.current_y][self.current_x][0] = number
        # Update list of covered tiles around the current position
        covered = self.adj_covered_state(self.current_x, self.current_y)

        # If the current tile is 0, label all adjacent tiles as safe
        if number == 0:
            self.mark_safe()
        # If the current tile is greater than 0, check and update labels
        elif number > 0:
            self.check_label(self.current_x, self.current_y, covered)

        self.process_board() #update tile states and process board
        self.apply_subset_neighbor_algorithm()

        # If no tiles are marked for uncovering
        if not self.to_be_uncovered:
            self.mine_probability()

        # Check if the game is complete
        if self.uncovered_count == self.colDimension * self.rowDimension - self.totalMines:
            return Action(AI.Action.LEAVE)
        # If there are tiles to uncover, choose the next one
        elif self.to_be_uncovered:
            self.current_x, self.current_y = self.to_be_uncovered.popleft()
            self.uncovered_count += 1
            return Action(AI.Action.UNCOVER, self.current_x, self.current_y)
        # If no more moves can be made safely, leave the game
        else:
            return Action(AI.Action.LEAVE)


    def process_board(self):
        # Iterate through the entire board to update tile states
        for row in range(self.rowDimension):
            for col in range(self.colDimension):
                if (self.board[row][col][0] != self.COVERED and 
                    self.board[row][col][0] > 0 and 
                    self.board[row][col][2] > 0 and 
                    (self.current_x != col or self.current_y != row)):
                    covers = self.adj_covered_state(col, row)
                    if covers:
                        self.check_label(col, row, covers)

    def mark_safe(self):
        # Mark all adjacent tiles as safe when the current tile is 0
        for dx, dy in self.adjacent_offsets:
            adjX, adjY = self.current_x + dx, self.current_y + dy
            if self.is_valid_coord(adjX, adjY) and self.board[adjY][adjX][0] == self.COVERED:
                self.board[adjY][adjX][0] = 0
                self.to_be_uncovered.append((adjX, adjY))
        self.board[self.current_y][self.current_x][1] = 0 # Effective label = 0, no adjacent mines
        self.board[self.current_y][self.current_x][2] = 0 # Remaining uncovered = 0, 

    def check_label(self, x: int, y: int, covered: List[Tuple[int, int]]):
        # Check and update labels based on the effective label and covered tiles
        effective_label = self.board[y][x][1]
        if effective_label == 0:  # All the remaining tiles are safe, label the remaining adjacent as safe
            for tile_x, tile_y in covered:
                self.board[tile_y][tile_x][0] = 0
                self.to_be_uncovered.append((tile_x, tile_y))
            self.board[y][x][1] = self.board[y][x][2] = 0
        elif effective_label == len(covered):
            for tile_x, tile_y in covered:
                self.board[tile_y][tile_x][0] = self.MINE
                self.update_adj_state(tile_x, tile_y)
            self.board[y][x][1] = self.board[y][x][2] = 0

    def adj_covered_state(self, x: int, y: int) -> List[Tuple[int, int]]:
        # Update the state of adjacent tiles and return covered tiles
        cover_tiles = []
        count_mines = 0
        for dx, dy in self.adjacent_offsets:
            adjX, adjY = x + dx, y + dy
            if self.is_valid_coord(adjX, adjY):
                if self.board[adjY][adjX][0] == self.MINE:
                    count_mines += 1
                elif self.board[adjY][adjX][0] == self.COVERED:
                    cover_tiles.append((adjX, adjY))
        self.board[y][x][1] = self.board[y][x][0] - count_mines
        self.board[y][x][2] = len(cover_tiles)
        return cover_tiles

    def update_adj_state(self, x: int, y: int):
        # Update the state of tiles adjacent to a newly identified mine
        for dx, dy in self.adjacent_offsets:
            adjX, adjY = x + dx, y + dy
            if (self.is_valid_coord(adjX, adjY) and 
                self.board[adjY][adjX][1] != self.UNKNOWN and 
                self.board[adjY][adjX][1] > 0):
                self.adj_covered_state(adjX, adjY)

    def mine_probability(self):
        # Calculate mine probabilities for covered tiles when no safe moves are available
        covered = [(col, row) for row in range(self.rowDimension) 
                   for col in range(self.colDimension) 
                   if self.board[row][col][0] == self.COVERED]
        if covered:
            mine_prob = {tile: sum(1 for dx, dy in self.adjacent_offsets
                                   if self.is_valid_coord(tile[0]+dx, tile[1]+dy) and
                                   self.board[tile[1]+dy][tile[0]+dx][1] != self.UNKNOWN and
                                   self.board[tile[1]+dy][tile[0]+dx][1] > 0)
                         for tile in covered}
            min_prob_tile = min(mine_prob, key=mine_prob.get)
            self.to_be_uncovered.append(min_prob_tile)
    
    def is_valid_coord(self, x: int, y: int) -> bool:
        # Check if the given coordinates are within the board boundaries
        return 0 <= x < self.colDimension and 0 <= y < self.rowDimension

    def apply_subset_neighbor_algorithm(self):
        # Apply advanced subset-based neighbor analysis to the entire board
        for y in range(self.rowDimension):
            for x in range(self.colDimension):
                if isinstance(self.board[y][x][0], int) and self.board[y][x][0] >= 0:
                    self.check_subset_neighbors(x, y)

    def check_subset_neighbors(self, x: int, y: int):
        # Check for subset relationships between neighboring tiles
        tile_a_neighbors = self.get_covered_neighbors(x, y)
        tile_a_effective_value = self.board[y][x][1]

        if not isinstance(tile_a_effective_value, int):
            return  # Skip if the effective value is not an integer

        for dx, dy in self.adjacent_offsets:
            neighbor_x, neighbor_y = x + dx, y + dy
            if self.is_valid_coord(neighbor_x, neighbor_y):
                tile_b_value = self.board[neighbor_y][neighbor_x][0]
                if isinstance(tile_b_value, int) and tile_b_value >= 0:
                    tile_b_neighbors = self.get_covered_neighbors(neighbor_x, neighbor_y)
                    tile_b_effective_value = self.board[neighbor_y][neighbor_x][1]

                    if not isinstance(tile_b_effective_value, int):
                        continue  # Skip if the effective value is not an integer

                    if set(tile_b_neighbors).issubset(set(tile_a_neighbors)):
                        exclusive_neighbors = set(tile_a_neighbors) - set(tile_b_neighbors)
                        value_difference = tile_a_effective_value - tile_b_effective_value
                        neighbor_difference = len(tile_a_neighbors) - len(tile_b_neighbors)

                        if value_difference == 0:
                             # All exclusive neighbors are safe
                            for ex, ey in exclusive_neighbors:
                                if self.board[ey][ex][0] == self.COVERED:
                                    self.board[ey][ex][0] = 0
                                    self.to_be_uncovered.append((ex, ey))
                        elif value_difference == neighbor_difference:
                            # All exclusive neighbors are mines
                            for ex, ey in exclusive_neighbors:
                                if self.board[ey][ex][0] == self.COVERED:
                                    self.board[ey][ex][0] = self.MINE
                                    self.update_adj_state(ex, ey)

    def get_covered_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
         # Get a list of covered neighboring tiles
        return [(x + dx, y + dy) for dx, dy in self.adjacent_offsets
                if self.is_valid_coord(x + dx, y + dy) and self.board[y + dy][x + dx][0] == self.COVERED]