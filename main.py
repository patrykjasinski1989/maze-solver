from dataclasses import dataclass
from tkinter import Tk, BOTH, Canvas


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Line:
    p1: Point
    p2: Point

    def draw(self, canvas: Canvas, fill_color: str, width: int) -> None:
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=width)
        canvas.pack(fill=BOTH, expand=1)


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__canvas = Canvas(self.__root, width=width, height=height)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
    
    def close(self) -> None:
        self.__running = False
        self.__root.destroy()

    def draw_line(self, line: Line, fill_color: str, width: int = 2) -> None:
        line.draw(self.__canvas, fill_color, width)


if __name__ == "__main__":
    WIDTH = 800
    HEIGHT = 600
    HALF_WIDTH = WIDTH // 2
    HALF_HEIGHT = HEIGHT // 2

    win = Window(WIDTH, HEIGHT)

    lines_data = [
        (Point(0, 0), Point(WIDTH, HEIGHT), "red"),
        (Point(0, HEIGHT), Point(WIDTH, 0), "black"),
        (Point(0, HALF_HEIGHT), Point(WIDTH, HALF_HEIGHT), "green"),
        (Point(HALF_WIDTH, 0), Point(HALF_WIDTH, HEIGHT), "blue")
    ]

    for p1, p2, color in lines_data:
        win.draw_line(Line(p1, p2), color)

    win.wait_for_close()
