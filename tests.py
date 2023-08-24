import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m1.cells
        self.assertEqual(len(cells), num_rows)
        self.assertEqual(len(cells[0]), num_cols)

    def test_maze_create_cells_small(self):
        num_cols = 2
        num_rows = 2
        m2 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m2.cells
        self.assertEqual(len(cells), num_rows)
        self.assertEqual(len(cells[0]), num_cols)

    def test_maze_create_cells_large(self):
        num_cols = 50
        num_rows = 40
        m3 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m3.cells
        self.assertEqual(len(cells), num_rows)
        self.assertEqual(len(cells[0]), num_cols)

    def test_maze_create_cells_single_row(self):
        num_cols = 10
        num_rows = 1
        m4 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m4.cells
        self.assertEqual(len(cells), num_rows)
        self.assertEqual(len(cells[0]), num_cols)

    def test_maze_create_cells_single_col(self):
        num_cols = 1
        num_rows = 10
        m5 = Maze(0, 0, num_rows, num_cols, 10, 10)
        cells = m5.cells
        self.assertEqual(len(cells), num_rows)
        self.assertEqual(len(cells[0]), num_cols)

    def test_break_entrance_and_exit(self):
        """Test the _break_entrance_and_exit method."""
        self.maze = Maze(0, 0, 5, 5, 10, 10)
        self.maze._break_entrance_and_exit()

        # Check entrance
        entrance = self.maze.cells[0][0]
        self.assertFalse(entrance.has_left_wall)
        self.assertFalse(entrance.has_top_wall)

        # Check exit
        exit = self.maze.cells[self.maze.num_rows-1][self.maze.num_cols-1]
        self.assertFalse(exit.has_right_wall)
        self.assertFalse(exit.has_bottom_wall)

    def test_reset_cells_visited(self):
        """Test the _reset_cells_visited method."""
        self.maze = Maze(0, 0, 5, 5, 10, 10)

        # Mark some cells as visited
        self.maze.cells[0][0].visited = True
        self.maze.cells[1][1].visited = True
        self.maze.cells[2][2].visited = True

        self.maze._reset_cells_visited()

        # Check that all cells are no longer marked as visited
        for row in self.maze.cells:
            for cell in row:
                self.assertFalse(cell.visited)


if __name__ == "__main__":
    unittest.main()
