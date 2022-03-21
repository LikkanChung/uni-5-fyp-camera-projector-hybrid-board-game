from ...game_logic.smoothing import PointSmoother
from src.client.utils.debug import debugger


class Token:
    def __init__(self, color, coordinate):
        self.color = color
        self.point_smoother = PointSmoother('point')
        self.point_smoother.add_point(coordinate)
        self.coordinate = self.point_smoother.get_average()

    def __str__(self):
        return f'{self.get_color()}:{self.get_coordinate()}'

    def __repr__(self):
        return self.__str__()

    def get_color(self):
        return self.color

    def get_coordinate(self):
        return self.coordinate

    def update_coordinate(self, coordinate):
        self.point_smoother.add_point(coordinate)
        self.coordinate = self.point_smoother.get_average()

        x, y = self.coordinate
        debug_box = (x - 5, y - 5)
        debugger.update_annotation(f'{self.color}_coord', debug_box, (10, 10))
