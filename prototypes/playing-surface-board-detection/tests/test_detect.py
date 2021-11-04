from detect import find_anchor_points
import cv2


def test_detect(mock_board):
    find_anchor_points(mock_board)


if __name__ == '__main__':
    test_detect(cv2.imread("assets/composite.jpg"))
