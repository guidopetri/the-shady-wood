import pygame
import config


class MainCharacter(object):
    def __init__(self, surface):
        self.surface = surface

        self.sprite = pygame.image.load(f'{config.gfx_path}/Base Sprite.png')
        _, _, self._size_x, self._size_y = self.sprite.get_rect()

        self._accel_x = 0
        self._accel_y = 0
        self._x = 120
        self._y = 120

    @property
    def location(self):
        return pygame.Rect(*self.position, *self.size)

    @property
    def size(self):
        return (self._size_x, self._size_y)

    @property
    def accel(self):
        return (self._accel_x, self._accel_y)

    def increase_accel(self, xy):
        self._accel_x += xy[0]
        self._accel_y += xy[1]

    def reset_accel(self):
        self._accel_x = 0
        self._accel_y = 0

    @property
    def position(self):
        return (self._x, self._y)

    def handle(self):
        self.move_character()
        self.next_animation_frame()

    def next_animation_frame(self):
        pass

    def keep_character_inbounds(self):
        self._x = max(min(self._x,
                          config.screen_size[0] - self._size_x),
                      0)
        self._y = max(min(self._y,
                          config.screen_size[1] - self._size_y),
                      0)

    def move_character(self):
        self._x += self._accel_x
        self._y += self._accel_y

        self.keep_character_inbounds()

    def render(self, mode):
        if mode == config.Modes.GAME:
            coords = (config.screen_size[0] // 2 - self._size_x // 2,
                      config.screen_size[1] // 2 - self._size_y // 2,
                      )
            self.surface.blit(self.sprite, coords)
