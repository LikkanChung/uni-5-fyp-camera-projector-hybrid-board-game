import pygame


class TicTacToeBoard(pygame.sprite.Sprite):
    def __init__(self, window_size, listen_to, callback):
        super().__init__()
        self.image = pygame.Surface(window_size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.listen_to = listen_to
        self.callback = callback
        self.tile_surface = self.image.subsurface(self.image.get_rect().inflate(0, 0))
        self.board_anchor = (0, 0)
        self.board_size = (500, 500)
        self.game_state = [[None, None, None], [None, None, None], [None, None, None]]
        self.tile_size = (int(self.board_size[0] / 3), int(self.board_size[1] / 3))

        self.draw_grid()

    def update(self, events, dt):
        self.draw_grid()

    def update_board_bounds(self, anchor, size):
        self.board_anchor = anchor
        self.board_size = size
        self.tile_size = (int(self.board_size[0] / 3), int(self.board_size[1] / 3))

    def draw_grid(self):
        self.image.fill(pygame.Color('black'))

        row_count = 0
        for row in self.game_state:
            col_count = 0
            for tile_color in row:
                rel_x, rel_y = self.tile_size
                rel_x *= col_count
                rel_y *= row_count
                offset_x, offset_y = self.board_anchor
                tile = pygame.Rect(
                    (rel_x + offset_x, rel_y + offset_y),
                    self.tile_size
                )
                if tile_color:
                    pygame.draw.rect(self.tile_surface, pygame.Color(tile_color), tile)
                col_count += 1
            row_count += 1

        # Grid lines
        x, y = self.board_anchor
        for vertical in [self.tile_size[0], self.tile_size[0] * 2]:
            start = (vertical + x, 0 + y)
            end = (vertical + x, self.board_size[1] + y)
            pygame.draw.line(self.tile_surface, pygame.Color('white'), start, end, 2)
        for horizontal in [self.tile_size[1], self.tile_size[1] * 2]:
            start = (0 + x, horizontal + y)
            end = (self.board_size[0] + x, horizontal + y)
            pygame.draw.line(self.tile_surface, pygame.Color('white'), start, end, 2)

