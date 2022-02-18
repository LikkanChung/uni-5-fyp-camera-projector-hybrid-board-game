import cv2
from utils import crop_and_zoom


def setup_capture():
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    return cap


def detect_pieces():
    cap = setup_capture()

    while True:
        _, image = cap.read()

        zoomed_image = crop_and_zoom(image, 2.5, 2.5)
        cv2.imshow("img", zoomed_image)

        if cv2.waitKey(1) == 27:
            # ESC to quit
            break

    cv2.destroyAllWindows()
