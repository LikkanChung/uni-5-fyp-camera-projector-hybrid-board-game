import cv2
import json


def find_anchor_points(image):
    qr_code_detector = cv2.QRCodeDetector()
    _, data_tuple, points_tuple, _ = qr_code_detector.detectAndDecodeMulti(image)

    tags = []

    # Match up points to anchors
    if data_tuple is not None and points_tuple is not None and len(data_tuple) == len(points_tuple):
        data = list(data_tuple)
        points = list(points_tuple.astype(int))
        for index in range(len(data)):
            try:
                tag = json.loads(data[index])
                tag['points'] = points[index].tolist()
                tags.append(tag)
            except:
                print("could not decode " + str(data[index]) + " in " + str(data))

    return tags


def tag_board(board, tags):
    board_tags = {}
    for tag in tags:
        print(tag)
        if tag['id'] == 'board':
            board_tags[tag['anchor']] = _get_center(tag['points'])
    print(board_tags)
    board.update(board_tags)
    return board


def _get_center(points):
    # A simple approach but does not account for parallax
    x = [i[0] for i in points]
    y = [i[1] for i in points]
    mid_x = int((min(x) + max(x)) / 2)
    mid_y = int((min(y) + max(y)) / 2)
    return [mid_x, mid_y]


def draw_bounds(image, points):
    num_points = len(points)
    for i in range(num_points):
        point_1 = points[i]
        point_2 = points[(i+1) % num_points]
        cv2.line(image, point_1, point_2, color=(255, 0, 0), thickness=2)
    return image


def crop_and_scale(image):
    scale_factor = 2.5

    height, width, channels = image.shape

    centre_y = int(height / 2)
    centre_x = int(width / 2)

    scaled_half_size_y = int((height / scale_factor) / 2)
    scaled_half_size_x = int((width / scale_factor) / 2)

    # Bounds
    min_y = centre_y - scaled_half_size_y
    max_y = centre_y + scaled_half_size_y
    min_x = centre_x - scaled_half_size_x
    max_x = centre_x + scaled_half_size_x

    cropped_image = image[min_y:max_y, min_x:max_x]

    scaled_cropped_image = cv2.resize(cropped_image, (width, height))

    return scaled_cropped_image

