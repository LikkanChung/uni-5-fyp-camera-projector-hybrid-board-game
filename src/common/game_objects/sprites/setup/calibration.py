# Sprite classes used in the calibration phase
import pygame


class CalibrationTitle(pygame.sprite.Sprite):
    def __init__(self, font, title, subtitle, window_size, listen_to, callback):
        super().__init__()
        self.image = pygame.Surface(window_size)
        self.rect = self.image.get_rect()
        self.font = font
        self.title = title
        self.subtitle = subtitle
        self.window_size = window_size

        self.font.origin = True
        self.line_spacing_offset = 20
        self.text_surface = self.image.subsurface(self.image.get_rect().inflate(-50, -50))

        self.callback = callback
        self.listen_to = listen_to

        self._update_titles()

    def update(self, events, dt):
        pass

    def _clear_surface(self):
        # Fill background with black color to overwrite blitted text, instead of making new surface
        self.text_surface.fill(pygame.Color('black'))

    def _render_text(self, text, line_offset_spacing):
        # Title text
        text_bounds = self.font.get_rect(text)
        x, y = self.window_size
        self.font.render_to(
            self.text_surface,
            ((x / 2) - (text_bounds.width / 2), (y / 2) - (text_bounds.height / 2) + line_offset_spacing),
            text,
            pygame.Color('white')
        )

    def _update_titles(self):
        self._clear_surface()
        self._render_text(self.title, self.line_spacing_offset * -1)
        self._render_text(self.subtitle, self.line_spacing_offset)

    def set_subtitle(self, text):
        self.subtitle = text
        self._update_titles()


class CalibrationTiles(pygame.sprite.Sprite):
    def __init__(self, window_size, listen_to, callback):
        super().__init__()
        self.image = pygame.Surface(window_size, pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.tile_surface = self.image.subsurface(self.image.get_rect().inflate(-50, -50))
        x, y = window_size
        self.centre_x = x / 2
        self.centre_y = y / 2

    def update(self, events, dt):
        pass

    def add_tile(self, color, relative_position_xy, size=30):
        relative_position_x, relative_position_y = relative_position_xy
        tile = pygame.Rect(
            (self.centre_x + relative_position_x, self.centre_y + relative_position_y),
            (size, size)
        )
        pygame.draw.rect(self.tile_surface, color, tile)
