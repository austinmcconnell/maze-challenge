import factory

from app.maze import Cell


class CellFactory(factory.Factory):
    """
    Factory class to simplify the creation of Cells with
    specific properties for use in unit tests.
    """

    class Meta:
        model = Cell

    is_mine = False
    is_end = False
    is_start = False
    door_left = False
    door_down = False
    door_right = False
    door_up = False
