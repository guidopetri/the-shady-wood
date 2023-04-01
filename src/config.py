import enum
import os
from pathlib import Path
from math import ceil
import sys


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
    INTRO = 2
    GAME_OVER = 3
    WIN_DIALOG = 4


debug_mode = False
version_text = 'v1.1.0'
version_color = '#444444'
version_text_padding = (-10, -10)

# pyinstaller shenanigans
if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    root = Path(sys._MEIPASS)
else:
    main_dir = Path(os.path.split(os.path.abspath(__file__))[0])
    root = main_dir / '..'

gfx_path = root / 'assets' / 'gfx'
sfx_path = root / 'assets' / 'fx'

screen_size = (1080, 720)
screen_center = tuple(x // 2 for x in screen_size)

window_title = 'The Shady Wood'

framerate = 60

character_speed = 2
snail_speed = 6

fontpath = root / 'assets' / 'font'
fontname = fontpath / 'OTF' / 'dogicapixel.otf'
fontsize = 16
font_color = 'white'

text_padding = (0, 3)

main_menu_bg_color = '#141414'
main_menu_text = 'Press any key to start'
menu_text_padding = (0, 0)
menu_sprite_padding = (0, 110)
title_padding = (0, 80)

courage_fontsize = 10
courage_font_color = 'black'
courage_text_padding = (0, 4)
courage_text = 'COURAGE'

hp_bar_border_radius = 3
full_hp_color = '#00aa00'
empty_hp_color = '#cc0000'
hp_bar_bg_color = '#222222'
hp_indicator_size = (150,  # ~ 1080 / 8 + 10%
                     40,  # ~ 720 / 20 + 10%
                     )
hp_bar_border_thickness = 1
hp_bar_padding = (0, 4)

item_fontsize = 10
item_icon_size = 48
item_padding = 11
item_bar_size = (3 * item_icon_size + 4 * item_padding,
                 item_icon_size + 2 * item_padding,
                 )
item_font_color = 'black'
item_count_padding = (-3, 8)
item_key_padding = (0, 1)
item_letter_padding = (0, -1)

img_buffer = 2

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
                   'Anyone who shows fear gets turned to stone and is lost forever.'),  # noqa
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
firefly_flashes = 10
firefly_flash_frames = framerate // 2
item_durations = {'candle': 30 * framerate,
                  'firefly': int((firefly_duration_in_s * firefly_flashes
                                  + firefly_flash_frames / framerate)
                                 * framerate),
                  'snail': 3 * framerate,
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

game_over_fontsize = 16
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
cant_use_item_text = ('anne_negative', 'I can\'t use that right now.')
cant_use_item_duration = 3 * framerate

lightning_effect_rate = 1 * framerate

music_fadeout_time_ms = 2000
music_fadein_time_ms = 100
music_death_fadeout_time_ms = 100
# warning: includes magic numbers
music_delay_frames = {Modes.WIN_DIALOG: int(0.375
                                            * map_tile_size
                                            / character_speed),
                      Modes.MAIN_MENU: 0.1 * framerate,
                      }

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
                      'inventory': {'candle': 5, 'firefly': 0, 'snail': 0},
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
                      'tried_to_use_item': False,
                      'menu_ready': False,
                      'fading_in_logo': True,
                      'hold_logo': False,
                      'fading_out_logo': False,
                      'fading_in_credits': False,
                      'hold_credits': False,
                      'fading_out_credits': False,
                      'fading_in_anne': False,
                      'fading_in_title': False,
                      'hold_at_menu': False,
                      'ready_for_win': False,
                      'ready_for_restart': False,
                      }

fadein_credits_text = 'Created by Kendra Lemon and Guido Petri'
fadein_credits_text_padding = (0, 0)

logo_fadein_period = 2 * framerate
logo_hold_period = 1 * framerate
logo_fadeout_period = 2 * framerate

credits_fadein_period = 2 * framerate
credits_hold_period = 1 * framerate
credits_fadeout_period = 2 * framerate

anne_fadein_period = 2 * framerate
title_fadein_period = 2 * framerate
ready_hold_period = 1 * framerate

restart_text = 'Press any key to restart'
advance_text = 'Press any key to continue'
advance_fontsize = 14
advance_color = 'gray'
advance_padding = (-32, 0)

credits_text = 'A game by Lemon Pepper Wings'
credits_fontsize = 12
credits_font_color = 'gray'
credits_padding = (0, 22)
