"""Main script to generate and solve a maze using a GUI."""

from gui import Window
from maze import Maze

def main():
    """Main function to generate and display the maze."""
    MARGIN = 20
    START_X = MARGIN
    START_Y = MARGIN
    TOTAL_WIDTH = 1024
    TOTAL_HEIGHT = 768
    WIDTH = TOTAL_WIDTH - 2 * MARGIN
    HEIGHT = TOTAL_HEIGHT - 2 * MARGIN
    CELL_SIZE = 50
    NUM_ROWS = HEIGHT // CELL_SIZE
    NUM_COLS = WIDTH // CELL_SIZE

    win = Window(WIDTH, HEIGHT)
    maze = Maze(START_X, START_Y, NUM_ROWS, NUM_COLS, CELL_SIZE, CELL_SIZE, seed=None)

    maze.generate()

    win.draw_maze(maze)
    win.animate_solution(maze)
    win.wait_for_close()

if __name__ == "__main__":
    main()
