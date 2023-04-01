import enum
import os
from pathlib import Path
from math import ceil


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
    INTRO = 2
    GAME_OVER = 3
    WIN_DIALOG = 4


debug_mode = True

screen_size = (1080, 720)
screen_center = tuple(x // 2 for x in screen_size)

framerate = 60

character_speed = 2
snail_speed = 8

fontname = 'Copperplate Gothic'
fontsize = 24
font_color = '#303030'

dialog_border_color = 'blue'
dialog_box_color = 'yellow'
menu_bg_color = 'yellow'
dialog_border_radius = 5
border_padding = 10
border_size = (20, 10)
text_padding = (0, 3)

main_menu_bg_color = '#072016'
main_menu_text = 'Press any key to start'
menu_text_padding = (0, 50)
title_padding = (0, -30)

courage_fontname = 'Copperplate Gothic'
courage_fontsize = 14
courage_font_color = 'black'

hp_bar_border_radius = 3
full_hp_color = '#00aa00'
empty_hp_color = '#cc0000'
hp_bar_bg_color = '#222222'
hp_indicator_size = (150,  # ~ 1080 / 8 + 10%
                     40,  # ~ 720 / 20 + 10%
                     )
hp_bar_border_thickness = 1

item_fontsize = 14
item_icon_size = 48
item_padding = 11
item_bar_size = (3 * item_icon_size + 4 * item_padding,
                 item_icon_size + 2 * item_padding,
                 )
item_font_color = 'black'
item_count_padding = (-3, 2)
item_key_padding = (0, 1)
item_letter_padding = (0, -1)

img_buffer = 2

main_dir = Path(os.path.split(os.path.abspath(__file__))[0])
root = main_dir / '..'
gfx_path = root / 'assets' / 'gfx'
sfx_path = root / 'assets' / 'fx'

intro_messages = [('anne_normal',
                   'All I wanted was a nice picnic at my favorite spot.'),
                  ('anne_normal',
                   'Unfortunately for me, I wasn\'t the only one using it today.'),  # noqa
                  ('anne_normal',
                   'When I arrived at the spot and sat down, something poked at me!'),  # noqa
                  ('anne_normal',
                   'I had sat on a tiny angry fairy!'),
                  ('anne_normal',
                   'It was so upset it cast a spell on me and...'),
                  ('anne_normal',
                   'it transported me to the middle of the Shady Wood!'),
                  ('anne_normal',
                   'The Shady Wood is cursed.'),
                  ('anne_normal',
                   'Anyone who shows fear gets turned to stone and lost forever.'),  # noqa
                  ('anne_normal',
                   'I need to keep courage and find my way out!'),
                  ]

maze_begin_message = ('anne_normal',
                      'It\'s a good thing I packed some candles. But I don\'t think they\'ll be enough...')  # noqa

items = ['firefly', 'candle', 'snail']
keys = {'firefly': 'f',
        'candle': 'c',
        'snail': 's',
        }

firefly_duration_in_s = 2.75
firefly_flashes = 5
firefly_flash_frames = framerate // 2
item_durations = {'candle': 15 * framerate,
                  'firefly': int((firefly_duration_in_s * firefly_flashes
                                  + firefly_flash_frames / framerate)
                                 * framerate),
                  'snail': 30 * framerate,
                  }
item_variances = {'candle': 13000,
                  'firefly': 9600,
                  'snail': 4800,
                  }
firefly_default_variance = 2400
firefly_flash_frames_freq = framerate * firefly_duration_in_s

item_end_messages = {'candle': ('anne_negative', 'Oh... It\'s all used up...'),
                     'firefly': ('anne_negative', 'Oh... It flew away...'),
                     }

first_item_messages = {'firefly': ('anne_normal', 'A firefly! That will help light my way! I can keep it in my jar.'),  # noqa
                       'snail': ('anne_normal', 'A glowing snail! It should help me, but they have a mind of their own...'),  # noqa
                       }

first_item_end_messages = {'snail': ('anne_normal', 'Whoa, that\'s a fast snail! At least it showed me the way out.'),  # noqa
                           }

default_map_size = (11, 11)
map_tile_size = 384
map_buffer_size = ceil(max(screen_size) / map_tile_size)

boundary_safe_zone_color = '#15ff00'
boundary_unsafe_zone_color = '#0000ff'
boundary_dead_zone_color = '#ff0000'
boundary_win_zone_color = '#fff000'

game_win_text = [('anne_normal', 'I found a road! I can make it home safely now.'),  # noqa
                 ('anne_normal', 'Thank you for your help!'),
                 ]

game_over_text = ['GAME OVER',
                  'Anne became too afraid. She turned to stone...',
                  ]

game_over_fontname = 'Copperplate Gothic'
game_over_fontsize = 20
game_over_font_color = 'white'

moonlight_color = 'blue'
moonlight_default_alpha = 120
moonlight_duration = 20 * framerate
moonlight_drop_rate = (255 - moonlight_default_alpha) / moonlight_duration
moonlight_fade_in_s = 3
moonlight_fade_in_f = moonlight_fade_in_s * framerate
moonlight_text = ('anne_normal', 'The Moon came out. Now I can see my way!')
moonlight_text_end = ('anne_negative', 'Aw, it\'s cloudy again. It was nice while it lasted...')  # noqa

lightning_color = 'black'
lightning_default_alpha = 120
lightning_duration = 20 * framerate
lightning_frame_count = 8
lightning_drop_rate = (255 - lightning_default_alpha) // lightning_frame_count
lightning_fade_in_s = 2
lightning_fade_in_f = lightning_fade_in_s * framerate
lightning_freq = 0.3
lightning_text = ('anne_negative', 'Oh no! It\'s starting to rain...')
lightning_text_end = ('anne_normal', 'Phew. I\'m glad that’s over.')
lightning_rain_fps = 4
lightning_rain_alpha = 80

effect_rate = 5 * framerate
lightning_effect_rate = 1 * framerate

music_fadeout_time_ms = 2000
music_fadein_time_ms = 100
music_death_fadeout_time_ms = 100

initial_position = tuple([int((x + 2 * map_buffer_size)
                              / 2 * map_tile_size)
                          for x in default_map_size])

msg_duration = framerate * 3
pickup_item_sprite_size = 32

default_game_state = {'current_game_mode': Modes.MAIN_MENU,
                      'active_message': 0,
                      'hp': 100,
                      'status': 'safe',
                      'unsafe_frame_count': 0,
                      'game_over': False,
                      'action': 'standing',
                      'inventory': {'candle': 5, 'firefly': 1, 'snail': 3},
                      'direction': 'forward',
                      'item': 'none',
                      'position': initial_position,
                      'effect': 'regular',
                      'effect_alpha': 120,
                      'effect_duration': 0,
                      'effect_check_counter': 0,
                      'effect_fade_in': False,
                      'effect_fade_out': False,
                      'moonlight_frame_count': 0,
                      'can_use_item': True,
                      'item_duration': 0,
                      'msg_duration': msg_duration,
                      'maze_begin': True,
                      'first_item_end': {'candle': True,
                                         'firefly': True,
                                         'snail': True,
                                         },
                      'last_item_picked_up': None,
                      'pickup': False,
                      'first_item_pickup': {'candle': True,
                                            'firefly': True,
                                            'snail': True,
                                            },
                      'snail_position': (0, 0),
                      'generate_map': True,
                      'active_sfx': set(),
                      'message_sfx_played': True,
                      }

restart_text = 'Press any key to restart'
advance_text = 'Press any key'
