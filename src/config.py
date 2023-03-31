import enum
import os
from pathlib import Path
from math import ceil


debug_mode = True

screen_size = (1080, 720)
screen_center = tuple(x // 2 for x in screen_size)

framerate = 60

character_speed = 2

fontname = 'Arial'
fontsize = 32
font_color = '#303030'

dialog_border_color = 'blue'
dialog_box_color = 'yellow'
menu_bg_color = 'yellow'

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

intro_messages = ['All I wanted was a nice picnic at my favorite spot.',
                  'Unfortunately for me, I wasn\'t the only one using it today.',  # noqa
                  'When I arrived at the spot and sat down, something poked at me!',  # noqa
                  'I had sat on a tiny angry fairy!',
                  'It was so upset it cast a spell on me and...',
                  'it transported me to the middle of the Shady Wood!',
                  'The Shady Wood is cursed.',
                  'Anyone who shows fear gets turned to stone and lost forever.',  # noqa
                  'I need to keep courage and find my way out!',
                  ]

maze_begin_message = 'It\'s a good thing I packed some candles. But I don\'t think they\'ll be enough...'  # noqa

items = ['firefly', 'candle', 'snail']
keys = {'firefly': 'f',
        'candle': 'c',
        'snail': 's',
        }

item_durations = {'candle': 15 * framerate,
                  'firefly': 15 * framerate,
                  'snail': 30 * framerate,
                  }
item_variances = {'candle': 13000,
                  'firefly': 9600,
                  'snail': 4800,
                  }
firefly_flash_frames_freq = 90
firefly_flash_frames = 4

item_end_messages = {'candle': 'Oh... It\'s all used up...',
                     'firefly': 'Oh... It flew away...',
                     'snail': 'The snail crawled away...',
                     }

first_item_messages = {'firefly': 'A firefly! That will help light my way! I can keep it in my jar.',  # noqa
                       'snail': 'A glowing snail! It should help me, but they have a mind of their own...',  # noqa
                       }

default_map_size = (11, 11)
map_tile_size = 384
map_buffer_size = ceil(max(screen_size) / map_tile_size)

boundary_safe_zone_color = '#15ff00'
boundary_unsafe_zone_color = '#0000ff'
boundary_dead_zone_color = '#ff0000'
boundary_win_zone_color = '#fff000'

game_win_text = ['I found a road! I can make it home safely now.',
                 'Thank you for your help!',
                 ]

game_over_text = ['GAME OVER',
                  'Anne became too afraid. She turned to stone...',
                  ]

game_over_fontname = 'Copperplate Gothic'
game_over_fontsize = 20
game_over_font_color = 'white'

moonlight_color = 'blue'
moonlight_default_alpha = 120
moonlight_duration = 15 * framerate
moonlight_drop_rate = (255 - moonlight_default_alpha) / moonlight_duration
moonlight_fade_in_s = 3
moonlight_fade_in_f = moonlight_fade_in_s * framerate
moonlight_text = 'The Moon came out. Now I can see my way!'
moonlight_text_end = 'Aw, it\'s cloudy again. It was nice while it lasted...'

lightning_color = 'black'
lightning_default_alpha = 120
lightning_duration = 15 * framerate
lightning_frame_count = 8
lightning_drop_rate = (255 - lightning_default_alpha) // lightning_frame_count
lightning_fade_in_s = 2
lightning_fade_in_f = lightning_fade_in_s * framerate
lightning_freq = 0.3
lightning_text = 'Oh no! It\'s starting to rain...'
lightning_text_end = 'Phew. I\'m glad that’s over.'

effect_rate = 1 * framerate

music_fadeout_time_ms = 2000
music_fadein_time_ms = 100


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
    INTRO = 2
    GAME_OVER = 3
    WIN_DIALOG = 4
