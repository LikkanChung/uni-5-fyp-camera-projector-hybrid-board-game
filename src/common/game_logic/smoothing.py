"""
Python class which will smooth the coordinate inputs and will essentially produce a rolling average
"""


class PointSmoother:
    def __init__(self, point_type, buffer_length=10):
        self.point_type = point_type  # box or point
        self.buffer_length = buffer_length
        self.buffer = []

    def __repr__(self):
        return str(f'PointSmoother({self.point_type},{self.buffer_length})')

    def add_point(self, point):
        # point is an object with the structure of box
        self.buffer.append(point)
        if len(self.buffer) > self.buffer_length and len(self.buffer) > 0:
            self.buffer.pop(0)

    def _average_box(self):
        zipped_buffer = list(zip(*self.buffer))
        average_box = []
        for point_of_box in zipped_buffer:
            # for the 4 corners
            sum_x = 0
            sum_y = 0
            for p in point_of_box:
                sum_x += p[0]
                sum_y += p[1]
            average_point = [int(sum_x / len(point_of_box)), int(sum_y / len(point_of_box))]
            average_box.append(average_point)
        return average_box

    def _average_point(self):
        sum_x = 0
        sum_y = 0
        for point in self.buffer:
            x, y = point
            sum_x += x
            sum_y += y
        return int(sum_x / len(self.buffer)), int(sum_y / len(self.buffer))

    def get_average(self):
        if self.point_type == 'box':
            # Average of box [[x0,y0],[x1,y1],...]
            return self._average_box()
        elif self.point_type == 'point':
            # Average of points (x, y)
            return self._average_point()
        else:
            raise TypeError(f'Wrong type of Smoother: {self.point_type}. Should be point or box')
