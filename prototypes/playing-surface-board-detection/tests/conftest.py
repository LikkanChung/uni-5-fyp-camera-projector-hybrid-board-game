def mock_board():
    with open("assets/composite.jpg", "r") as mock_board_img:
        yield mock_board_img