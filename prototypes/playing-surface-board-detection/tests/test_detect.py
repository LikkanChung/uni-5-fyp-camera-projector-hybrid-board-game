from detect import find_anchor_points, tag_board, draw_bounds
import cv2


def test_detect(mock_board):
    tags = find_anchor_points(mock_board)
    board_tags = tag_board(tags)
    image = draw_bounds(mock_board, list(board_tags.values()))
    h, w, _ = mock_board.shape
    image_scaled = cv2.resize(image, (int(w/2.5), int(h/2.5)))
    cv2.imshow("img", image_scaled)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    test_detect(cv2.imread("assets/composite.jpg"))
