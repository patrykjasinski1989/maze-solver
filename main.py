"""Maze generator and solver."""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas

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


if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2

    win = Window(WIDTH, HEIGHT)

    lines = [
        Line(Point(0, 0), Point(WIDTH, HEIGHT), "red"),
        Line(Point(0, HEIGHT), Point(WIDTH, 0), "black"),
        Line(Point(0, HALF_HEIGHT), Point(WIDTH, HALF_HEIGHT), "green"),
        Line(Point(HALF_WIDTH, 0), Point(HALF_WIDTH, HEIGHT), "blue")
    ]

    for line in lines:
        win.draw(line)

    cell = Cell(HALF_WIDTH / 2, HALF_HEIGHT / 2, HALF_WIDTH * 3 / 2, HALF_HEIGHT * 3 / 2)
    win.draw(cell)

    win.wait_for_close()
