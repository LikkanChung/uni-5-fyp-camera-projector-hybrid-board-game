"""Helper tools to mnipulate images"""
import cv2


def scale_to(image, x, y):
    return cv2.resize(image, (x, y))


def crop_by_scale_factor(image, sf_x, sf_y):
    height, width, _ = image.shape

    centre_x = int(width / 2)
    centre_y = int(height / 2)

    scaled_width = width / sf_x
    scaled_height = height / sf_y

    offset_from_centre_x = scaled_width / 2
    offset_from_centre_y = scaled_height / 2

    min_x = int(centre_x - offset_from_centre_x)
    max_x = int(centre_x + offset_from_centre_x)
    min_y = int(centre_y - offset_from_centre_y)
    max_y = int(centre_y + offset_from_centre_y)

    cropped_image = image[min_y:max_y, min_x:max_x]
    return cropped_image
