import pygame


class TicTacToeBoard(pygame.sprite.Sprite):
    def __init__(self, window_size, font, listen_to, callback):
        super().__init__()
        self.image = pygame.Surface(window_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.listen_to = listen_to
        self.callback = callback
        self.tile_surface = self.image.subsurface(self.image.get_rect().inflate(0, 0))
        self.board_anchor = (0, 0)
        self.board_size = (500, 500)
        self.game_state = [[None, None, None], [None, None, None], [None, None, None]]
        self.message = ""
        self.font = font
        self.tile_size = (int(self.board_size[0] / 3), int(self.board_size[1] / 3))

        self.draw_grid()

    def update(self, events, dt):
        self.draw_grid()
        self.draw_text_message()

    def update_board_bounds(self, anchor, size):
        self.board_anchor = anchor
        self.board_size = size
        self.tile_size = (int(self.board_size[0] / 3), int(self.board_size[1] / 3))

    def reset_game_state(self):
        self.game_state = [[None, None, None], [None, None, None], [None, None, None]]

    def update_game_state(self, row, col, color):
        self.game_state[row][col] = color

    def get_game_state(self):
        return self.game_state

    def update_message(self, message):
        self.message = message

    def draw_grid(self):
        self.image.fill(pygame.Color('black'))

        # Token tiles
        row_count = 0
        for row in self.game_state:
            col_count = 0
            for tile_color in row:
                rel_x, rel_y = self.tile_size
                rel_x *= col_count
                rel_y *= row_count
                offset_x, offset_y = self.board_anchor
                tile = pygame.Rect(
                    (rel_x + (offset_x * (2/3)), rel_y + (offset_y * (2/3))),
                    self.tile_size
                )
                if tile_color:
                    pygame.draw.rect(self.tile_surface, pygame.Color(tile_color), tile)
                col_count += 1
            row_count += 1

        # Grid lines
        x, y = self.board_anchor
        x = x * (2/3)
        y = y * (2/3)
        for vertical in [self.tile_size[0], self.tile_size[0] * 2]:
            start = (vertical + x, 0 + y)
            end = (vertical + x, self.board_size[1] + y)
            pygame.draw.line(self.tile_surface, pygame.Color('white'), start, end, 5)
        for horizontal in [self.tile_size[1], self.tile_size[1] * 2]:
            start = (0 + x, horizontal + y)
            end = (self.board_size[0] + x, horizontal + y)
            pygame.draw.line(self.tile_surface, pygame.Color('white'), start, end, 5)

    def draw_text_message(self):
        text_bounds = self.font.get_rect(self.message)
        x, y = self.board_anchor
        x_pos = (self.board_anchor[0] + (self.board_size[0] / 2)) - (text_bounds.width / 2)
        y_pos = self.board_anchor[1] + self.board_size[1] + 10
        self.font.render_to(
            self.tile_surface,
            (x_pos, y_pos),
            self.message,
            pygame.Color('white')
        )
