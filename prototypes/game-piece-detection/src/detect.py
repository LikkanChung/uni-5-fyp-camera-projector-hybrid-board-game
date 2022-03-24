import random

import cv2
import numpy as np
from .utils import crop_and_zoom

WHITE_THRESHOLD = 230


def setup_capture():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap


def setup_cascade():
    cascade_red = cv2.CascadeClassifier('training/combined_experiment_7/cascade.xml')
    return cascade_red


def find_board(image):
    image_greyscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_threshold = cv2.threshold(image_greyscale, WHITE_THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(image_threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_box_bounds = {
        'length': 0,
        'box': []
    }
    for contour in contours[0]:
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Check is square
        w = abs(int(box[0][0] - box[1][0])) + 1
        h = abs(int(box[2][1] - box[1][1])) + 1
        aspect_ratio = w / h
        if 0.95 <= aspect_ratio <= 1.05:
            if w > largest_box_bounds.get('length'):
                largest_box_bounds = {
                    'length': int(rect[1][0]),
                    'box': box
                }

    return largest_box_bounds


def transform_to_bounds(image, box):
    """Transforms the image to a cropped level box from a rotated bounding box """
    source_points = box.get('box').astype("float32")
    length = box.get('length')
    dest_points = np.array([
        [0, length - 1],
        [0, 0],
        [length - 1, 0],
        [length - 1, length - 1]
    ], dtype='float32')
    transform_matrix = cv2.getPerspectiveTransform(source_points, dest_points)
    transformed_image = cv2.warpPerspective(image, transform_matrix, (length, length))
    return transformed_image


def transform_to_bounds_basic(image, box):
    """Transforms to basic bounding box from the highest and lowest x and y values"""
    height, width, _ = image.shape
    sorted_x = sorted(box.get('box'), key=lambda c: c[0])
    low_x = max(0, sorted_x[0][0])
    high_x = min(width, sorted_x[3][0])
    sorted_y = sorted(box.get('box'), key=lambda c: c[1])
    low_y = max(0, sorted_y[0][1])
    high_y = min(height, sorted_y[3][1])
    cropped_image = image[low_y:high_y, low_x:high_x]
    anchor_point_closest_to_origin = (low_x, low_y)
    return cropped_image, anchor_point_closest_to_origin


def draw_rectangles(image, rectangles, point_offset, color=(255, 0, 0)):
    offset_x, offset_y = point_offset
    for rectangle in rectangles:
        (x1, y1) = (rectangle[0] + offset_x, rectangle[1] + offset_y)
        (x2, y2) = (rectangle[0] + rectangle[2] + offset_x, rectangle[1] + rectangle[3] + offset_y)
        cv2.rectangle(image, (x1, y1), (x2, y2), color, 2)
    return image


def detect_pieces():
    cap = setup_capture()
    cascade = setup_cascade()

    while True:
        _, image = cap.read()

        zoomed_image = crop_and_zoom(image, 2.5, 2.5)

        board = find_board(zoomed_image)
        board_image, board_anchor_offset = transform_to_bounds_basic(zoomed_image, board)

        # Show bounds of detection
        bound_height, bound_width, _ = board_image.shape
        bounds = [0, 0, bound_width, bound_height]
        marked_simple_bounds_image = draw_rectangles(zoomed_image, [bounds], board_anchor_offset, (0, 255, 0))

        identified_pieces = cascade.detectMultiScale(board_image)
        marked_pieces_image = draw_rectangles(marked_simple_bounds_image, identified_pieces, board_anchor_offset)

        cv2.imshow("img", marked_pieces_image)

        if cv2.waitKey(1) == 27:
            # ESC to quit
            break

    cv2.destroyAllWindows()
