"""
Helper class to aid dataset collection
"""
import copy

import cv2
import os


class ImageProcessor:
    def __init__(self, crop_dimension, destination_path, sample_type, sample_key):
        self.image = None
        self.crop_dimension = crop_dimension
        self.write_path = destination_path  # Includes the sample type dir
        self.filename_prefix = sample_type
        self.filename_postfix = 0
        self.sample_key = sample_key
        self.is_first_capture = True

    def _get_new_filename(self):
        # Ensure path exists
        if not os.path.exists(self.write_path):
            os.makedirs(self.write_path)

        postfix = str(self.filename_postfix).zfill(4)
        filename = f'{self.filename_prefix}_{postfix}.jpg'

        self.filename_postfix += 1
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

            # If negative - capture data point for statistics purposes
            if self.filename_prefix == 'negative':
                sample_points_path = os.path.join(self.write_path, 'sample_points')
                if not os.path.isdir(sample_points_path):
                    os.makedirs(sample_points_path)

                if self.is_first_capture is True:
                    # Capture whole image, this should
                    filename = f'image_{self.filename_prefix}_{self.sample_key}.png'
                    cv2.imwrite(os.path.join(sample_points_path, filename), self.image)
                    self.is_first_capture = False

                point_filepath = os.path.join(sample_points_path, 'sample_points.csv')
                if not os.path.exists(point_filepath):
                    # Create new CSV file if not exists
                    with open(point_filepath, 'w') as new_points_file:
                        new_points_file.write('sample_key,x,y\n')
                with open(point_filepath, 'a') as points:
                    # Add points to list
                    points.write(f'{self.sample_key},{x},{y}\n')

            cropped_image = self.image[minY:maxY, minX:maxX]

            # Save image
            filename = self._get_new_filename()
            while os.path.isfile(filename):
                filename = self._get_new_filename()
            cv2.imwrite(filename, cropped_image)

            print(f'Captured and saved as {filename}')

            # Append to Description file
            descriptor_filetype = ''
            data = ''
            if 'positive' in self.filename_prefix:
                descriptor_filetype = '.dat'
                # Positive descriptor: <filename> <num of objects> <x1> <y1> <width1> <height1> [<x2> <y2> <h2> <w2>...]
                centre_coordinate = int(self.crop_dimension / 2)
                data = f' 1 0 0 {self.crop_dimension} {self.crop_dimension}'
            elif self.filename_prefix == 'negative':
                descriptor_filetype = '.txt'
            else:
                raise(Exception('Incorrect sample type'))
            descriptor_filename = f'{self.filename_prefix}{descriptor_filetype}'
            descriptor_filepath = os.path.join(self.write_path, descriptor_filename)
            with open(descriptor_filepath, 'a') as df:
                df.write(f'{filename}{data}\n')
