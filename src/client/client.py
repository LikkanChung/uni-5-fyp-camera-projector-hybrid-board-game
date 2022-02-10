import cv2
import json
import pygame
import pygame.freetype
from .utils.setup import load_config, get_initial_game_state
from .utils.input_handler import input_event_handler, quit_handler
from ..common.game_objects.sprites.setup import calibration
from ..common.game_logic.states import State


def setup():
    config = load_config()

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
    cv2.VideoCapture(config.get('resolution').get('camera').get('id'))

    # Calibrate
    calibrate_sprites = pygame.sprite.Group()
    calibrate_sprites.add(calibration.CalibrationTitle(font, "Calibrating", "Please wait...", projector_resolution, None, None))

    game_state = get_initial_game_state()
    while game_state.get('state') is State.CALIBRATING:
        events, game_state = input_event_handler(game_state)

        print('calibrating ', game_state)
        calibrate_sprites.update(events, dt)
        calibrate_sprites.draw(window)
        pygame.display.update()
        dt = clock.tick(60)

        if pygame.time.get_ticks() > 1000:
            print(pygame.time.get_ticks())
            game_state['state'] = State.MAIN
        quit_handler(game_state)
    print('last before return ', game_state)
    return config, font, clock, game_state


def main():
    config, font, clock, game_state = setup()

    print('before main while', game_state)
    while game_state.get('state') is State.MAIN:
        # Quit event handlers
        events, game_state = input_event_handler(game_state)


        print('in main')

        dt = clock.tick(60)
        quit_handler(game_state)

