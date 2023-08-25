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

    def solve(self, algorithm : str = "dfs") -> List[Tuple[Cell, Cell]]:
        """Compute a solution to the maze and return a list of steps."""
        steps = []
        if algorithm == "dfs":
            self._solve_r(self.cells[0][0], 0, 0, steps)
        elif algorithm == "a_star":
            start = self.cells[0][0]
            end = self.cells[self.num_rows - 1][self.num_cols - 1]
            steps = self.a_star_search(start, end)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")
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

    def manhattan_distance(self, cell1, cell2):
        return abs(cell1.x1 - cell2.x1) + abs(cell1.y1 - cell2.y1)

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()

        # Convert the list of cells to the expected format
        solution_steps = []
        for i in range(len(path) - 1):
            solution_steps.append((path[i], path[i + 1], False))
        return solution_steps

    def get_cell_position(self, cell: Cell) -> Tuple[int, int]:
        """Return the row and column indices of a given cell."""
        for i, row in enumerate(self.cells):
            for j, current_cell in enumerate(row):
                if current_cell == cell:
                    return i, j
        raise ValueError("Cell not found in the maze.")

    def _get_valid_neighbors(self, i: int, j: int, current_cell: Cell):
        """Get the neighboring cells of the current cell that can be reached without crossing a wall."""
        neighbors = []
        indices = []
        if i > 0 and not current_cell.has_top_wall:
            neighbors.append(self.cells[i-1][j])
            indices.append((i-1, j))
        if j > 0 and not current_cell.has_left_wall:
            neighbors.append(self.cells[i][j-1])
            indices.append((i, j-1))
        if i < self.num_rows - 1 and not current_cell.has_bottom_wall:
            neighbors.append(self.cells[i+1][j])
            indices.append((i+1, j))
        if j < self.num_cols - 1 and not current_cell.has_right_wall:
            neighbors.append(self.cells[i][j+1])
            indices.append((i, j+1))
        return neighbors, indices

    def a_star_search(self, start, end):
        open_set = [start]
        closed_set = []
        came_from = {}

        g = {cell: float('inf') for row in self.cells for cell in row}
        g[start] = 0

        f = {cell: float('inf') for row in self.cells for cell in row}
        f[start] = self.manhattan_distance(start, end)

        while open_set:
            current = min(open_set, key=lambda x: f[x])
            if current == end:
                return self.reconstruct_path(came_from, current)

            open_set.remove(current)
            closed_set.append(current)

            i, j = self.get_cell_position(current)
            neighbors, _ = self._get_valid_neighbors(i, j, current)  # Unpack neighbors and their indices
            for neighbor in neighbors:  # Use only the Cell objects for the A* logic
                if neighbor in closed_set:
                    continue
                tentative_g_score = g[current] + 1

                if neighbor not in open_set:
                    open_set.append(neighbor)
                elif tentative_g_score >= g[neighbor]:
                    continue

                came_from[neighbor] = current
                g[neighbor] = tentative_g_score
                f[neighbor] = g[neighbor] + self.manhattan_distance(neighbor, end)

        return []
