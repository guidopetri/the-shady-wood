import pygame
import config


class MainCharacter(object):
    def __init__(self, surface):
        self.surface = surface

        self.num_frames = 4
        self.fps = 4
        self._frames_per_sprite = config.framerate // self.fps
        self.frame_counter = 0
        self.spritesheets = {}

        for action in ['walking', 'firefly']:
            self.spritesheets[action] = {}
            for direction in ['back', 'forward', 'left', 'right']:
                file = f'anne_spritesheet_{action}_{direction}_2x2_128px.png'
                sprites = self.load_spritesheet(file, self.num_frames)
                self.spritesheets[action][direction] = sprites

        self.spritesheets['standing'] = self.spritesheets['walking']
        # load dead sprite
        file = 'anne_spritesheet_gameover_2x2_3frames_128px.png'
        self.spritesheets['dead'] = {'forward': self.load_spritesheet(file,
                                                                      3),
                                     }

        # start by default facing forward
        self.current_sprites = self.spritesheets['standing']['forward']
        self.current_frame = 0

        _, _, self._size_x, self._size_y = self.sprite.get_rect()

        self.coords = (config.screen_size[0] // 2 - self._size_x // 2,
                       config.screen_size[1] // 2 - self._size_y // 2,
                       )

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

    def next_animation_frame(self, state):
        if state['action'] == 'walking':
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

        if mode in (config.Modes.MAIN_MENU, config.Modes.INTRO):
            return

        self.current_sprites = (self.spritesheets.get(state['action'])
                                                 .get(state['direction'])
                                )
        if mode == config.Modes.GAME_OVER:
            pass
            # print(state['action'], state['direction'], self.current_sprites)

        self.next_animation_frame(state)

        self.surface.blit(self.sprite, self.coords)
