import cv2
import pygame.sprite

from ....common.game_objects.sprites.setup import calibration


class Calibrator:
    def __init__(self, calibrate_sprites, font, projector_resolution):
        self.complete = False
        self.results = {}
        self.calibrate_sprites = calibrate_sprites
        self.font = font
        self.projector_resolution = projector_resolution
        self.instruction = None

    def is_complete(self):
        return self.complete

    def get_results(self):
        return self.results

    def start(self):
        title = calibration.CalibrationTitle(
            self.font, 'Calibrating', 'Please wait', self.projector_resolution, None, None
        )
        self.calibrate_sprites.add(title)
        # 1. This should project 4 squares on the playing surface, doesn't matter where -
        # but the locations are known in the projector coordinate frame
        piece_tiles = calibration.CalibrationTiles(self.projector_resolution, None, None)
        self.calibrate_sprites.add(piece_tiles)
        piece_tiles.add_tile(pygame.Color('red'), -150, -150)
        piece_tiles.add_tile(pygame.Color('green'), 150, 100)
        piece_tiles.add_tile(pygame.Color('blue'), -150, 100)
        piece_tiles.add_tile(pygame.Color('purple'), 150, -150)
        title.set_subtitle('Place coloured pieces onto tiles')
        self.instruction = title
        # 2. The player places 4 colored pieces in those squares

    def step_2(self):
        # 2. The player places 4 colored pieces in those squares
        self.instruction.set_subtitle('Press space when ready')
        
    def step_3(self):
        # 3. The camera detects the location of the pieces in the camera frame
        # 4. Line up the two frames
        self.instruction.set_subtitle('Please wait')
        print('step3')

    def align_frames(self):
        pass
