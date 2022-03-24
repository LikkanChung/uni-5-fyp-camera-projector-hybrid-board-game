from src.detect import find_anchor_points, tag_board, draw_bounds
import cv2


def test_detect(mock_board):

    board = {
    }

    tags = find_anchor_points(mock_board)
    board = tag_board(board, tags)
    image = draw_bounds(mock_board, list(board.values()))
    h, w, _ = mock_board.shape
    image_scaled = cv2.resize(image, (int(w/2.5), int(h/2.5)))
    cv2.imshow("img", image_scaled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_detect_live():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)  # set the Horizontal resolution
    cap.set(4, 1080)  # Set the Vertical resolution

    board = {

    }

    while True:
        _, image = cap.read()

        tags = find_anchor_points(image)
        for tag in tags:
            image = draw_bounds(image, tag['points'])
        board = tag_board(board, tags)
        image = draw_bounds(image, list(board.values()))
        h, w, _ = image.shape
        image_scaled = cv2.resize(image, (int(w), int(h)))

        cv2.imshow("img", image_scaled)
        if cv2.waitKey(1) == ord("q"):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    test_detect(cv2.imread("assets/composite.jpg"))
    test_detect_live()
