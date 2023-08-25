from abc import ABC, abstractmethod
from dataclasses import dataclass
from tkinter import Canvas
from typing import List

DEFAULT_WIDTH = 5

class Drawable(ABC):
    """Abstract base class for drawable objects."""
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

    def __post_init__(self):
        if self.x1 >= self.x2:
            raise ValueError(f"x1 ({self.x1}) should be less than x2 ({self.x2})")
        if self.y1 >= self.y2:
            raise ValueError(f"y1 ({self.y1}) should be less than y2 ({self.y2})")

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
