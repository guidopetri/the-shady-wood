import pygame
import config


class MainCharacter(object):
    def __init__(self, surface):
        self.surface = surface
        self.current_action = 'standing'
        self.current_item = 'none'

        self.num_frames_map = {'none': 4,
                               'walking': 4,
                               'firefly': 4,
                               'candle': 4,
                               'snail': 4,
                               'dead': 3,
                               }

        self.fps_map = {'none': 4,
                        'walking': 4,
                        'firefly': 4,
                        'candle': 4,
                        'snail': 4,
                        'dead': 1,
                        }

        self._frames_per_sprite_map = {k: config.framerate // v
                                       for k, v in self.fps_map.items()
                                       }

        self.frame_counter = 0
        self.spritesheets = {}

        for action in ['walking', 'firefly', 'candle']:
            self.spritesheets[action] = {}
            for direction in ['back', 'forward', 'left', 'right']:
                file = f'anne_spritesheet_{action}_{direction}_2x2_128px.png'
                sprites = self.load_spritesheet(file,
                                                self.num_frames_map[action])
                self.spritesheets[action][direction] = sprites

        self.spritesheets['none'] = self.spritesheets['walking']
        self.spritesheets['snail'] = self.spritesheets['walking']
        # load dead sprite
        file = 'anne_spritesheet_gameover_2x2_3frames_128px.png'
        self.spritesheets['dead'] = {'forward': self.load_spritesheet(file,
                                                                      3),
                                     }

        # start by default facing forward
        self.current_sprites = self.spritesheets['none']['forward']
        self.current_frame = 0

        _, _, self._size_x, self._size_y = self.sprite.get_rect()

        self.coords = (config.screen_size[0] // 2 - self._size_x // 2,
                       config.screen_size[1] // 2 - self._size_y // 2,
                       )

    @property
    def num_frames(self):
        return self.num_frames_map[self.current_item]

    @property
    def fps(self):
        return self.fps_map[self.current_item]

    @property
    def _frames_per_sprite(self):
        return self._frames_per_sprite_map[self.current_item]

    def load_spritesheet(self, file, num_frames):
        path = config.gfx_path / file
        sheet = pygame.image.load(path).convert_alpha()

        sprites = []
        width = 128
        height = 128

        coords = [(0, 0),
                  (width, 0),
                  (0, height),
                  (width, height),
                  ]

        for idx in range(num_frames):
            sprite_area = pygame.Rect(*coords[idx], width, height)
            sprites.append(sheet.subsurface(sprite_area))
        return sprites

    @property
    def sprite(self):
        return self.current_sprites[self.current_frame]

    @property
    def size(self):
        return (self._size_x, self._size_y)

    def advance_frame(self, amount=1, loop=True):
        self.frame_counter += 1
        if self.current_action == 'standing':
            frames_per_sprite = 2 * self._frames_per_sprite
        elif self.current_action in ('walking', 'dead'):
            frames_per_sprite = self._frames_per_sprite
        if self.frame_counter >= frames_per_sprite:
            self.current_frame += amount
            self.frame_counter = 0

        if loop:
            self.current_frame %= self.num_frames
        else:
            self.current_frame = min(self.num_frames - 1, self.current_frame)

    def next_animation_frame(self):
        if self.current_action == 'walking':
            self.advance_frame(1, loop=True)
        elif self.current_action == 'standing':
            self.advance_frame(2, loop=True)
        elif self.current_action == 'dead':
            self.advance_frame(1, loop=False)
        else:
            self.current_frame = 0
            self.frame_counter = 0

    def update_action(self, action):
        if action != self.current_action:
            self.current_action = action
            self.current_frame = 0

    def update_item(self, item):
        if item != self.current_item:
            self.current_item = item
            self.current_frame = 0

    def render(self, state):
        mode = state['current_game_mode']

        if mode not in (config.Modes.GAME, config.Modes.GAME_OVER):
            return

        self.current_sprites = (self.spritesheets.get(state['item'])
                                                 .get(state['direction'])
                                )

        self.update_item(state['item'])
        self.update_action(state['action'])
        self.next_animation_frame()

        self.surface.blit(self.sprite, self.coords)
