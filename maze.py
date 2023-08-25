"""Maze generator and solver."""
from models import Drawable, Cell
from dataclasses import dataclass
from tkinter import Canvas
from typing import List, Tuple
import random

class MazeFactory:
    """Creates and initializes cells for the maze."""
    @staticmethod
    def create_cells(x1: int, y1: int, num_rows: int, num_cols: int, cell_size_x: int, cell_size_y: int) -> List[List[Cell]]:
        """Create the cells for the maze."""
        cells: List[List[Cell]] = []
        for row in range(num_rows):
            cells.append([])
            for col in range(num_cols):
                x_start: int = x1 + col * cell_size_x
                y_start: int = y1 + row * cell_size_y
                x_end: int = x_start + cell_size_x
                y_end: int = y_start + cell_size_y
                cells[row].append(Cell(x_start, y_start, x_end, y_end))
        return cells

@dataclass
class Maze(Drawable):
    """Represents a maze."""
    x1: int
    y1: int
    num_rows: int
    num_cols: int
    cell_size_x: int
    cell_size_y: int
    _cells: List[List[Cell]] = None
    seed: int = None

    @property
    def cells(self) -> List[List[Cell]]:
        """Lazy initialization of cells."""
        if self._cells is None:
            self._cells = MazeFactory.create_cells(self.x1, self.y1, self.num_rows, self.num_cols, self.cell_size_x, self.cell_size_y)
        return self._cells
    
    def __post_init__(self):
        if self.seed is not None:
            random.seed(self.seed)

    def draw(self, canvas: Canvas) -> None:
        """Draw the maze on the given canvas."""
        for row in self.cells:
            for cell in row:
                cell.draw(canvas)

    def _break_entrance_and_exit(self):
        entrance = self.cells[0][0]
        entrance.has_left_wall = False
        entrance.has_top_wall = False

        exit = self.cells[self.num_rows-1][self.num_cols-1]
        exit.has_right_wall = False
        exit.has_bottom_wall = False

    def _break_walls_r(self, cell: Cell, i: int, j: int):
        """The recursive break_walls_r method is a breadth-first traversal through the cells, breaking down walls as it goes."""
        cell.visited = True
        neighbors, indices = self._get_neighbors(i, j)

        # Shuffle the neighbors to introduce randomness
        combined = random.sample(list(zip(neighbors, indices)), len(neighbors))
        neighbors, indices = zip(*combined)

        for idx, neighbor in enumerate(neighbors):
            ni, nj = indices[idx]
            if not neighbor.visited:
                self._break_walls_between(cell, i, j, neighbor, ni, nj)
                self._break_walls_r(neighbor, ni, nj)

    def _get_neighbors(self, i: int, j: int):
        """Get the neighboring cells of the current cell."""
        neighbors = []
        indices = []
        if i > 0:
            neighbors.append(self.cells[i-1][j])
            indices.append((i-1, j))
        if j > 0:
            neighbors.append(self.cells[i][j-1])
            indices.append((i, j-1))
        if i < self.num_rows - 1:
            neighbors.append(self.cells[i+1][j])
            indices.append((i+1, j))
        if j < self.num_cols - 1:
            neighbors.append(self.cells[i][j+1])
            indices.append((i, j+1))
        return neighbors, indices

    def _break_walls_between(self, cell1 : Cell, i1 : int, j1 : int, cell2 : Cell, i2 : int, j2 : int):
        """Break the walls between two adjacent cells. Determine which walls to break based on their relative positions."""
        if i1 == i2:
            if j1 < j2:
                cell1.has_right_wall = False
                cell2.has_left_wall = False
            else:
                cell1.has_left_wall = False
                cell2.has_right_wall = False
        elif j1 == j2:
            if i1 < i2:
                cell1.has_bottom_wall = False
                cell2.has_top_wall = False
            else:
                cell1.has_top_wall = False
                cell2.has_bottom_wall = False
        else:
            raise Exception(f"Cells at ({i1}, {j1}) and ({i2}, {j2}) are not adjacent")

    def _reset_cells_visited(self):
        """Reset the visited flag of all cells."""
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def generate(self):
        """Generate the maze."""
        self._break_entrance_and_exit()
        self._break_walls_r(self.cells[0][0], 0, 0)
        self._reset_cells_visited()

    def solve(self) -> List[Tuple[Cell, Cell]]:
        """Compute a solution to the maze and return a list of steps."""
        steps = []
        self._solve_r(self.cells[0][0], 0, 0, steps)
        return steps

    def _solve_r(self, cell : Cell, i : int, j : int, steps: List[Tuple[Cell, Cell, bool]]):
        """A depth-first solution to the maze.
        The _solve_r method returns True if the current cell is an end cell, OR if it leads to the end cell.
        It returns False if the current cell is a loser cell."""
        cell.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        neighbors, indices = self._get_neighbors(i, j)

        combined = random.sample(list(zip(neighbors, indices)), len(neighbors))
        neighbors, indices = zip(*combined)

        for idx, neighbor in enumerate(neighbors):
            ni, nj = indices[idx]
            if not neighbor.visited:
                if (i == ni and j < nj and not cell.has_right_wall) or \
                (i == ni and j > nj and not cell.has_left_wall) or \
                (j == nj and i < ni and not cell.has_bottom_wall) or \
                (j == nj and i > ni and not cell.has_top_wall):

                    steps.append((cell, neighbor, False))  # False indicates it's not an undo step

                    if self._solve_r(neighbor, ni, nj, steps):
                        return True

                    steps.append((cell, neighbor, True))  # True indicates it's an undo step

        return False
