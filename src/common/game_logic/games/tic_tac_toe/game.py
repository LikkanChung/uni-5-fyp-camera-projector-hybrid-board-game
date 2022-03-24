from ....game_objects.sprites.tic_tac_toe.board import TicTacToeBoard
from src.client.utils.detection.board import convert_box_to_rect


class GameHandler:
    def __init__(self, window_size):
        self.board = TicTacToeBoard(window_size, None, None)
        self.sprite_group = None

    def start(self, sprite_group):
        self.sprite_group = sprite_group
        self.sprite_group.add(self.board)

    def update_board(self, board_boundaries):
        # board boundaries of type box, convert to rect with rotation
        rect, size = convert_box_to_rect(board_boundaries)
        self.board.update_board_bounds(rect, size)

