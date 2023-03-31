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
                               'waving': 4,
                               'firefly_out': 4,
                               'candle_out': 4,
                               'snail_out': 4,
                               }

        self.fps_map = {'none': 4,
                        'walking': 4,
                        'firefly': 4,
                        'candle': 4,
                        'snail': 4,
                        'dead': 1,
                        'waving': 4,
                        'firefly_out': 4,
                        'candle_out': 4,
                        'snail_out': 4,
                        }

        self._frames_per_sprite_map = {k: config.framerate // v
                                       for k, v in self.fps_map.items()
                                       }

        self.frame_counter = 0
        self.spritesheets = {}

        actions = ['walking',
                   'firefly',
                   'candle',
                   'waving',
                   'firefly_out',
                   'candle_out',
                   ]

        forward_only = ['waving',
                        'firefly_out',
                        'candle_out',
                        ]

        for action in actions:
            self.spritesheets[action] = {}
            for direction in ['back', 'forward', 'left', 'right']:
                # todo: load waving animations
                if action in forward_only and direction != 'forward':
                    # we only have forward waving/firefly out/candle out
                    continue
                file = f'anne_spritesheet_{action}_{direction}_2x2_128px.png'
                sprites = self.load_spritesheet(file,
                                                self.num_frames_map[action])
                self.spritesheets[action][direction] = sprites

        self.spritesheets['none'] = self.spritesheets['walking']
        self.spritesheets['snail'] = self.spritesheets['walking']
        self.spritesheets['snail_out'] = self.spritesheets['walking']
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

    def advance_frame(self, state, amount=1, loop=True):
        self.frame_counter += 1
        if self.current_action == 'standing':
            frames_per_sprite = 2 * self._frames_per_sprite
        elif self.current_action in ('walking', 'dead', 'waving', 'item_out'):
            frames_per_sprite = self._frames_per_sprite
        if self.frame_counter >= frames_per_sprite:
            self.current_frame += amount
            self.frame_counter = 0

        if loop:
            self.current_frame %= self.num_frames
        else:
            self.current_frame = min(self.num_frames - 1, self.current_frame)
            if self.current_frame == self.num_frames - 1 and self.current_action == 'item_out':  # noqa
                state['item'] = 'none'
                state['action'] = 'standing'
                # remove _out
                item = self.current_item[:-4]
                state['first_item_end'][item] = False

    def next_animation_frame(self, state):
        if self.current_action in ('walking', 'waving'):
            self.advance_frame(state, 1, loop=True)
        elif self.current_action == 'standing':
            self.advance_frame(state, 2, loop=True)
        elif self.current_item == 'snail_out':
            self.advance_frame(state, 2, loop=False)
        elif self.current_action in ('dead', 'item_out'):
            self.advance_frame(state, 1, loop=False)
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

        valid_modes = (config.Modes.GAME,
                       config.Modes.GAME_OVER,
                       config.Modes.WIN_DIALOG,
                       )

        if mode not in valid_modes:
            return

        self.current_sprites = (self.spritesheets.get(state['item'])
                                                 .get(state['direction'])
                                )

        self.update_item(state['item'])
        self.update_action(state['action'])
        self.next_animation_frame(state)

        self.surface.blit(self.sprite, self.coords)


