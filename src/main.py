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
        self._x = max(min(self._x, config.screen_size[0] - self._size_x), 0)
        self._y = max(min(self._y, config.screen_size[1] - self._size_y), 0)

    def move_character(self):
        self._x += self._accel_x
        self._y += self._accel_y

        self.keep_character_inbounds()


def handle_events(character):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                character.increase_accel((0, -1))
            elif event.key == pygame.K_DOWN:
                character.increase_accel((0, 1))
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                character.reset_accel()


if __name__ == '__main__':
    # TODO: fix folder root
    folder_root = '..'
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()

    screen = pygame.display.set_mode(config.screen_size)

    # character_loc = character_image.get_rect()
    character = MainCharacter()

    while True:
        handle_events(character)

        screen.fill('black')
        # screen.blit(character_image, character_loc)
        character.handle()
        pygame.draw.rect(screen, 'red', character.location)
        pygame.display.flip()
