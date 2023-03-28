import pygame
import config
from scipy.stats import multivariate_normal
import numpy as np


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

    def render(self, state):
        mode = state['current_game_mode']

        fns = {config.Modes.MAIN_MENU: self.render_main_menu,
               config.Modes.GAME: self.render_game,
               config.Modes.INTRO: self.render_intro_dialog,
               }

        fns[mode]()

    def render_intro_dialog(self):
        self.surface.fill('black')

    def render_main_menu(self):
        self.surface.fill('black')

        dims = [int(dim * 0.8) for dim in config.screen_size]
        menu_surface = pygame.Surface(dims)
        menu_surface.fill(config.menu_bg_color)
        menu_rect = menu_surface.get_rect(center=config.screen_center)

        self.surface.blit(menu_surface, menu_rect)

    def render_game(self):
        self.surface.fill('black')
        self.surface.blit(self.cross_bg, self.position)

        # to the left
        self.surface.blit(self.cross_bg,
                          (self._position_x
                           - self.cross_bg.get_width()
                           + config.img_buffer,
                           self._position_y)
                          )
        # to the top
        self.surface.blit(self.cross_bg,
                          (self._position_x,
                           self._position_y
                           - self.cross_bg.get_height()
                           + config.img_buffer)
                          )

        # diagonal
        self.surface.blit(self.cross_bg,
                          (self._position_x
                           - self.cross_bg.get_width()
                           + config.img_buffer,
                           self._position_y
                           - self.cross_bg.get_height()
                           + config.img_buffer)
                          )

    def move(self, amount):
        self._position_x += amount[0]
        self._position_x %= self.cross_bg.get_width()
        self._position_y += amount[1]
        self._position_y %= self.cross_bg.get_height()


class Shadows(object):
    def __init__(self, surface, area, variance):
        self.surface = surface
        self.area = area
        self.variance = variance
        self.shadows = None
        self.redo_render = True

    def render_shadows(self):
        # foreground with lighting effect
        shadow = pygame.Surface((self.surface.get_width(),
                                 self.surface.get_height(),
                                 ),
                                flags=pygame.SRCALPHA,
                                )

        shadow.fill('black')
        alphas = pygame.surfarray.pixels_alpha(shadow)

        midpoints = [config.screen_size[0] // 2,
                     config.screen_size[1] // 2]

        area_half = self.area // 2

        array = np.mgrid[:self.area, :self.area]
        array = array.transpose((1, 2, 0))
        rv = multivariate_normal(mean=[area_half, area_half],
                                 cov=[[self.variance, 0], [0, self.variance]])
        diffs = rv.pdf(array)
        normalized_diffs = diffs * alphas.max() / diffs.max()

        x_start = midpoints[0] - area_half
        x_end = midpoints[0] + area_half
        y_start = midpoints[1] - area_half
        y_end = midpoints[1] + area_half
        # replace middle section of alphas with the diff'd amount
        alphas[x_start: x_end,
               y_start: y_end] = alphas[x_start: x_end,
                                        y_start: y_end] - normalized_diffs

        self.redo_render = False

        return shadow

    def render(self, state):
        mode = state['current_game_mode']

        if self.redo_render or self.shadows is None:
            self.shadows = self.render_shadows()

        if mode == config.Modes.GAME:
            self.surface.blit(self.shadows, (0, 0))
