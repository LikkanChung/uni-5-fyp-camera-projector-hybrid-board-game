import pygame
from ...common.game_logic.states import State


def input_event_handler(game_state):
    events = pygame.event.get()
    for e in events:
        # QUIT
        if (e.type == pygame.QUIT or
                (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE)):
            game_state['state'] = State.QUIT
    print('input handler returning', game_state)
    return events, game_state


def quit_handler(game_state):
    if game_state.get('state') is State.QUIT:
        print('quit handler pygame.quit')
        pygame.quit()
