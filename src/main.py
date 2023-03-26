#! /usr/bin/env python3

import pygame
import config
import sys


class MainCharacter(object):
    def __init__(self):
        # self.image = pygame.image.load(f'{folder_root}/assets/gfx/')
        # self.location = self.image.get_rect()
        self._accel_x = 0
        self._accel_y = 0
        self._x = 120
        self._y = 120
        self._size_x = 10
        self._size_y = 10

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
        # self.next_animation_frame()

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

    def render(self):
        pass


def handle_events(character):
    keys_map = {pygame.K_UP: (0, -1),
                pygame.K_DOWN: (0, 1),
                pygame.K_LEFT: (-1, 0),
                pygame.K_RIGHT: (1, 0),
                }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in keys_map:
                character.increase_accel(keys_map[event.key])
        elif event.type == pygame.KEYUP:
            if event.key in keys_map:
                character.reset_accel()


class Background(object):
    def __init__(self, screen):
        self.screen = screen
        self.gfx_path = f"{folder_root}/assets/gfx"
        self.cross_bg = pygame.image.load(
            f"{self.gfx_path}/sample_cross_bg.bmp"
            )

    def render(self, mode):
        if mode == config.Modes.MAIN_MENU:
            pass
        elif mode == config.Modes.GAME:
            self.screen.blit(self.cross_bg, (0, 0))


if __name__ == '__main__':
    # TODO: fix folder root
    folder_root = '..'
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(config.screen_size)

    # character_loc = character_image.get_rect()
    character = MainCharacter()
    bg = Background(screen)

    while True:
        handle_events(character)
        bg.render(config.Modes.GAME)
        # screen.blit(character_image, character_loc)
        character.handle()
        pygame.draw.rect(screen, 'blue', character.location)
        pygame.display.flip()

        clock.tick(60)
