import pygame
import config
from scipy.stats import multivariate_normal
import numpy as np
from abc import ABC
from functools import partial
from math import ceil


class AbstractBG(ABC):
    def __init__(self, surface):
        self.surface = surface
        self._position_x = config.screen_size[0] // 2
        self._position_y = config.screen_size[1] // 2

        self.load_images()
        self.calc_num_tiles_in_screen()

    def load_images(self):
        raw_imgs = {}

        for tile in ['Blank', 'Corner', 'Cross', 'DeadEnd', 'Straight', 'T']:
            filename = f"BG_Maze_{self.image_type}_{tile}_384px.png"
            path = config.gfx_path / filename
            raw_imgs[tile] = pygame.image.load(path).convert_alpha()

        rot_90 = partial(pygame.transform.rotate, angle=90)
        rot_180 = partial(pygame.transform.rotate, angle=180)
        rot_270 = partial(pygame.transform.rotate, angle=270)

        self.images = {'cross': raw_imgs['Cross'],
                       't_up': rot_180(raw_imgs['T']),
                       't_down': raw_imgs['T'],
                       't_right': rot_90(raw_imgs['T']),
                       't_left': rot_270(raw_imgs['T']),
                       'straight_horizontal': rot_90(raw_imgs['Straight']),
                       'straight_vertical': raw_imgs['Straight'],
                       'corner_topleft': rot_180(raw_imgs['Corner']),
                       'corner_topright': rot_90(raw_imgs['Corner']),
                       'corner_botleft': rot_270(raw_imgs['Corner']),
                       'corner_botright': raw_imgs['Corner'],
                       'deadend_left': rot_270(raw_imgs['DeadEnd']),
                       'deadend_right': rot_90(raw_imgs['DeadEnd']),
                       'deadend_up': rot_180(raw_imgs['DeadEnd']),
                       'deadend_down': raw_imgs['DeadEnd'],
                       'blank': raw_imgs['Blank'],
                       }

    @property
    def position(self):
        return (self._position_x, self._position_y)

    def render(self, state):
        mode = state['current_game_mode']

        fns = {config.Modes.MAIN_MENU: self.render_main_menu,
               config.Modes.GAME: self.render_game,
               config.Modes.INTRO: self.render_intro_dialog,
               }

        fns[mode](state)

    def render_intro_dialog(self, state):
        pass

    def render_main_menu(self, state):
        pass

    def calc_num_tiles_in_screen(self):
        self.h_tiles = ceil(config.screen_size[0]
                            / (2 * config.map_tile_size)
                            )
        self.v_tiles = ceil(config.screen_size[1]
                            / (2 * config.map_tile_size)
                            )

    def render_game(self, state):
        for y in range(-self.v_tiles, self.v_tiles + 1):
            for x in range(-self.h_tiles, self.h_tiles + 1):
                h_adjustment = state['position'][0] % config.map_tile_size
                v_adjustment = state['position'][1] % config.map_tile_size

                tile_h_adj = state['position'][0] // config.map_tile_size
                tile_v_adj = state['position'][1] // config.map_tile_size

                pos = (int(config.map_tile_size * (x + 0.5)
                           + config.screen_center[0]
                           - h_adjustment),
                       int(config.map_tile_size * (y + 0.5)
                           + config.screen_center[1]
                           - v_adjustment),
                       )
                if config.debug_mode and (x, y) == (2, 0):
                    print(x + tile_h_adj, y + tile_v_adj)
                    pygame.draw.rect(self.surface,
                                     'red',
                                     pygame.Rect(*pos, 10, 10)
                                     )
                    # print(pos)

                try:
                    tile = state['map'][y + tile_v_adj][x + tile_h_adj]  # noqa
                except IndexError:
                    tile = 'blank'
                rect = self.images[tile].get_rect(center=pos)
                self.surface.blit(self.images[tile], rect)

    def move(self, amount):
        self._position_x += amount[0]
        self._position_x %= self.cross.get_width()
        self._position_y += amount[1]
        self._position_y %= self.cross.get_height()


class Background(AbstractBG):
    def __init__(self, surface):
        self.image_type = 'Ground'

        super().__init__(surface)

    def render_intro_dialog(self, state):
        self.surface.fill('black')

    def render_main_menu(self, state):
        self.surface.fill('black')

        dims = [int(dim * 0.8) for dim in config.screen_size]
        menu_surface = pygame.Surface(dims)
        menu_surface.fill(config.menu_bg_color)
        menu_rect = menu_surface.get_rect(center=config.screen_center)

        self.surface.blit(menu_surface, menu_rect)


class Foreground(AbstractBG):
    def __init__(self, surface):
        self.image_type = 'Tree'

        super().__init__(surface)


class Boundaries(AbstractBG):
    def __init__(self, surface):
        self.image_type = 'Boundary'

        super().__init__(surface)


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
