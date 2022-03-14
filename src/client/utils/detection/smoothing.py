"""
Python class which will smooth the coordinate inputs and will essentially produce a rolling average
"""


class PointSmoother:
    def __init__(self, buffer_length):
        self.buffer_length = buffer_length
        self.buffer = []

    def add_point(self, point):
        self.buffer.append(point)
        if len(self.buffer) > self.buffer_length and len(self.buffer) > 0:
            self.buffer.pop(0)

    def _average(self):
        zipped_buffer = list(zip(*self.buffer))
        average_box = []
        for point_of_box in zipped_buffer:
            # for the 4 corners
            sum_x = 0
            sum_y = 0
            for p in point_of_box:
                sum_x += p[0]
                sum_y += p[1]
            average_point = [sum_x / len(point_of_box), sum_y / len(point_of_box)]
            average_box.append(average_point)
        return average_box

    def get_average(self):
        # Average of box [[x0,y0],[x1,y1],...]
        return self._average()

