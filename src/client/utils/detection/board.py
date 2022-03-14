import cv2
import numpy as np
from .smoothing import PointSmoother
from ...utils import debug


def _box_is_square(box):
    # Box is a list of coordinates forming a bounding box around the board
    # box[index][coord]
    # index = ordered from the lowest anticlockwise, where lowest is on the screen (not in coord frame)
    # coord = [x, y]
    # +1 to ensure non-zero division
    width = abs(int(box[0][0] - box[1][0])) + 1
    height = abs(int(box[2][1] - box[1][1])) + 1
    aspect_ratio = width / height

  #  average_dimension = (width + height) / 2

    # Assuming squareness is within 5%
    return 0.95 <= aspect_ratio <= 1.05#, average_dimension


def convert_box_to_rect(box):
    # Basic bounding box to rect from high low x y values
    first_element_in_list = 0
    last_element_in_list = len(box) - 1
    sorted_x = sorted(box, key=lambda c: c[0])
    low_x = sorted_x[first_element_in_list][0]
    high_x = sorted_x[last_element_in_list][0]
    sorted_y = sorted(box, key=lambda c: c[1])
    low_y = sorted_y[first_element_in_list][1]
    high_y = sorted_y[last_element_in_list][1]
    anchor = (low_x, low_y)
    size = (high_x - low_x, high_y - low_y)
    return anchor, size


class BoardBoundary:
    def __init__(self, color_threshold: 200):
        self.smoothing_buffer = PointSmoother(10)
        self.color_threshold = color_threshold
        self.boundary = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def get_boundary(self):
        return self.boundary

    def find_board(self, image):
        image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_threshold = cv2.threshold(image_greyscale, self.color_threshold, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(image_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        debug.debugger.update_image(image_threshold, 'threshold')
        # Filter out small boxes
        largest_bounds = {
            'length': 0,
            'box': []
        }
        for contour in contours[0]:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            #square, length = _box_is_square(box)
            square = _box_is_square(box)
            length = int(rect[1][0])
            debug.debugger.update_variables('box_length', length)

            if square and length > largest_bounds.get('length'):
                largest_bounds = {
                    'length': int(rect[1][0]),
                    'box': box
                }

            anchor, size = convert_box_to_rect(box)
            debug.debugger.add_temporary_annotation('threshold', anchor, size)

        self.smoothing_buffer.add_point(largest_bounds.get('box'))
        self.boundary = self.smoothing_buffer.get_average()
        return self.boundary
