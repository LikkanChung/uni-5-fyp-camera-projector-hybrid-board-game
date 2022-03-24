import cv2
import pygame
import pygame.freetype
from .utils.setup import get_initial_game_state
from .utils.input_handler import input_event_handler, quit_handler, capture_image
from ..common.game_logic.states import State
from ..common.game_logic.games.tic_tac_toe.game import GameHandler
from .utils.calibration.calibration import Calibrator
from .utils.detection.board import BoardBoundary, convert_box_to_rect
from .utils.detection.tokens import TokenDetection
from .utils import debug
from .utils.config import config
from .utils.image_transform import crop_to, scale_by
from ..common.game_logic.smoothing import PointSmoother


def detect_board_elements(video_capture, game_board, token_detector):
    image = capture_image(video_capture)
    scaled_image = scale_by(image, 1.5)

    board_boundaries = game_board.find_board(scaled_image)
    anchor, size = convert_box_to_rect(board_boundaries)
    debug.debugger.update_annotation('board', anchor, size)

    min_x, min_y = anchor
    d_x, d_y = size

    board_image = crop_to(scaled_image, anchor, (min_x + d_x, min_y + d_y))
    tokens = token_detector.find_pieces(board_image, anchor)

    return board_boundaries, tokens


def setup():

    # Debugger
    debug.debugger.set_enabled(config.get_property(['debug', 'enabled']))
    debug.debugger.set_window_size(
        config.get_property(['debug', 'x']),
        config.get_property(['debug', 'y'])
    )

    # Display setup
    projector_resolution = (
        config.get_property(['resolution', 'projector', 'x']),
        config.get_property(['resolution', 'projector', 'y']),
    )
    pygame.init()
    font = pygame.freetype.SysFont(None, config.get_property(['client', 'font']),)
    config.set_global_pygame_font(font)
    clock = pygame.time.Clock()
    dt = 0

    window = pygame.display.set_mode(projector_resolution, pygame.FULLSCREEN)
    pygame.display.flip()

    # Camera setup
    video_capture = cv2.VideoCapture(config.get_property(['resolution', 'camera', 'id']))
    video_capture.set(3, config.get_property(['resolution', 'camera', 'x']))
    video_capture.set(4, config.get_property(['resolution', 'camera', 'y']))

    # Calibrate
    calibrate_sprites = pygame.sprite.Group()
    calibrator = Calibrator(calibrate_sprites, font, projector_resolution)
    calibrator.start()

    # Board and Piece objects
    game_board = BoardBoundary(config.get_property(['client', 'color', 'board_detect_threshold']))
    token_detector = TokenDetection(None)
    tokens_buffer = {}

    for color in config.get_property(['client', 'color', 'classes']):
        tokens_buffer[color] = PointSmoother('point', 5)

    game_state = get_initial_game_state()
    step_3_start_timestamp = 10000
    start_step_3 = False
    while game_state.get('state') is State.CALIBRATING:
        events, game_state = input_event_handler(game_state)
        calibrate_sprites.update(events, dt)
        calibrate_sprites.draw(window)
        pygame.display.update()
        dt = clock.tick(60)
        debug.debugger.update_variables('time', dt)

        # Image handling
        board_boundaries, tokens = detect_board_elements(video_capture, game_board, token_detector)

        for token in tokens:
            tokens_buffer[token.get_color()].add_point(token.get_coordinate())

            x, y = token.get_coordinate()
            debug_anchor = (x - 5, y - 5)
            debug.debugger.update_annotation(f'{token.get_color()}_coord', debug_anchor, (10, 10))

        [debug.debugger.update_variables(f'token_{t.get_color()}', t) for t in tokens]

        if pygame.time.get_ticks() > 5000:
            if not start_step_3:
                calibrator.step_2()
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    start_step_3 = True
                    calibrator.step_3()
                    # Add some waiting time to allow the buffers to smooth
                    step_3_start_timestamp = pygame.time.get_ticks() + 5000
            if start_step_3 and pygame.time.get_ticks() > step_3_start_timestamp:
                break
        quit_handler(game_state)

    events, game_state = input_event_handler(game_state)
    calibrate_sprites.update(events, dt)
    calibrate_sprites.draw(window)
    pygame.display.update()
    dt = clock.tick(60)
    debug.debugger.update_variables('time', dt)
    # Calibrate frames
    for color in tokens_buffer:
        tokens_buffer[color] = tokens_buffer.get(color).get_average()
    calibrator.align_frames(tokens_buffer)
    game_state['state'] = State.MAIN

    return window, clock, game_state, video_capture, calibrator, game_board, token_detector


def main():
    window, clock, game_state, video_capture, calibrator, game_board, token_detector = setup()

    # todo make it enter a game handler which has backgrounds etc

    print('Starting main game loop', game_state)
    while game_state.get('state') is State.MAIN:
        # Quit event handlers
        events, game_state = input_event_handler(game_state)
        dt = clock.tick(60)

        projector_resolution = (
            config.get_property(['resolution', 'projector', 'x']),
            config.get_property(['resolution', 'projector', 'y']),
        )

        tic_tac_toe = GameHandler(projector_resolution)

        # start a game
        game_state['state'] = State.GAME
        game_sprite_group = pygame.sprite.Group()
        tic_tac_toe.start(game_sprite_group)
        while game_state.get('state') is State.GAME:
            events, game_state = input_event_handler(game_state)
            dt = clock.tick(60)
            debug.debugger.update_variables('time', dt)

            board_boundaries, tokens = detect_board_elements(video_capture, game_board, token_detector)
            tic_tac_toe.update_board(board_boundaries)

            game_sprite_group.update(events, dt)
            game_sprite_group.draw(window)
            pygame.display.update()
            quit_handler(game_state)

        pygame.display.update()
        debug.debugger.update_variables('time', dt)
        quit_handler(game_state)

