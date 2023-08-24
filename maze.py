"""Maze generator and solver."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from random import shuffle
from time import sleep
from tkinter import Tk, BOTH, Canvas
from typing import List

DEFAULT_WIDTH = 5
BACKGROUND_COLOR = "white"

class Drawable(ABC):
    @abstractmethod
    def draw(self, canvas: Canvas) -> None:
        """Draw the object on the given canvas."""
        pass

@dataclass
class Point:
    """Represents a 2D point with x and y coordinates."""
    x: int
    y: int

@dataclass
class Line(Drawable):
    """Represents a line segment defined by two points, a color, and a width."""
    p1: Point
    p2: Point
    color: str
    width: int = DEFAULT_WIDTH

    def draw(self, canvas: Canvas) -> None:
        """Draw the line on the given canvas."""
        line_options = {
            "fill": self.color,
            "width": self.width,
            "joinstyle": "round",  # Round the junctions between connected segments
            "capstyle": "round"   # Round the endpoints of the lines
        }
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, **line_options)

@dataclass
class Cell(Drawable):
    """Represents a cell in a maze."""
    x1: int
    y1: int
    x2: int
    y2: int
    has_left_wall: bool = True
    has_top_wall: bool = True
    has_right_wall: bool = True
    has_bottom_wall: bool = True
    color: str = "black"
    width: int = DEFAULT_WIDTH
    visited: bool = False

    def draw(self, canvas: Canvas) -> None:
        """Draw the cell on the given canvas."""
        line_options = {
            "fill": self.color,
            "width": self.width,
            "joinstyle": "round",  # Round the junctions between connected segments
            "capstyle": "round"   # Round the endpoints of the lines
        }
        if self.has_top_wall:
            canvas.create_line(self.x1, self.y1, self.x2, self.y1, **line_options)
        if self.has_left_wall:
            canvas.create_line(self.x1, self.y1, self.x1, self.y2, **line_options)
        if self.has_right_wall:
            canvas.create_line(self.x2, self.y1, self.x2, self.y2, **line_options)
        if self.has_bottom_wall:
            canvas.create_line(self.x1, self.y2, self.x2, self.y2, **line_options)


class MazeFactory:
    """Factory to create maze cells."""
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

    def draw(self, canvas: Canvas) -> None:
        """Draw the maze on the given canvas."""
        for row in self.cells:
            for cell in row:
                cell.draw(canvas)

    def toggle_cell_walls(self, row: int, col: int):
        """Toggle the walls of a specific cell."""
        cell = self.cells[row][col]
        # Toggle the walls of the current cell
        cell.has_left_wall = not cell.has_left_wall
        cell.has_top_wall = not cell.has_top_wall
        cell.has_right_wall = not cell.has_right_wall
        cell.has_bottom_wall = not cell.has_bottom_wall

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
        combined = list(zip(neighbors, indices))
        shuffle(combined)
        neighbors, indices = zip(*combined)

        for idx, neighbor in enumerate(neighbors):
            ni, nj = indices[idx]
            if not neighbor.visited:
                self._break_walls_between(cell, i, j, neighbor, ni, nj)
                self._break_walls_r(neighbor, ni, nj)

    def _get_neighbors(self, i: int, j: int):
        """Get the neighbors of the current cell."""
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

    def _break_walls_between(self, cell1, i1, j1, cell2, i2, j2):
        """Break the walls between two cells."""
        if i1 == i2:  # Cells are in the same row
            if j1 < j2:  # cell1 is to the left of cell2
                cell1.has_right_wall = False
                cell2.has_left_wall = False
            else:  # cell1 is to the right of cell2
                cell1.has_left_wall = False
                cell2.has_right_wall = False
        elif j1 == j2:  # Cells are in the same column
            if i1 < i2:  # cell1 is above cell2
                cell1.has_bottom_wall = False
                cell2.has_top_wall = False
            else:  # cell1 is below cell2
                cell1.has_top_wall = False
                cell2.has_bottom_wall = False
        else:
            raise Exception("Cells are not adjacent")

    def _reset_cells_visited(self):
        """Reset the visited flag of all cells."""
        for row in self.cells:
            for cell in row:
                cell.visited = False

    def solve(self, window : 'Window' = None):
        return self._solve_r(self.cells[0][0], i=0, j=0, window=window)

    def _solve_r(self, cell, i, j, window : 'Window' = None):
        """A depth-first solution to the maze.
        The _solve_r method returns True if the current cell is an end cell, OR if it leads to the end cell.
        It returns False if the current cell is a loser cell."""
        cell.visited = True

        if i == self.num_rows - 1 and j == self.num_cols - 1:
            return True

        neighbors, indices = self._get_neighbors(i, j)

        combined = list(zip(neighbors, indices))
        shuffle(combined)
        neighbors, indices = zip(*combined)

        for idx, neighbor in enumerate(neighbors):
            ni, nj = indices[idx]
            if not neighbor.visited:
                if (i == ni and j < nj and not cell.has_right_wall) or \
                (i == ni and j > nj and not cell.has_left_wall) or \
                (j == nj and i < ni and not cell.has_bottom_wall) or \
                (j == nj and i > ni and not cell.has_top_wall):

                    window.draw_move(cell, neighbor)

                    if self._solve_r(neighbor, ni, nj, window):
                        return True

                    window.draw_move(cell, neighbor, undo=True)

        return False

class Window:
    """A window with a canvas to draw on."""
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.configure(background=BACKGROUND_COLOR)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def _redraw(self) -> None:
        """Update the window."""
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        """Keep the window open until closed by the user."""
        self.__running = True
        while self.__running:
            self._redraw()

    def close(self) -> None:
        """Close the window."""
        self.__running = False
        self.__root.destroy()

    def draw(self, drawable: Drawable) -> None:
        """Draw the given drawable object on the canvas."""
        drawable.draw(self.__canvas)
        self._animate()

    def draw_move(self, from_cell: Cell, to_cell: Cell, undo : bool = False):
        """Draw a move from one cell to another."""
        color: str = "gray" if undo else "red"
        from_x: int = (from_cell.x1 + from_cell.x2) // 2
        from_y: int = (from_cell.y1 + from_cell.y2) // 2
        to_x: int = (to_cell.x1 + to_cell.x2) // 2
        to_y: int = (to_cell.y1 + to_cell.y2) // 2
        line: Line = Line(Point(from_x, from_y), Point(to_x, to_y), color)
        self.draw(line)

    def _animate(self):
        """Animate the window."""
        self._redraw()
        sleep(0.01)


if __name__ == "__main__":
    MARGIN : int = 20
    START_X : int = MARGIN
    START_Y : int = MARGIN
    WIDTH : int = 1024 - 2 * MARGIN
    HEIGHT : int = 768 - 2 * MARGIN
    CELL_SIZE: int = 50
    NUM_ROWS : int = HEIGHT // CELL_SIZE
    NUM_COLS : int = WIDTH // CELL_SIZE

    win: Window = Window(WIDTH, HEIGHT)
    maze: Maze = Maze(START_X, START_Y, NUM_ROWS, NUM_COLS, CELL_SIZE, CELL_SIZE, seed=0)

    maze._break_entrance_and_exit()
    maze._break_walls_r(maze.cells[0][0], 0, 0)
    maze._reset_cells_visited()

    win.draw(maze)
    maze.solve(win)

    win.wait_for_close()
