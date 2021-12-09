import cv2
import json
import pygame
from .utils.setup import load_config


def setup():
    config = load_config()

    # Display setup
    projector_resolution = (
        config.get('resolution').get('projector').get('x'),
        config.get('resolution').get('projector').get('y')
    )
    window = pygame.display.set_mode(projector_resolution, pygame.FULLSCREEN)
    pygame.display.flip()

    # Camera setup


def main():
    setup()

    running = True
    while running:
        # Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

