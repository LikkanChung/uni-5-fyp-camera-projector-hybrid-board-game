import cv2
import numpy as np
from src.common.game_logic.smoothing import PointSmoother
from ...utils import debug
from ...utils.config import config


def _box_is_square(box):
    # Box is a list of coordinates forming a bounding box around the board
    # box[index][coord]
    # index = ordered from the lowest anticlockwise, where lowest is on the screen (not in coord frame)
    # coord = [x, y]
    # +1 to ensure non-zero division
    p0 = np.array(box[0])
    p1 = np.array(box[1])
    p2 = np.array(box[2])

    p01_length = np.linalg.norm(p0 - p1) + 1
    p12_length = np.linalg.norm(p1 - p2) + 1

    aspect_ratio = p01_length / p12_length
    average_dimension = (p01_length + p12_length) / 2

    # Assuming squareness is within 5%
    return 0.95 <= aspect_ratio <= 1.05, average_dimension


def convert_box_to_rect(box):
    # Basic bounding box to rect from high low x y values
    first_element_in_list = 0
    last_element_in_list = len(box) - 1
    sorted_x = sorted(box, key=lambda c: c[0])
    low_x = int(sorted_x[first_element_in_list][0])
    high_x = int(sorted_x[last_element_in_list][0])
    sorted_y = sorted(box, key=lambda c: c[1])
    low_y = int(sorted_y[first_element_in_list][1])
    high_y = int(sorted_y[last_element_in_list][1])
    anchor = (low_x, low_y)
    size = (high_x - low_x, high_y - low_y)
    return anchor, size


class BoardBoundary:
    def __init__(self, color_threshold: 200):
        self.smoothing_buffer = PointSmoother(
            'box',
            config.get_property(['client', 'detection_smoothing_buffer', 'board'])
        )
        self.color_threshold = color_threshold
        self.boundary = [[0, 0], [0, 0], [0, 0], [0, 0]]

    def get_boundary(self):
        # Box
        return self.boundary

    def find_board(self, image):
        """
        Finds the board in the image
        :param image:
        :return: A box of the board
        """
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

            square, length = _box_is_square(box)
            debug.debugger.update_variables('box_length', length)

            if square and length > largest_bounds.get('length'):
                largest_bounds = {
                    'length': length,
                    'box': box
                }
                anchor, size = convert_box_to_rect(box)
                debug.debugger.add_temporary_annotation('threshold', anchor, size)

        if largest_bounds.get('length') > 0:
            self.smoothing_buffer.add_point(largest_bounds.get('box'))
            self.boundary = self.smoothing_buffer.get_average()
        return self.boundary
