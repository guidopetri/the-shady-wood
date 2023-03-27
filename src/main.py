#! /usr/bin/env python3

import pygame
import config
import sys

from character import MainCharacter
from background import Background
from dialog import Dialog
from background import Shadows
from gui import Gui


def handle_events(state, bg):
    keys_map = {pygame.K_UP: (0, config.character_speed),
                pygame.K_DOWN: (0, -config.character_speed),
                pygame.K_LEFT: (config.character_speed, 0),
                pygame.K_RIGHT: (-config.character_speed, 0),
                }

    any_key = False
    mode = state['current_game_mode']

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            any_key = True

    keys = pygame.key.get_pressed()

    if mode == config.Modes.MAIN_MENU:
        if any_key:
            state['current_game_mode'] = config.Modes.INTRO
    elif mode == config.Modes.INTRO:
        if any_key:
            state['active_message'] += 1
            if state['active_message'] >= len(config.intro_messages):
                state['current_game_mode'] = config.Modes.GAME
                state['active_message'] = 0
    elif mode == config.Modes.GAME:
        for key, movement in keys_map.items():
            if keys[key]:
                bg.move(movement)

    return state


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)

    game_state = {'current_game_mode': config.Modes.MAIN_MENU,
                  'active_message': 0,
                  'hp': 0,
                  'status': 'safe',
                  'inventory': [],
                  }

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)
    shadows = Shadows(surface, area=720, variance=48000)
    fg = Background(surface)
    gui = Gui(surface)

    while True:
        game_state = handle_events(game_state, bg)
        character.handle()

        bg.render(game_state)
        character.render(game_state)
        # fg.render(game_state)
        shadows.render(game_state)
        gui.render(game_state)
        dialog.render(game_state)

        pygame.display.flip()

        clock.tick(60)
