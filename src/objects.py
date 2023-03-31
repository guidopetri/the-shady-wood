import pygame
import config


class Objects(object):
    def __init__(self, surface):
        self.surface = surface
        self._current_frame = 0
        self._frame_counter = 0

        self.load_images()

    def load_images(self):
        self.num_frames = 2
        self.fps = 2
        self._frames_per_sprite = config.framerate / self.fps

        file = 'Snail_spritesheet_left_2x1_32px.png'
        self.snail = self.load_spritesheet(file, self.num_frames)

        file = 'firefly_spritesheet_2x1_15px.png'
        self.firefly = self.load_spritesheet(file, self.num_frames)

        self.width = self.snail[0].get_width()
        self.height = self.snail[0].get_height()

        self.sprites_map = {'firefly': self.firefly, 'snail': self.snail}

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

    def render_item(self, state, item, x, y):
        tile_h_adj = x
        tile_v_adj = y

        player_tile_h_adj = state['position'][0] // config.map_tile_size
        player_tile_v_adj = state['position'][1] // config.map_tile_size
        player_h_adj = state['position'][0] % config.map_tile_size
        player_v_adj = state['position'][1] % config.map_tile_size

        item_coords = (config.map_tile_size
                       * (tile_h_adj
                          - player_tile_h_adj
                          + 0.5)
                       + config.screen_center[0]
                       - player_h_adj
                       - self.width // 2,
                       config.map_tile_size
                       * (tile_v_adj
                          - player_tile_v_adj
                          + 0.5)
                       + config.screen_center[1]
                       - player_v_adj
                       - self.height // 2,
                       )

        sprite = self.sprites_map[item][self.current_frame]

        item_outside_x = (item_coords[0] < -self.width
                          or item_coords[0] > (config.screen_size[0]
                                               + self.width))

        item_outside_y = (item_coords[1] < -self.height
                          or item_coords[1] > (config.screen_size[1]
                                               + self.height))
        if item_outside_x and item_outside_y:
            return
        self.surface.blit(sprite, item_coords)

    @property
    def current_frame(self):
        return self._current_frame

    @current_frame.setter
    def current_frame(self, value):
        self._current_frame = value
        self._current_frame %= self.num_frames

    @property
    def frame_counter(self):
        return self._frame_counter

    @frame_counter.setter
    def frame_counter(self, value):
        self._frame_counter = value
        if self._frame_counter >= self._frames_per_sprite:
            self.current_frame += 1
            self._frame_counter = 0

    def render(self, state):
        if state['current_game_mode'] != config.Modes.GAME:
            return

        # use state to render objects
        for y, row in enumerate(state['item_map']):
            for x, item in enumerate(row):
                if item == ' ':
                    continue
                self.render_item(state, item, x, y)
        self.frame_counter += 1
