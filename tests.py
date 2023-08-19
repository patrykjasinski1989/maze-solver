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


if __name__ == "__main__":
    unittest.main()