"""
Helper class to aid dataset collection
"""
import copy

import cv2
import os


class ImageProcessor:
    def __init__(self, crop_dimension, destination_path, filename_prefix):
        self.image = None
        self.crop_dimension = crop_dimension
        self.write_path = destination_path
        self.filename_prefix = filename_prefix
        self.filename_postfix = 0

    def _get_new_filename(self):
        postfix = str(self.filename_postfix).zfill(4)
        self.filename_postfix += 1
        filename = f'{self.filename_prefix}_{postfix}.jpg'
        return os.path.join(self.write_path, filename)

    def set_image(self, image):
        self.image = image

    def click_event(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONUP:
            self.capture_image_and_save(x, y)

    def capture_image_and_save(self, x, y):
        # TODO logic to capture image of right size and save to a directory
        if self.image is not None:
            print(x, " ", y)
            height, width, _ = self.image.shape
            # Crop image
            offset = int(self.crop_dimension / 2)
            minX = max(0, x - offset)
            minY = max(0, y - offset)
            maxX = min(width, x + offset)
            maxY = min(height, y + offset)

            cropped_image = self.image[minY:maxY, minX:maxX]

            # Save image
            filename = self._get_new_filename()
            while os.path.isfile(filename):
                filename = self._get_new_filename()
            cv2.imwrite(filename, cropped_image)

            print(f'Captured and saved as {filename}')
