import pytest

from app.maze import Maze, extract_cell_characteristics
from tests.factories import CellFactory


@pytest.fixture
def example_maze():
    """
    This is the example maze from the instructions.
    """
    num_rows, num_columns, cell_values = 3, 3, [34, 14, 12, 6, 77, 5, 1, 19, 9]
    return num_rows, num_columns, cell_values


class TestExtractCellCharacteristics:
    """
    Suite of tests to ensure the cell conversion / characteristic
    extraction works as expected.
    """

    def test_all_doors(self):
        expected_cell = CellFactory(door_up=True, door_down=True, door_left=True, door_right=True)
        actual_cell = extract_cell_characteristics(value=15)
        assert expected_cell == actual_cell

    def test_mine_door_up_cell(self):
        expected_cell = CellFactory(is_mine=True, door_up=True)
        actual_cell = extract_cell_characteristics(value=65)
        assert expected_cell == actual_cell

    def test_start_left_up_door(self):
        expected_cell = CellFactory(is_start=True, door_left=True, door_up=True)
        actual_cell = extract_cell_characteristics(value=25)
        assert expected_cell == actual_cell

    def test_end_right_door(self):
        expected_cell = CellFactory(is_end=True, door_right=True)
        actual_cell = extract_cell_characteristics(value=34)
        assert expected_cell == actual_cell

    def test_example_cell_from_instructions(self):
        expected_cell = CellFactory(is_mine=True, door_left=True, door_down=True, door_up=True)
        actual_cell = extract_cell_characteristics(value=77)
        assert expected_cell == actual_cell


class TestMaze:
    """
    These tests ensure the example maze from the instructions
    is solved correctly. Especially the case where only 1
    life remaining yields a different solution path.
    """

    def test_example_maze_from_instructions(self, example_maze):
        maze = Maze(num_rows=example_maze[0],
                    num_columns=example_maze[1],
                    cell_values=example_maze[2])
        maze.solve()

        assert maze.best_path == ['up', 'up', 'left']

    def test_example_maze_from_instructions_one_life(self, example_maze):
        maze = Maze(num_rows=example_maze[0],
                    num_columns=example_maze[1],
                    cell_values=example_maze[2],
                    lives=1)
        maze.solve()

        assert maze.best_path == ['right', 'up', 'up', 'left', 'left']
