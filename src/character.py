import pygame
import config


class MainCharacter(object):
    def __init__(self, surface):
        self.surface = surface

        self.num_frames = 4
        self.fps = 5
        self._frames_per_sprite = config.framerate // self.fps
        self.frame_counter = 0
        self.spritesheets = {}

        for direction in ['back', 'forward', 'left', 'right']:
            filename = f'anne_spritesheet_walking_{direction}_2x2_128px.png'
            path = config.gfx_path / filename
            sheet = pygame.image.load(path).convert_alpha()

            sprites = []
            width = 128
            height = 128

            coords = [(0, 0),
                      (width, 0),
                      (0, height),
                      (width, height),
                      ]

            for idx in range(self.num_frames):
                sprite_area = pygame.Rect(*coords[idx], width, height)
                sprites.append(sheet.subsurface(sprite_area))

            self.spritesheets[direction] = sprites

        # start by default facing forward
        self.current_sprites = self.spritesheets['forward']
        self.current_frame = 0

        _, _, self._size_x, self._size_y = self.sprite.get_rect()

        self.coords = (config.screen_size[0] // 2 - self._size_x // 2,
                       config.screen_size[1] // 2 - self._size_y // 2,
                       )

    @property
    def sprite(self):
        return self.current_sprites[self.current_frame]

    @property
    def size(self):
        return (self._size_x, self._size_y)

    def next_animation_frame(self, walking):
        if walking:
            self.frame_counter += 1
            if self.frame_counter == self._frames_per_sprite:
                self.current_frame += 1
                self.frame_counter = 0
        else:
            self.current_frame = 0
            self.frame_counter = 0

        self.current_frame %= self.num_frames

    def render(self, state):
        mode = state['current_game_mode']

        if mode != config.Modes.GAME:
            return

        self.current_sprites = self.spritesheets[state['direction']]

        self.next_animation_frame(state['walking'])

        self.surface.blit(self.sprite, self.coords)
