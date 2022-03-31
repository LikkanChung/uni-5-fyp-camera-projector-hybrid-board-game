from ....game_objects.sprites.tic_tac_toe.board import TicTacToeBoard
from src.client.utils.detection.board import convert_box_to_rect


class GameHandler:
    def __init__(self, window_size, font):
        self.board = TicTacToeBoard(window_size, font, None, None)
        self.sprite_group = None
        self.board_anchor = (0, 0)
        self.board_size = (500, 500)
        self.end = False

    def start(self, sprite_group):
        self.sprite_group = sprite_group
        self.sprite_group.add(self.board)

    def check_win_state(self):
        winner = ''
        game_state = self.board.get_game_state()
        for row in game_state:
            if all(tile is not None and row[0] == tile for tile in row):
                winner = f'{row[0].upper()} wins!'
                break
        if winner == '':
            for i in range(len(game_state)):
                color = game_state[0][i]
                match = True
                for row in game_state:
                    if row[i] is None or not row[i] == color:
                        match = False
                if match:
                    winner = f'{color.upper()} wins!'
        if winner == '':
            # diagonals
            if all(tile is not None and game_state[0][0] == tile for tile in [game_state[1][1], game_state[2][2]]):
                # top left to bottom right
                winner = f'{game_state[0][0].upper()} wins!'
            elif all(tile is not None and game_state[2][0] == tile for tile in [game_state[1][1], game_state[0][2]]):
                # top right to bottom left
                winner = f'{game_state[2][0].upper()} wins!'
        if not winner == '':
            self.end = True
            self.board.update_message(winner + "   Remove pieces from board to play again")

    def update_board(self, board_boundaries):
        # board boundaries of type box, convert to rect with rotation
        anchor, size = convert_box_to_rect(board_boundaries)
        self.board.update_board_bounds(anchor, size)
        self.board_anchor = anchor
        self.board_size = size
        self.check_win_state()

    def update_tokens(self, tokens):
        # self.board.reset_game_state()
        for token in tokens:
            # Calculate position on board
            token_x, token_y = token.get_coordinate()
            board_x, board_y = self.board_anchor
            dx = token_x - board_x
            dy = token_y - board_y
            col = min(max(0, int(dx / (self.board_size[0] / 3))), 2)
            row = min(max(0, int(dy / (self.board_size[1] / 3))), 2)
            self.board.update_game_state(row, col, token.get_color())
            # print(f'{token} in {row},{col}')
        self.check_win_state()

    def is_finished(self):
        return self.end

    def reset_game(self):
        self.end = False
        self.board.update_message("")
        for row in range(3):
            for col in range(3):
                self.board.update_game_state(row, col, None)

