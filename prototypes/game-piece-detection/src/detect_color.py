"""
Find a color threshold for each piece
"""
import os
import cv2
import numpy


BACKGROUND_THRESHOLD = 200


def get_data_path(color):
    return os.path.join('data', f'positive_{color}')


def get_threshold_image(image, threshold):
    # Using binary thresh on BGR images
    #image_threshold = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)[1]

    # Using filter mask in range
    threshold_filter = numpy.array([threshold, threshold, threshold])
    black_filter = numpy.array([0, 0, 0])
    mask = cv2.inRange(image, black_filter, threshold_filter)
    result = cv2.bitwise_and(image, image, mask=mask)
    return result


def average_color(image):
    # filter out black
    r = 0
    g = 0
    b = 0
    count = 0
    for row in image:
        for pixel in row:
            black_pixel = numpy.zeros(3, numpy.uint8)
            if not numpy.array_equal(pixel, black_pixel):
                b += pixel[0]
                g += pixel[1]
                r += pixel[2]
                count += 1
    return int(b / count), int(g / count), int(r / count)


def dominant_color(image):
    pixels = numpy.float32(image.reshape(-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
    flags = cv2.KMEANS_RANDOM_CENTERS
    _, labels, palette = cv2.kmeans(pixels, 1, None, criteria, 10, flags)
    _, counts = numpy.unique(labels, return_counts=True)
    return palette[numpy.argmax(counts)]


def detect_color_rgb(color):
    path = get_data_path(color)
    image_paths = os.listdir(path)
    colors = []

    for image_filename in image_paths:
        if '.jpg' in image_filename:
            image_full_filepath = os.path.join(get_data_path(color), image_filename)
            image = cv2.imread(image_full_filepath)

            # Filter background
            image_threshold = get_threshold_image(image, BACKGROUND_THRESHOLD)

            # Average color
            rgb = average_color(image_threshold)
            average_color_image = numpy.zeros((50, 50, 3), numpy.uint8)
            average_color_image[:] = rgb
            # Average colour (filtered out black) on threshold image seems to work the best
            colors.append(rgb)

            rgb_original = average_color(image)
            average_color_image_orig = numpy.zeros((50, 50, 3), numpy.uint8)
            average_color_image_orig[:] = rgb_original

            # Dominant color on threshold- k-means clustering
            dominant_color_rgb = dominant_color(image_threshold)
            dominant_color_image = numpy.zeros((50, 50, 3), numpy.uint8)
            dominant_color_image[:] = dominant_color_rgb

            # Dom col orig image
            dominant_color_rgb_orig = dominant_color(image)
            dominant_color_image_orig = numpy.zeros((50, 50, 3), numpy.uint8)
            dominant_color_image_orig[:] = dominant_color_rgb

            # combined_image = numpy.concatenate((image, image_threshold, average_color_image, average_color_image_orig, dominant_color_image, dominant_color_image_orig), axis=1)
            # print("Image shown: original, threshold, average threshold, average orig, dominant threshold, dominant original ")
            # cv2.imshow('colors', combined_image)
            # k = cv2.waitKey()
            # if k == 27:
            #     break
    # cv2.destroyAllWindows()

    zipped_colors = list(zip(*colors))
    min_color = min(zipped_colors[0]), min(zipped_colors[1]), min(zipped_colors[2])
    max_color = max(zipped_colors[0]), max(zipped_colors[1]), max(zipped_colors[2])
    return min_color, max_color


def detect_colors():
    colors = {
        'blue': None,
        'green': None,
        'purple': None,
        'red': None
    }

    print('| color | lower | average | higher |\n|---|---|---|---|')
    for color in colors:
        lower_color, higher_color = detect_color_rgb(color)

        lower_color_image = numpy.zeros((50, 50, 3), numpy.uint8)
        lower_color_image[:] = lower_color
        higher_color_image = numpy.zeros((50, 50, 3), numpy.uint8)
        higher_color_image[:] = higher_color

        average_col = average_color([[lower_color, higher_color]])
        average_col_image = numpy.zeros((50, 50, 3), numpy.uint8)
        average_col_image[:] = average_col

        colors[color] = numpy.concatenate((lower_color_image, average_col_image, higher_color_image), axis=0)
        print(f'| {color} | {lower_color} | {average_col} | {higher_color} |')

    # Show colors
    combined_colors = numpy.concatenate(list(colors.values()), axis=1)
    cv2.imshow('colors', combined_colors)
    cv2.waitKey()
    cv2.destroyAllWindows()


def find_threshold():
    threshold = 100
    colors = {
        'blue': os.listdir(get_data_path('blue')),
        'green': os.listdir(get_data_path('green')),
        'purple': os.listdir(get_data_path('purple')),
        'red': os.listdir(get_data_path('red'))
    }

    blue_image_paths = colors.get('blue')

    stop = False
    while not stop:
        for index in range(len(blue_image_paths)):
            color_images = []
            for color in colors:
                original_image = cv2.imread(os.path.join(get_data_path(color), colors.get(color)[index]))
                if original_image is None:
                    continue
                threshold_image = get_threshold_image(original_image, threshold)
                print(f'Threshold: {threshold} (= 255 - {255 - threshold})')
                if original_image is None or threshold_image is None:
                    continue
                combined_image = numpy.concatenate((threshold_image, original_image), axis=1)
                color_images.append(combined_image)

            all_colors = numpy.concatenate(color_images, axis=0)
            cv2.imshow("threshold", all_colors)

            key = cv2.waitKey(100)
            if key == 27:
                stop = True
            elif key == ord('a'):
                threshold = max(0, threshold - 1)
            elif key == ord('d'):
                threshold = min(255, threshold + 1)

    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_colors()