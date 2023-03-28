import enum
import os
from pathlib import Path


screen_size = (1080, 720)
screen_center = tuple(x // 2 for x in screen_size)

framerate = 60

character_speed = 4

fontname = 'Arial'
fontsize = 32
font_color = '#303030'

dialog_border_color = 'blue'
dialog_box_color = 'yellow'
menu_bg_color = 'yellow'

courage_fontname = 'Copperplate Gothic'
courage_fontsize = 14
courage_font_color = '#808080'

hp_bar_border_radius = 3
full_hp_color = '#00aa00'
empty_hp_color = '#cc0000'
hp_bar_bg_color = '#222222'
hp_indicator_size = (150,  # ~ 1080 / 8 + 10%
                     40,  # ~ 720 / 20 + 10%
                     )

img_buffer = 2

main_dir = Path(os.path.split(os.path.abspath(__file__))[0])
root = main_dir / '..'
gfx_path = root / 'assets' / 'gfx'
sfx_path = root / 'assets' / 'fx'

intro_messages = ['lorem ipsum',
                  'dolor sit amet',
                  'Oh no! I\'m lost in the woods...',
                  ]


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
    INTRO = 2
