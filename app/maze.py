from collections import deque, namedtuple
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List

Position = namedtuple('Position', 'row column')

MINE_VALUE = 64
END_VALUE = 32
START_VALUE = 16
LEFT_VALUE = 8
DOWN_VALUE = 4
RIGHT_VALUE = 2
UP_VALUE = 1


def extract_cell_characteristics(value: int) -> 'Cell':
    is_mine = bool(value & MINE_VALUE)
    is_end = bool(value & END_VALUE)
    is_start = bool(value & START_VALUE)
    door_left = bool(value & LEFT_VALUE)
    door_down = bool(value & DOWN_VALUE)
    door_right = bool(value & RIGHT_VALUE)
    door_up = bool(value & UP_VALUE)

    cell = Cell(is_mine=is_mine,
                is_end=is_end,
                is_start=is_start,
                door_left=door_left,
                door_down=door_down,
                door_right=door_right,
                door_up=door_up)

    return cell


@dataclass
class Cell:
    """
    The Cell class is intended to contain all the characteristics
    or attributes of a cell in a way that is easy to access.
    """
    is_mine: bool
    is_end: bool
    is_start: bool
    door_left: bool
    door_down: bool
    door_right: bool
    door_up: bool


@dataclass
class Maze:
    """
    The Maze class hold all the information about the maze, a collection of Cells
    in a grid pattern, and the methods to solve the maze.
    """
    num_rows: int
    num_columns: int
    cell_values: List
    lives: int = field(default=3)

    def __post_init__(self):
        self.mines = list()
        self.grid: List[List[Cell]] = self.convert_grid()
        self.directions: Dict[int, Dict] = {0: {'lives': self.lives,
                                                'path': [],
                                                'visited': []}}
        self.best_path: List = list()
        self.current_index = 0

    def convert_grid(self):
        """
        This method takes the list of cell values and converts them
        to a grid of Cells. It also stores meta information, such as
        the start_position, end_position, and location of mines.
        """
        grid = []
        for i in range(0, len(self.cell_values), self.num_columns):
            grid.append(self.cell_values[i:i + self.num_columns])

        for row in range(self.num_rows):
            for col in range(self.num_columns):
                value = grid[row][col]
                cell = extract_cell_characteristics(value=value)
                if cell.is_start:
                    self.start_position = Position(row, col)
                if cell.is_end:
                    self.end_position = Position(row, col)
                if cell.is_mine:
                    self.mines.append((row, col))
                grid[row][col] = cell
        return grid

    @staticmethod
    def get_pos(cur_pos):
        right_pos = Position(cur_pos.row, cur_pos.column + 1)
        left_pos = Position(cur_pos.row, cur_pos.column - 1)
        up_pos = Position(cur_pos.row - 1, cur_pos.column)
        down_pos = Position(cur_pos.row + 1, cur_pos.column)
        return down_pos, left_pos, right_pos, up_pos

    def solve(self):
        """
        This method starts from the end and works back to the beginning
        because it was initially setup as a backtracking method
        to find the best path back to start after each cell was
        assigned a score or cost.

        Alas, after implementing the solver and incorporating the check
        for lives remaining, the solution I came up with no longer used
        the score. C'est la vie.
        """
        def check_neighboring_cell(position, direction, index, branch):
            if position not in self.directions[index]['visited']:
                if branch:
                    old_index = index
                    self.current_index += 1
                    index = self.current_index
                    self.directions[index] = deepcopy(self.directions[old_index])
                    self.directions[index]['path'].pop()

                queue.append((position, index))
                self.directions[index]['path'].append(direction)

        index = self.current_index
        queue = deque([(self.end_position, index)])

        while queue:
            cur_pos, index = queue.popleft()
            current_cell = self.grid[cur_pos.row][cur_pos.column]
            self.directions[index]['visited'].append(cur_pos)

            if current_cell.is_start:
                break

            if current_cell.is_mine:
                self.directions[index]['lives'] -= 1

            if self.directions[index]['lives'] == 0:
                del self.directions[index]
                continue

            down_pos, left_pos, right_pos, up_pos = self.get_pos(cur_pos)
            need_to_branch = False

            if current_cell.door_right:
                queue_length = len(queue)
                check_neighboring_cell(position=right_pos,
                                       direction='right',
                                       index=index,
                                       branch=need_to_branch)
                if len(queue) == queue_length + 1:
                    need_to_branch = True

            if current_cell.door_left:
                queue_length = len(queue)
                check_neighboring_cell(position=left_pos,
                                       direction='left',
                                       index=index,
                                       branch=need_to_branch)
                if len(queue) == queue_length + 1:
                    need_to_branch = True

            if current_cell.door_up:
                queue_length = len(queue)
                check_neighboring_cell(position=up_pos,
                                       direction='up',
                                       index=index,
                                       branch=need_to_branch)
                if len(queue) == queue_length + 1:
                    need_to_branch = True

            if current_cell.door_down:
                check_neighboring_cell(position=down_pos,
                                       direction='down',
                                       index=index,
                                       branch=need_to_branch)

        indexes_to_delete = []
        if len(self.directions) > 1:
            for index, item in self.directions.items():
                if item['visited'][-1] != self.start_position:
                    indexes_to_delete.append(index)

        for index in indexes_to_delete:
            del self.directions[index]

        index, winning_path = self.directions.popitem()
        winning_path['path'].reverse()
        switch_directions_map = {'up': 'down',
                                 'down': 'up',
                                 'left': 'right',
                                 'right': 'left'}
        reversed_path = list(map(lambda x: switch_directions_map[x], winning_path['path']))
        self.best_path = reversed_path
