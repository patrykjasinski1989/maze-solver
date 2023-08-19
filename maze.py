"""Maze generator and solver."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import sleep
from tkinter import Tk, BOTH, Canvas
from typing import List

DEFAULT_WIDTH = 5

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
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=self.color, width=self.width)

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

    def draw(self, canvas: Canvas) -> None:
        """Draw the cell on the given canvas."""
        if self.has_top_wall:
            canvas.create_line(self.x1, self.y1, self.x2, self.y1, fill=self.color, width=self.width)
        if self.has_left_wall:
            canvas.create_line(self.x1, self.y1, self.x1, self.y2, fill=self.color, width=self.width)
        if self.has_right_wall:
            canvas.create_line(self.x2, self.y1, self.x2, self.y2, fill=self.color, width=self.width)
        if self.has_bottom_wall:
            canvas.create_line(self.x1, self.y2, self.x2, self.y2, fill=self.color, width=self.width)

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
        """Toggle the walls of a specific cell and its neighbors."""
        cell = self.cells[row][col]

        # Toggle the walls of the current cell
        cell.has_left_wall = not cell.has_left_wall
        cell.has_top_wall = not cell.has_top_wall
        cell.has_right_wall = not cell.has_right_wall
        cell.has_bottom_wall = not cell.has_bottom_wall

        # Toggle the corresponding walls of neighboring cells
        if row > 0 and cell.has_top_wall == False:
            self.cells[row-1][col].has_bottom_wall = not self.cells[row-1][col].has_bottom_wall
        if row < self.num_rows - 1 and cell.has_bottom_wall == False:
            self.cells[row+1][col].has_top_wall = not self.cells[row+1][col].has_top_wall
        if col > 0 and cell.has_left_wall == False:
            self.cells[row][col-1].has_right_wall = not self.cells[row][col-1].has_right_wall
        if col < self.num_cols - 1 and cell.has_right_wall == False:
            self.cells[row][col+1].has_left_wall = not self.cells[row][col+1].has_left_wall

    def __str__(self) -> str:
        return super().__str__() + f"({self.x1}, {self.y1}) ({self.num_rows}, {self.num_cols})"

class Window:
    """A window with a canvas to draw on."""
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height)
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
        sleep(0.05)


if __name__ == "__main__":
    WIDTH : int = 800
    HEIGHT : int = 600
    CELL_SIZE: int = 50
    START_X: int = 2
    START_Y: int = 2

    win: Window = Window(WIDTH, HEIGHT)

    maze: Maze = Maze(START_X, START_Y, HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE, CELL_SIZE, CELL_SIZE)
    win.draw(maze)

    win.wait_for_close()
