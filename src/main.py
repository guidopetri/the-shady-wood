#! /usr/bin/env python3

import pygame
import config
import sys

from character import MainCharacter
from background import Background
from dialog import Dialog
from background import Shadows


def handle_events(current_game_mode, message, bg, character):
    keys_map = {pygame.K_UP: (0, config.character_speed),
                pygame.K_DOWN: (0, -config.character_speed),
                pygame.K_LEFT: (config.character_speed, 0),
                pygame.K_RIGHT: (-config.character_speed, 0),
                }

    any_key = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            any_key = True

    keys = pygame.key.get_pressed()

    if current_game_mode == config.Modes.MAIN_MENU:
        if any_key:
            current_game_mode = config.Modes.INTRO
    elif current_game_mode == config.Modes.INTRO:
        if any_key:
            message += 1
            if message >= len(config.intro_messages):
                current_game_mode = config.Modes.GAME
                message = 0
    elif current_game_mode == config.Modes.GAME:
        for key, movement in keys_map.items():
            if keys[key]:
                bg.move(movement)

    return current_game_mode, message


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)
    current_game_mode = config.Modes.MAIN_MENU
    active_message = 0

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)
    shadows = Shadows(surface, area=720, variance=48000)
    fg = Background(surface)

    while True:
        current_game_mode, active_message = handle_events(current_game_mode, active_message, bg, character)  # noqa
        character.handle()

        bg.render(current_game_mode)
        character.render(current_game_mode)
        # fg.render(current_game_mode)
        shadows.render(current_game_mode)
        dialog.render(current_game_mode, active_message)

        pygame.display.flip()

        clock.tick(60)
