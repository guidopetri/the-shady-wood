#! /usr/bin/env python3

import pygame
import config
import sys

from character import MainCharacter
from background import Background
from dialog import Dialog


def handle_events(bg, character):
    keys_map = {pygame.K_UP: (0, config.character_speed),
                pygame.K_DOWN: (0, -config.character_speed),
                pygame.K_LEFT: (config.character_speed, 0),
                pygame.K_RIGHT: (-config.character_speed, 0),
                }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    for key, movement in keys_map.items():
        if keys[key]:
            bg.move(movement)


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)

    while True:
        handle_events(bg, character)
        character.handle()

        bg.render(config.Modes.GAME)
        character.render(config.Modes.GAME)
        dialog.render(config.Modes.GAME)

        pygame.display.flip()

        clock.tick(60)
