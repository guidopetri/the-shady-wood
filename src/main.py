#! /usr/bin/env python3

import pygame
import config
import sys
import random

from character import MainCharacter
from character import Snail
from background import Background
from background import Foreground
from background import Boundaries
from background import Shadows
from background import LightStatusEffects
from dialog import Dialog
from gui import Gui
from map import Map
from audio import Audio
from objects import Objects


def handle_events(state):
    keys_map = {pygame.K_UP: {'movement': (0, -config.character_speed),
                              'direction': 'back',
                              },
                pygame.K_DOWN: {'movement': (0, config.character_speed),
                                'direction': 'forward',
                                },
                pygame.K_LEFT: {'movement': (-config.character_speed, 0),
                                'direction': 'left',
                                },
                pygame.K_RIGHT: {'movement': (config.character_speed, 0),
                                 'direction': 'right',
                                 },
                }

    items_map = {pygame.key.key_code(config.keys['candle']): 'candle',
                 pygame.key.key_code(config.keys['firefly']): 'firefly',
                 pygame.key.key_code(config.keys['snail']): 'snail',
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
        if state['item'].endswith('_out'):
            return state
        state['action'] = 'standing'
        state['maze_begin'] = False
        state['msg_duration'] -= 1
        state['msg_duration'] = max(0, state['msg_duration'])
        for key, actions in keys_map.items():
            if keys[key]:
                state['position'] = tuple(map(sum, zip(state['position'],
                                                       actions['movement'])))
                state['action'] = 'walking'
                state['direction'] = actions['direction']

        if state['status'] == 'win':
            state['current_game_mode'] = config.Modes.WIN_DIALOG
            state['maze_begin'] = False
            state['map'] = state['win_map']
            state['item'] = 'waving'
            state['action'] = 'waving'
            state['direction'] = 'forward'
            state['position'] = config.initial_position

        if state['status'] == 'unsafe':
            # lose 1hp every 3 frames ~ 20hp per s ~ 5s in unsafe zone
            state['unsafe_frame_count'] += 1
            state['hp'] -= state['unsafe_frame_count'] // 3
            state['unsafe_frame_count'] %= 3
        if state['status'] == 'dead' or state['hp'] <= 0:
            state['hp'] = 0
            state['status'] = 'dead'
            state['game_over'] = True
            state['direction'] = 'forward'
            state['action'] = 'dead'
            state['item'] = 'dead'

        if state['game_over']:
            state['current_game_mode'] = config.Modes.GAME_OVER
            state['maze_begin'] = False

        if state['effect'] == 'regular':
            # randomly switch to other effects

            if state['effect_check_counter'] < config.effect_rate:
                state['effect_check_counter'] += 1
            else:
                state['effect_check_counter'] = 0

                val = random.random()
                if val < 0.025:
                    state['effect'] = 'moonlight'
                    state['effect_alpha'] = config.moonlight_default_alpha
                    state['effect_duration'] = config.moonlight_duration
                    state['effect_fade_in'] = True
                    state['can_use_item'] = False
                    # place item back in inventory
                    if state['item'] != 'none':
                        state['inventory'][state['item']] += 1
                        state['item'] = 'none'
                        state['can_use_item'] = False
                        state['item_duration'] = 0
                elif val < 0.05:
                    state['effect'] = 'lightning'
                    state['effect_alpha'] = config.lightning_default_alpha
                    state['effect_duration'] = config.lightning_duration
                    state['effect_fade_in'] = True
                    state['can_use_item'] = False
                    # place item back in inventory
                    if state['item'] != 'none':
                        state['inventory'][state['item']] += 1
                        state['item'] = 'none'
                        state['can_use_item'] = False
                        state['item_duration'] = 0
                else:
                    pass
        elif state['effect'] == 'moonlight':
            state['effect_duration'] -= 1
            state['effect_alpha'] -= config.moonlight_drop_rate

            # gain 1 hp for every N frames in moonlight
            N = 20
            state['moonlight_frame_count'] += 1
            state['hp'] += state['moonlight_frame_count'] // N
            state['moonlight_frame_count'] %= N
            # but make sure we don't go over 100
            state['hp'] = min(100, state['hp'])

            if state['effect_duration'] <= config.moonlight_fade_in_f:
                state['effect_fade_out'] = True
        elif state['effect'] == 'lightning':
            state['effect_duration'] -= 1

            if state['effect_check_counter'] < config.lightning_effect_rate:
                state['effect_check_counter'] += 1
            else:
                state['effect_check_counter'] = 0
                val = random.random()
                if val < config.lightning_freq:
                    state['effect_alpha'] = config.lightning_default_alpha

            state['effect_alpha'] += config.lightning_drop_rate
            state['effect_alpha'] = min(state['effect_alpha'], 255)

            if state['effect_duration'] <= config.lightning_fade_in_f:
                state['effect_fade_out'] = True

        if state['effect'] != 'regular' and state['effect_duration'] <= 0:
            state['effect'] = 'regular'
            state['effect_fade_in'] = False
            state['effect_fade_out'] = False
            state['can_use_item'] = True

        if state['can_use_item']:
            for key, item in items_map.items():
                if keys[key] and state['inventory'][item] > 0:
                    state['item'] = item
                    state['inventory'][item] -= 1
                    state['can_use_item'] = False
                    state['item_duration'] = config.item_durations[item]

                    if item == 'snail':
                        state['snail_position'] = state['position']
                    break
        elif state['item'] != 'none':
            state['item_duration'] -= 1

        reset_item = (state['item_duration'] <= 0
                      and state['item'] not in ('none', 'dead', 'waving'))
        if reset_item:
            state['item'] = f'{state["item"]}_out'
            state['action'] = 'item_out'
            state['direction'] = 'forward'
            state['can_use_item'] = True
            state['item_duration'] = 0

        tile_size = config.map_tile_size
        dist_to_tile_center = (state['position'][0]
                               % tile_size
                               - 0.5 * tile_size,
                               state['position'][1]
                               % tile_size
                               - 0.5 * tile_size,
                               )

        close_to_tile_center = (abs(dist_to_tile_center[0])
                                < config.pickup_item_sprite_size
                                and abs(dist_to_tile_center[1])
                                < config.pickup_item_sprite_size)
        current_tile = (state['position'][0] // tile_size,
                        state['position'][1] // tile_size,
                        )
        item = state['item_map'][current_tile[1]][current_tile[0]]
        if close_to_tile_center and item != ' ':
            state['inventory'][item] += 1
            state['item_map'][current_tile[1]][current_tile[0]] = ' '

        if config.debug_mode:
            if keys[pygame.K_a]:
                state['hp'] = min(state['hp'] + 1, 100)
            if keys[pygame.K_v]:
                state['hp'] = max(state['hp'] - 1, 0)
            if keys[pygame.K_d]:
                state['status'] = 'unsafe'
            if keys[pygame.K_b]:
                state['status'] = 'safe'
            if keys[pygame.K_g]:
                state['status'] = 'dead'
            if keys[pygame.K_e]:
                state['inventory']['candle'] += 1
            if keys[pygame.K_r]:
                state['inventory']['candle'] -= 1
            if keys[pygame.K_t]:
                state['action'] = 'firefly'
            if keys[pygame.K_y]:
                state['action'] = 'walking'
            if keys[pygame.K_u]:
                state['effect'] = 'moonlight'
            if keys[pygame.K_i]:
                state['effect'] = 'lightning'
            if keys[pygame.K_o]:
                state['effect'] = 'regular'
            if keys[pygame.K_p]:
                state['effect_alpha'] += 1
            if keys[pygame.K_l]:
                state['effect_alpha'] -= 1
    elif mode == config.Modes.GAME_OVER:
        pass
    elif mode == config.Modes.WIN_DIALOG:
        if any_key:
            state['active_message'] += 1
            if state['active_message'] >= len(config.game_win_text):
                state['current_game_mode'] = config.Modes.MAIN_MENU
                # revert to default state
                # return default_state
                state['active_message'] = 0

    return state


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)

    game_map = Map()
    game_map.generate_map()

    map_state = {'map': game_map.map,
                 'ai_map': game_map.ai_map,
                 'win_map': game_map.win_map,
                 'item_map': game_map.item_map,
                 }
    game_state = config.default_game_state.copy()
    game_state.update(map_state)

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)
    shadows = Shadows(surface, area=360, variance=240)
    # shadows = Shadows(surface, area=360, variance=48000)
    fg = Foreground(surface)
    gui = Gui(surface)
    boundaries = Boundaries(surface)
    light_fx = LightStatusEffects(surface)
    snail = Snail(surface)
    objects = Objects(surface)

    audio = Audio()

    if config.debug_mode:
        game_map.pretty_print()
        game_map.pretty_print_item()

    while True:
        boundaries.check_for_dmg(game_state)
        game_state = handle_events(game_state)

        surface.fill('black')

        bg.render(game_state)
        character.render(game_state)
        fg.render(game_state)

        shadows.render(game_state)
        # place snail above shadows
        objects.render(game_state)
        snail.render(game_state)
        light_fx.render(game_state)
        gui.render(game_state)
        dialog.render(game_state)

        audio.play(game_state)

        pygame.display.flip()

        clock.tick(config.framerate)
