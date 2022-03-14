import pygame
from ...common.game_logic.states import State
from .image_transform import scale_to, crop_by_scale_factor
from ..utils import debug



def input_event_handler(game_state):
    events = pygame.event.get()
    for e in events:
        # QUIT
        if (e.type == pygame.QUIT or
                (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE)):
            game_state['state'] = State.QUIT
    return events, game_state


def quit_handler(game_state):
    if game_state.get('state') is State.QUIT:
        print('quit handler pygame.quit')
        pygame.quit()


def capture_image(video_capture, update_debug=False):
    _, image = video_capture.read()
    height, width, _ = image.shape
    image = scale_to(crop_by_scale_factor(image, 2.5, 2.5), width, height)
    debug.debugger.update_image(image, 'camera')
    return image
