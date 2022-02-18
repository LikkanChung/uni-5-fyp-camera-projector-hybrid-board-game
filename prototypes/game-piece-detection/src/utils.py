import cv2


def crop_and_zoom(image, scale_factor_x, scale_factor_y):
    # Camera size
    height, width, channels = image.shape

    centre_y = int(height / 2)
    centre_x = int(width / 2)

    scaled_half_size_y = int((height / scale_factor_y) / 2)
    scaled_half_size_x = int((width / scale_factor_x) / 2)

    # Bounds
    min_y = centre_y - scaled_half_size_y
    max_y = centre_y + scaled_half_size_y
    min_x = centre_x - scaled_half_size_x
    max_x = centre_x + scaled_half_size_x

    cropped_image = image[min_y:max_y, min_x:max_x]

    scaled_cropped_image = cv2.resize(cropped_image, (width, height))

    return scaled_cropped_image
