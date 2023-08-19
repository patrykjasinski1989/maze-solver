"""Maze generator and solver."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas
from typing import List

DEFAULT_WIDTH = 2

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

    def draw_move(self, from_cell: Cell, to_cell: Cell, undo : bool = False):
        color: str = "gray" if undo else "red"
        from_x: int = (from_cell.x1 + from_cell.x2) // 2
        from_y: int = (from_cell.y1 + from_cell.y2) // 2
        to_x: int = (to_cell.x1 + to_cell.x2) // 2
        to_y: int = (to_cell.y1 + to_cell.y2) // 2
        line: Line = Line(Point(from_x, from_y), Point(to_x, to_y), color)
        self.draw(line)


if __name__ == "__main__":
    WIDTH : int = 800
    HEIGHT : int = 600
    HALF_WIDTH : int = WIDTH // 2
    HALF_HEIGHT : int = HEIGHT // 2

    win: Window = Window(WIDTH, HEIGHT)

    lines: List[Line] = [
        Line(Point(0, 0), Point(WIDTH, HEIGHT), "red"),
        Line(Point(0, HEIGHT), Point(WIDTH, 0), "black"),
        Line(Point(0, HALF_HEIGHT), Point(WIDTH, HALF_HEIGHT), "green"),
        Line(Point(HALF_WIDTH, 0), Point(HALF_WIDTH, HEIGHT), "blue")
    ]

    for line in lines:
        win.draw(line)

    cells: List[Cell] = [
        Cell(50, 50, 150, 150),
        Cell(200, 50, 300, 150, has_right_wall=False),
        Cell(350, 50, 450, 150, has_bottom_wall=False),
        Cell(500, 50, 600, 150, has_left_wall=False, has_top_wall=False),
        Cell(650, 50, 750, 150, has_right_wall=False, has_bottom_wall=False)
    ]

    for cell in cells:
        win.draw(cell)

    win.draw_move(cells[2], cells[3])

    win.wait_for_close()
