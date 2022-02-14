# This file is a script that will help create the dataset required to train the haar cascades.
import copy

import cv2
import os
from .image_processor import ImageProcessor

IMAGE_PIXELS = 50
DATA_PATH = os.path.join(os.getcwd(), 'data')


def setup_capture():
    cv2.namedWindow('collect', cv2.WINDOW_GUI_NORMAL)
    cv2.resizeWindow('collect', 1080, 720)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap


def draw_grid(image):
    """
    Helper. Draws grid the same size as the output image.
    Can be used as a reference for the user to know how the image is framed.
    :return: Image with grid
    """
    height, width, _ = image.shape  # h w channels
    for i in range(1, int(height/IMAGE_PIXELS) + 1):
        # Horizontal lines, (start_x, start,y), (end_x, end_y), Blue
        cv2.line(image, (0, i * IMAGE_PIXELS), (width, i * IMAGE_PIXELS), (255, 0, 0), 1, 1)
    for j in range(1, int(width/IMAGE_PIXELS) + 1):
        # Vertical lines
        cv2.line(image, (j * IMAGE_PIXELS, 0), (j * IMAGE_PIXELS, height), (255, 0, 0), 1, 1)
    return image


def main():
    cap = setup_capture()
    image_processor = ImageProcessor(IMAGE_PIXELS, DATA_PATH, "test")
    while True:
        _, image = cap.read()
        original_image = image
        grid_image = copy.deepcopy(image)
        cv2.imshow("collect", draw_grid(grid_image))

        image_processor.set_image(original_image)
        cv2.setMouseCallback('collect', image_processor.click_event)

        if cv2.waitKey(1) == 27:
            # ESC to quit
            break

    cv2.destroyAllWindows()
