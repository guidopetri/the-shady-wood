#! /usr/bin/env python3

import pygame
import config
import sys


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


def handle_events(bg, character):
    keys_map = {pygame.K_UP: (0, config.character_speed),
                pygame.K_DOWN: (0, -config.character_speed),
                pygame.K_LEFT: (config.character_speed, 0),
                pygame.K_RIGHT: (-config.character_speed, 0),
                }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    keys = pygame.key.get_pressed()

    for key, movement in keys_map.items():
        if keys[key]:
            print(f"moving {movement}")
            bg.move(movement)


class Background(object):
    def __init__(self, surface):
        self.surface = surface
        self.cross_bg = pygame.image.load(
            f"{config.gfx_path}/sample_cross_bg.bmp"
            )

        self._position_x = 0
        self._position_y = 0

    @property
    def position(self):
        return (self._position_x, self._position_y)

    def render(self, mode):
        surface.fill('black')
        if mode == config.Modes.MAIN_MENU:
            pass
        elif mode == config.Modes.GAME:
            self.surface.blit(self.cross_bg, self.position)

    def move(self, amount):
        self._position_x += amount[0]
        self._position_y += amount[1]


class Dialog(object):
    def __init__(self, surface):
        self.surface = surface
        self.messages = ['lorem ipsum',
                         'dolor sit amet',
                         'Oh no! I\'m lost in the woods...',
                         ]
        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(30, 30, 30)

    @property
    def position(self):
        return (10, 10)

    @property
    def size(self):
        return (100, 100)

    def render_box_bg(self, width, height, position):
        # create filled in rect for border
        border = pygame.Surface((width + 20, height + 10))
        border.fill(config.dialog_border_color)
        border_rect = border.get_rect(**position)

        # create bg to overlay on border
        bg = pygame.Surface((border_rect.width - 10, border_rect.height - 10))
        bg.fill(config.dialog_box_color)
        bg_rect = bg.get_rect(midtop=(border_rect.width / 2, 5))

        # blit bg onto border to achieve a border effect
        border.blit(bg, bg_rect)

        # blit the result onto screen
        self.surface.blit(border, border_rect)

    def render_text(self, text, position):
        render = self.font.render(text, True, self.font_color)
        rect = render.get_rect(**position)
        return render, rect

    def blit_text(self, text, rect):
        self.surface.blit(text, rect)

    def render(self, mode):
        if True:
            position = {'midtop': (config.screen_size[0] // 2,
                                   3 * config.screen_size[1] // 4),
                        }
            text, rect = self.render_text(self.messages[2], position)
            self.render_box_bg(rect.width, rect.height, position)
            self.blit_text(text, rect)


if __name__ == '__main__':
    # pygame.display.init()
    # pygame.font.init()
    # pygame.mixer.init()
    pygame.init()
    clock = pygame.time.Clock()

    surface = pygame.display.set_mode(config.screen_size)

    character = MainCharacter(surface)
    bg = Background(surface)
    dialog = Dialog(surface)

    while True:
        handle_events(bg, character)
        character.handle()

        bg.render(config.Modes.GAME)
        character.render(config.Modes.GAME)
        dialog.render(config.Modes.GAME)

        pygame.display.flip()

        clock.tick(60)
