from ....common.game_objects.tokens.token import Token
from src.client.utils.image_transform import crop_to
import cv2
import os
import numpy
from src.client.utils.config import config
from src.client.utils.debug import debugger

CASCADE_PATH = os.path.join('src', 'client', 'utils', 'detection', 'model', 'token_cascade.xml')


def centre_coordinate(anchor, size):
    (x, y) = anchor
    (w, h) = size
    return x + (w / 2), y + (h / 2)


def detect_color(piece_image):
    if piece_image is not None:
        # Filter background
        threshold = config.get_property(['client', 'color', 'token_background_threshold'])
        black_pixel = numpy.array([0, 0, 0])
        threshold_filter = numpy.array([threshold, threshold, threshold])
        mask = cv2.inRange(piece_image, black_pixel, threshold_filter)
        threshold_image = cv2.bitwise_and(piece_image, piece_image, mask=mask)

        # Calculate average color and filter out black pixels
        r, g, b, count = 0, 0, 0, 0
        for row in threshold_image:
            for pixel in row:
                if not numpy.array_equal(pixel, black_pixel):
                    b += pixel[0]
                    g += pixel[1]
                    r += pixel[2]
                    count += 1
        if count > 0:
            return int(b / count), int(g / count), int(r / count)  # bgr color
        else:
            return None
    return None

def classify_color(bgr_color):
    colors = config.get_property(['client', 'color', 'classes'])
    proximity = dict()
    for color in colors:
        color_class_bgr = colors.get(color)
        color_class_vector = numpy.array([color_class_bgr.get('b'), color_class_bgr.get('g'), color_class_bgr.get('r')])
        distance = numpy.linalg.norm(numpy.array(bgr_color) - color_class_vector)
        proximity[distance] = color
    nearst_color = proximity.get(sorted(proximity.keys())[0])
    return nearst_color


class TokenDetection:
    def __init__(self, board_dimensions):
        self.board_dimensions = board_dimensions
        self.detected_pieces = []
        self.cascade = cv2.CascadeClassifier(CASCADE_PATH)

    def find_pieces(self, board_image, board_anchor):
        if board_image is not None:
            identified_pieces_rects = self.cascade.detectMultiScale(board_image)
            offset_x, offset_y = board_anchor
            for rectangle in identified_pieces_rects:
                (x, y) = (rectangle[0], rectangle[1])
                (dx, dy) = (rectangle[2], rectangle[3])
                piece_image = crop_to(board_image, (x, y), (x + dx, y + dy))
                color_bgr = detect_color(piece_image)
                if color_bgr:
                    color_class = classify_color(color_bgr)
                    classified_token = False

                    token_anchor_coordinate = (x + offset_x, y + offset_y)
                    token_coordinate = centre_coordinate(token_anchor_coordinate, (dx, dy))

                    for token in self.detected_pieces:
                        if token.get_color() == color_class:
                            token.update_coordinate(token_coordinate)
                            debugger.update_annotation(color_class, token_anchor_coordinate, (dx, dy))
                            classified_token = True
                            # TODO work to include if it is nearby, instead of just the color
                    if not classified_token:
                        # new Token
                        token = Token(color_class, token_coordinate)
                        debugger.update_annotation(color_class, token_anchor_coordinate, (dx, dy))
                        self.detected_pieces.append(token)
                else:
                    # No color detected, or image all black
                    pass
            return self.detected_pieces
        return None

