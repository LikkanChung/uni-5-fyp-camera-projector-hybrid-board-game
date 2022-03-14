import cv2
import json
import pygame
import pygame.freetype
from .utils.setup import load_config, get_initial_game_state
from .utils.input_handler import input_event_handler, quit_handler, capture_image
from ..common.game_logic.states import State
from .utils.calibration.calibration import Calibrator
from .utils.detection.board import BoardBoundary, convert_box_to_rect
from .utils import debug
from .utils.image_transform import crop_by_scale_factor, scale_to


def setup():
    config = load_config()

    # Debugger
    debug.debugger.set_enabled(config.get('debug').get('enabled'))
    debug.debugger.set_window_size(
        config.get('debug').get('x'),
        config.get('debug').get('y')
    )

    # Display setup
    projector_resolution = (
        config.get('resolution').get('projector').get('x'),
        config.get('resolution').get('projector').get('y')
    )
    pygame.init()
    font = pygame.freetype.SysFont(None, config.get('client').get('font'))
    clock = pygame.time.Clock()
    dt = 0

    window = pygame.display.set_mode(projector_resolution, pygame.FULLSCREEN)
    pygame.display.flip()

    # Camera setup
    video_capture = cv2.VideoCapture(config.get('resolution').get('camera').get('id'))
    video_capture.set(3, config.get('resolution').get('camera').get('x'))
    video_capture.set(4, config.get('resolution').get('camera').get('y'))

    # Calibrate
    calibrate_sprites = pygame.sprite.Group()
    calibrator = Calibrator(calibrate_sprites, font, projector_resolution)
    calibrator.start()

    # Board and Piece objects
    game_board = BoardBoundary(config.get('client').get('color').get('board_detect_threshold'))

    game_state = get_initial_game_state()
    while game_state.get('state') is State.CALIBRATING:
        events, game_state = input_event_handler(game_state)
        calibrate_sprites.update(events, dt)
        calibrate_sprites.draw(window)
        pygame.display.update()
        dt = clock.tick(60)
        debug.debugger.update_variables('time', dt)

        # Image handling
        image = capture_image(video_capture)

        board_boundaries = game_board.find_board(image)
        anchor, size = convert_box_to_rect(board_boundaries)
        debug.debugger.update_annotation('board', anchor, size)

        if pygame.time.get_ticks() > 1000 and False:
            print(pygame.time.get_ticks())
            game_state['state'] = State.MAIN
        quit_handler(game_state)
    print('last before return ', game_state)
    return config, font, clock, game_state, video_capture


def main():
    config, font, clock, game_state, video_capture = setup()

    print('before main while', game_state)
    while game_state.get('state') is State.MAIN:
        # Quit event handlers
        events, game_state = input_event_handler(game_state)

        image = capture_image(video_capture)

        dt = clock.tick(60)
        debug.debugger.update_variables('time', dt)
        quit_handler(game_state)

