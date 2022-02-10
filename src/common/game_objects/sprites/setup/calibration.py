# Sprite classes used in the calibration phase
import pygame


class CalibrationTitle(pygame.sprite.Sprite):
    def __init__(self, font, title, subtitle, size, listen_to, callback):
        super().__init__()
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        font.origin = True
        line_spacing_offset = 20
        text_surface = self.image.subsurface(self.image.get_rect().inflate(-50, -50))

        # Title text
        title_bounds = font.get_rect(title)
        x, y = size
        font.render_to(
            text_surface,
            ((x / 2) - (title_bounds.width / 2), (y / 2) - (title_bounds.height / 2) - line_spacing_offset),
            title,
            pygame.Color('white')
        )

        # Subtitle text
        subtitle_bounds = font.get_rect(subtitle)
        font.render_to(
            text_surface,
            ((x / 2) - (subtitle_bounds.width / 2), (y / 2) - (subtitle_bounds.height / 2) + line_spacing_offset),
            subtitle,
            pygame.Color('white')
        )

        self.callback = callback
        self.listen_to = listen_to

    def update(self, events, dt):
        pass
