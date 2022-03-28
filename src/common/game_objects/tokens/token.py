from ...game_logic.smoothing import PointSmoother
from src.client.utils.debug import debugger
from src.client.utils.config import config


class Token:
    def __init__(self, color, coordinate):
        self.color = color
        self.point_smoother = PointSmoother(
            'point',
            config.get_property(['client', 'detection_smoothing_buffer', 'token'])
        )
        self.point_smoother.add_point(coordinate)
        self.coordinate = self.point_smoother.get_average()
        self.last_update_counter = 0

    def __str__(self):
        return f'{self.get_color()}:{self.get_coordinate()}:{self.last_update_counter}'

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        return self.color

    def get_coordinate(self):
        return self.coordinate

    def update_coordinate(self, coordinate):
        x, y = coordinate
        self.point_smoother.add_point((int(x), int(y)))
        self.coordinate = self.point_smoother.get_average()

        self.reset_update_counter()

    def update_counter(self):
        self.last_update_counter += 1

    def reset_update_counter(self):
        self.last_update_counter = 0

    def get_last_update(self):
        return self.last_update_counter

