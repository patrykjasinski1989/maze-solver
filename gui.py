from tkinter import Tk, BOTH, Canvas
from time import sleep
from maze import Maze
from models import Drawable, Cell, Point, Line

BACKGROUND_COLOR = "white"
ANIMATION_DELAY = 0.01

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
        """
        Draw a move from one cell to another.
        
        If undo is True, the move is drawn in gray indicating an undone move.
        If undo is False, the move is drawn in red indicating a new move.
        """
        color: str = "gray" if undo else "red"
        from_x: int = (from_cell.x1 + from_cell.x2) // 2
        from_y: int = (from_cell.y1 + from_cell.y2) // 2
        to_x: int = (to_cell.x1 + to_cell.x2) // 2
        to_y: int = (to_cell.y1 + to_cell.y2) // 2
        line: Line = Line(Point(from_x, from_y), Point(to_x, to_y), color)
        self.draw(line)

    def draw_maze(self, maze: Maze):
        """Draw the given maze."""
        maze.draw(self.__canvas)

    def animate_solution(self, maze: Maze, algorithm: str):
        """Animate the solution of the given maze."""
        solution_steps = maze.solve(algorithm=algorithm)
        for from_cell, to_cell, is_undo in solution_steps:
            self.draw_move(from_cell, to_cell, is_undo)

    def _animate(self):
        """Animate the window."""
        self._redraw()
        sleep(ANIMATION_DELAY)
