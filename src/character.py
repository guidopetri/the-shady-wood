import pygame
import config


class MainCharacter(object):
    def __init__(self, surface):
        self.surface = surface

        self.sprite = pygame.image.load(f'{config.gfx_path}/Base Sprite.png')
        _, _, self._size_x, self._size_y = self.sprite.get_rect()

    @property
    def size(self):
        return (self._size_x, self._size_y)

    def handle(self):
        self.next_animation_frame()

    def next_animation_frame(self):
        pass

    def render(self, mode):
        if mode == config.Modes.GAME:
            coords = (config.screen_size[0] // 2 - self._size_x // 2,
                      config.screen_size[1] // 2 - self._size_y // 2,
                      )
            self.surface.blit(self.sprite, coords)
