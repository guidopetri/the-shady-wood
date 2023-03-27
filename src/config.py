import enum
import os
from pathlib import Path


screen_size = (1080, 720)
screen_center = tuple(x // 2 for x in screen_size)

character_speed = 4

fontname = 'Arial'
fontsize = 32
font_color = '#303030'

dialog_border_color = 'blue'
dialog_box_color = 'yellow'
menu_bg_color = 'yellow'

img_buffer = 2

# TODO: fix folder root
main_dir = Path(os.path.split(os.path.abspath(__file__))[0])
root = main_dir / '..'
gfx_path = str(root / 'assets' / 'gfx')
sfx_path = str(root / 'assets' / 'fx')

intro_messages = ['lorem ipsum',
                  'dolor sit amet',
                  'Oh no! I\'m lost in the woods...',
                  ]


class Modes(enum.Enum):

    MAIN_MENU = 0
    GAME = 1
    INTRO = 2
