import cv2


def setup_capture():
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap


def crop_and_zoom(image):
    # Camera size
    height, width, channels = image.shape
    # TODO check variable names, x and y for height and width
    centreX = int(height / 2)
    centreY = int(width / 2)

    scaleFactorX = 2  # variable
    scaleFactorY = 2  # variable

    scaledHalfSizeX = int((height / scaleFactorX) / 2)
    scaledHalfSizeY = int((width / scaleFactorY) / 2)

    # Bounds
    minX = centreX - scaledHalfSizeX
    maxX = centreX + scaledHalfSizeX
    minY = centreY - scaledHalfSizeY
    maxY = centreY + scaledHalfSizeY

    cropped_image = image[minX:maxX, minY:maxY]

    scaled_cropped_image = cv2.resize(cropped_image, (width, height))

    return scaled_cropped_image


def detect_pieces():
    cap = setup_capture()

    while True:
        _, image = cap.read()

        zoomed_image = crop_and_zoom(image)
        cv2.imshow("img", zoomed_image)



        if cv2.waitKey(1) == 27:
            # ESC to quit
            break

    cv2.destroyAllWindows()
