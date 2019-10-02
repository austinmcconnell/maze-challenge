import logging
import os
import sys
from typing import List, Tuple

from app.maze import Maze

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

logging.basicConfig(level=LOG_LEVEL, format='%(message)s')


def read_file(filepath: str) -> List[Tuple[int, int, List[int]]]:
    def process_maze_string(maze_string: str) -> Tuple[int, int, List[int]]:
        size: List[int] = [int(x) for x in maze_string.split('-')[0].strip('()').split(',')]
        num_rows: int = size[0]
        num_cols: int = size[1]

        cells: List[int] = [int(x) for x in maze_string.split('-')[1].strip('[]\n').split(',')]

        return num_rows, num_cols, cells

    logging.debug(f'Reading input file at {filepath}')
    mazes = list()
    with open(filepath, mode='r') as file:
        for maze_string in file:
            mazes.append(process_maze_string(maze_string=maze_string))
    return mazes


def maze_solver(filepath: str) -> None:
    mazes = read_file(filepath=filepath)
    for index, item in enumerate(mazes, start=1):
        num_rows, num_columns, cell_values = item
        logging.debug('*' * 50)
        logging.debug(f'Processing maze: {index}')
        logging.debug('*' * 50)

        maze = Maze(num_rows=num_rows, num_columns=num_columns, cell_values=cell_values)
        maze.solve()

        logging.debug(f'Start position: {maze.start_position}')
        logging.debug(f'End position: {maze.end_position}')
        logging.debug(f'Mines located at: {maze.mines}')

        print(maze.best_path)


if __name__ == '__main__':
    maze_solver(filepath=sys.argv[1])
