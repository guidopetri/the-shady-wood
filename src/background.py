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

    def render(self, mode):
        self.surface.fill('black')
        if mode == config.Modes.MAIN_MENU:
            pass
        elif mode == config.Modes.GAME:
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

            # foreground with lighting effect
            foreground = pygame.Surface((self.surface.get_width(),
                                         self.surface.get_height(),
                                         ),
                                        flags=pygame.SRCALPHA,
                                        )

            foreground.fill('black')
            alphas = pygame.surfarray.pixels_alpha(foreground)

            midpoints = [config.screen_size[0] // 2,
                         config.screen_size[1] // 2]

            area_size = 400
            area_half = area_size // 2

            array = np.mgrid[:area_size, :area_size]
            array = array.transpose((1, 2, 0))
            rv = multivariate_normal(mean=area_half,
                                     cov=[[4000, 0], [0, 4000]])
            diffs = rv.pdf(array)
            normalized_diffs = diffs * 255 / diffs.max()

            # replace middle section of alphas with the diff'd amount
            alphas[midpoints[0] - area_half: midpoints[0] + area_half,
                   midpoints[1] - area_half: midpoints[1] + area_half] = alphas[midpoints[0] - area_half: midpoints[0] + area_half,  # noqa
                                                                                midpoints[1] - area_half: midpoints[1] + area_half] - normalized_diffs  # noqa
            del alphas
            self.surface.blit(foreground, (0, 0))

    def move(self, amount):
        self._position_x += amount[0]
        self._position_x %= self.cross_bg.get_width()
        self._position_y += amount[1]
        self._position_y %= self.cross_bg.get_height()