class Snail(object):
    def __init__(self, surface):
        self.surface = surface
        self.path = None
        self._total_movement = 0
        self.path_done = True
        self.original_pos = None
        # start by default facing down
        self._direction = 'S'

        self.num_frames = 2
        self.fps = 2
        self._frames_per_sprite = config.framerate // self.fps

        self.frame_counter = 0
        self.spritesheets = {}

        dirs_mapper = {'up': 'N', 'down': 'S', 'right': 'E', 'left': 'W'}
        for direction in ['down', 'up', 'left', 'right']:
            file = f'Snail_spritesheet_{direction}_2x1_32px.png'
            sprites = self.load_spritesheet(file,
                                            self.num_frames)
            self.spritesheets[dirs_mapper[direction]] = sprites
        self.spritesheets[''] = self.spritesheets['S']

        self.current_frame = 0

        _, _, self._size_x, self._size_y = self.sprite.get_rect()

        self.coords = (0, 0)
        self.move_map = {'N': (0, -config.snail_speed),
                         'S': (0, config.snail_speed),
                         'W': (-config.snail_speed, 0),
                         'E': (config.snail_speed, 0),
                         }

    def load_spritesheet(self, file, num_frames):
        path = config.gfx_path / file
        sheet = pygame.image.load(path).convert_alpha()

        sprites = []
        width = 32
        height = 32

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

    def next_animation_frame(self, state):
        self.frame_counter += 1
        if self.frame_counter >= self._frames_per_sprite:
            self.current_frame += 1
            self.frame_counter = 0

        self.current_frame %= self.num_frames

    @property
    def current_sprites(self):
        return self.spritesheets[self.current_direction]

    @property
    def current_direction(self):
        return self._direction

    @property
    def total_movement(self):
        return self._total_movement

    @total_movement.setter
    def total_movement(self, value):
        self._total_movement = value
        self._total_movement %= config.map_tile_size

    def relative_player_movement(self, state):
        if self._direction == 'N':
            return self.original_pos[1] - state['position'][1]
        elif self._direction == 'S':
            return state['position'][1] - self.original_pos[1]
        elif self._direction == 'W':
            return self.original_pos[0] - state['position'][0]
        elif self._direction == 'E':
            return state['position'][0] - self.original_pos[0]

    def update_coords(self, state):
        if state['item'] == 'snail':
            if self.original_pos is None:
                self.original_pos = state['position']

            player_tile_h_adj = self.original_pos[0] // config.map_tile_size
            player_tile_v_adj = self.original_pos[1] // config.map_tile_size
            player_h_adj = self.original_pos[0] % config.map_tile_size
            player_v_adj = self.original_pos[1] % config.map_tile_size

            new_player_tile_h_adj = state['position'][0] // config.map_tile_size  # noqa
            new_player_tile_v_adj = state['position'][1] // config.map_tile_size  # noqa
            new_player_h_adj = state['position'][0] % config.map_tile_size
            new_player_v_adj = state['position'][1] % config.map_tile_size

            tile_diff_h = new_player_tile_h_adj - player_tile_h_adj
            tile_diff_v = new_player_tile_v_adj - player_tile_v_adj

            h_adjustment = state['snail_position'][0] % config.map_tile_size
            v_adjustment = state['snail_position'][1] % config.map_tile_size

            tile_h_adj = state['snail_position'][0] // config.map_tile_size
            tile_v_adj = state['snail_position'][1] // config.map_tile_size

            self.coords = (config.map_tile_size
                           * (tile_h_adj
                              - player_tile_h_adj
                              - tile_diff_h
                              + 0.5)
                           + config.screen_center[0]
                           + h_adjustment
                           - player_h_adj
                           - new_player_h_adj,
                           config.map_tile_size
                           * (tile_v_adj
                              - player_tile_v_adj
                              - tile_diff_v
                              + 0.5)
                           + config.screen_center[1]
                           + v_adjustment
                           - player_v_adj
                           - new_player_v_adj,
                           )
            if config.debug_mode:
                pass
                # print('og_it_adj: ', player_h_adj, player_v_adj)
                # print('it_adj: ', new_player_h_adj, new_player_v_adj)
                # print('og_tile_adj: ', player_tile_h_adj, player_tile_v_adj)
                # print('tile: ', tile_h_adj, tile_v_adj)
                # print(self.coords, state['position'])
            if not self.path_done:
                state['snail_position'] = tuple(
                    map(sum, zip(state['snail_position'], self.movement))
                    )

                self.total_movement += config.snail_speed
                self.path_done = self.total_movement == 0

            if self.path_done:
                self._direction = state['ai_map'][tile_v_adj][tile_h_adj]
                self.movement = self.move_map[self._direction]
                self.path_done = False
                self.total_movement = 0

        elif state['item'] == 'snail_out':
            state['snail_position'] = (0, 0)
            self.coords = (0, 0)
            self.original_pos = None

    @property
    def blit_coords(self):
        # center the sprite
        return (self.coords[0] - self.sprite.get_width() // 2,
                self.coords[1] - self.sprite.get_height() // 2,
                )

    def render(self, state):
        mode = state['current_game_mode']

        if mode != config.Modes.GAME:
            return

        self.update_coords(state)
        self.next_animation_frame(state)

        if state['item'] == 'snail':
            self.surface.blit(self.sprite, self.blit_coords)
