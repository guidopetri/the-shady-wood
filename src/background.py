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

        tile_names = ['Blank',
                      'Corner',
                      'Cross',
                      'DeadEnd',
                      'Straight',
                      'T',
                      'MazeEnd',
                      ]

        for tile in tile_names:
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
                       'mazeend_left': rot_270(raw_imgs['MazeEnd']),
                       'mazeend_right': rot_90(raw_imgs['MazeEnd']),
                       'mazeend_up': rot_180(raw_imgs['MazeEnd']),
                       'mazeend_down': raw_imgs['MazeEnd'],
                       }

    @property
    def position(self):
        return (self._position_x, self._position_y)

    def render(self, state):
        mode = state['current_game_mode']

        fns = {config.Modes.MAIN_MENU: self.render_main_menu,
               config.Modes.GAME: self.render_game,
               config.Modes.INTRO: self.render_intro_dialog,
               config.Modes.GAME_OVER: self.render_game_over,
               config.Modes.WIN_DIALOG: self.render_win_dialog,
               }

        fns[mode](state)

    def render_win_dialog(self, *args):
        pass

    def render_game_over(self, *args):
        pass

    def render_intro_dialog(self, *args):
        pass

    def render_main_menu(self, *args):
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
                if config.debug_mode and (x, y) == (0, 0):
                    # current tile
                    # print(x + tile_h_adj, y + tile_v_adj)

                    # where center tile will be plotted
                    # print(pos)
                    pygame.draw.rect(self.surface,
                                     'red',
                                     pygame.Rect(*pos, 10, 10)
                                     )

                    # h/v adjustment for player position
                    # also location within current tile
                    # print(h_adjustment, v_adjustment)
                    pygame.draw.rect(self.surface,
                                     'magenta',
                                     pygame.Rect(h_adjustment,
                                                 v_adjustment,
                                                 5,
                                                 5,
                                                 ))

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

        self.font = pygame.font.SysFont(config.game_over_fontname,
                                        config.game_over_fontsize,
                                        )
        self.font_color = pygame.Color(config.game_over_font_color)

        super().__init__(surface)

    def render_game_over(self, *args):
        text = config.game_over_text

        coords = {'center': (config.screen_center[0],
                             config.screen_center[1] - 128,
                             )
                  }
        game_over_text = self.font.render(text[0], True, self.font_color)
        game_over_rect = game_over_text.get_rect(**coords)

        coords = {'center': (config.screen_center[0],
                             config.screen_center[1] + 128,
                             )
                  }
        stone_text = self.font.render(text[1], True, self.font_color)
        stone_rect = stone_text.get_rect(**coords)

        self.surface.blit(game_over_text, game_over_rect)
        self.surface.blit(stone_text, stone_rect)

    def render_intro_dialog(self, *args):
        self.surface.fill('black')

    def render_main_menu(self, *args):
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

        safe = tuple(pygame.Color(config.boundary_safe_zone_color))
        unsafe = tuple(pygame.Color(config.boundary_unsafe_zone_color))
        dead = tuple(pygame.Color(config.boundary_dead_zone_color))
        win = tuple(pygame.Color(config.boundary_win_zone_color))

        self.boundary_status_mapping = {safe: 'safe',
                                        unsafe: 'unsafe',
                                        dead: 'dead',
                                        win: 'win',
                                        }

        super().__init__(surface)

    def check_for_dmg(self, state):
        if state['current_game_mode'] != config.Modes.GAME:
            return
        if config.debug_mode:
            pass
            # super().render_game(state)

        tile_h_adj = state['position'][0] // config.map_tile_size
        tile_v_adj = state['position'][1] // config.map_tile_size

        center_tile = state['map'][tile_v_adj][tile_h_adj]

        h_adjustment = state['position'][0] % config.map_tile_size
        v_adjustment = state['position'][1] % config.map_tile_size
        xy = (h_adjustment, v_adjustment)
        boundary_color = tuple(self.images[center_tile].get_at(xy))

        state['status'] = self.boundary_status_mapping[boundary_color]

        if config.debug_mode:
            pass
            # print(state['status'])


class Shadows(object):
    def __init__(self, surface, area, variance):
        self.surface = surface
        self.area = area
        self.variance = variance
        self.shadows = None
        self.redo_render = True

    def render_shadows(self, color, default_alpha):
        # foreground with lighting effect
        shadow = pygame.Surface((self.surface.get_width(),
                                 self.surface.get_height(),
                                 ),
                                flags=pygame.SRCALPHA,
                                )

        shadow.fill(color)
        shadow.set_alpha(default_alpha)
        alphas = pygame.surfarray.pixels_alpha(shadow)

        midpoints = [config.screen_size[0] // 2,
                     config.screen_size[1] // 2]

        array = np.mgrid[:self.area * 2, :self.area * 2]
        array = array.transpose((1, 2, 0))
        rv = multivariate_normal(mean=[self.area, self.area],
                                 cov=[[self.variance, 0], [0, self.variance]])
        diffs = rv.pdf(array)
        normalized_diffs = diffs * alphas.max() / diffs.max()

        x_start = midpoints[0] - self.area
        x_end = midpoints[0] + self.area
        y_start = midpoints[1] - self.area
        y_end = midpoints[1] + self.area
        # replace middle section of alphas with the diff'd amount
        alphas[x_start: x_end,
               y_start: y_end] = alphas[x_start: x_end,
                                        y_start: y_end] - normalized_diffs

        self.redo_render = False

        return shadow

    def render(self, state):
        mode = state['current_game_mode']

        if self.redo_render or self.shadows is None:
            self.shadows = self.render_shadows('black', 255)

        if mode == config.Modes.GAME:
            if (state['effect'] == 'regular' or
                (state['effect'] == 'lightning'
                    and state['effect_fade_in'])):
                self.surface.blit(self.shadows, (0, 0))


class LightStatusEffects(Shadows):
    def __init__(self, surface):
        self.initial_area = 180
        self.initial_variance = 48000
        self.final_area = 50
        self.final_variance = 3

        moon_num_frames = 2
        filename = 'Moonlight_Rays_2x1_384px.png'

        self.moonlight_tiles = self.load_spritesheet(moon_num_frames,
                                                     filename,
                                                     384,
                                                     384,
                                                     )

        rain_num_frames = 4
        filename = 'Lightning_Rain_Spritesheet_2x2_128px.png'

        self.rain_tiles = self.load_spritesheet(rain_num_frames,
                                                filename,
                                                128,
                                                128,
                                                )

        super().__init__(surface,
                         area=self.initial_area,
                         variance=2400,
                         )
        self.shadows = self.render_shadows('black', 255)
        self.reset_to_defaults()

    def load_spritesheet(self, num_frames, file, width, height):
        path = config.gfx_path / file
        sheet = pygame.image.load(path).convert_alpha()

        sprites = []

        coords = [(0, 0),
                  (width, 0),
                  (0, height),
                  (width, height),
                  ]

        for idx in range(num_frames):
            sprite_area = pygame.Rect(*coords[idx], width, height)
            sprites.append(sheet.subsurface(sprite_area))
        return sprites

    def reset_to_defaults(self):
        self.fade_in_frame = 0
        self.filt = None
        self.area = self.initial_area
        self.variance = self.initial_variance
        self.effect_is_fading_in = False
        self.current_frame = 0
        self.moonlight_alpha = 0
        self.moonlight_up = True

    def render_filter(self, color, alpha):
        if self.effect_is_fading_in:
            self.filt = self.render_shadows(color, ceil(alpha))
        else:
            self.filt.set_alpha(alpha)

        # blit filter over whole surface
        self.surface.blit(self.filt, (0, 0))

    @property
    def moonlight(self):
        return self.moonlight_tiles[self.current_frame]

    @property
    def moonlight_alpha(self):
        return self._moonlight_alpha

    @moonlight_alpha.setter
    def moonlight_alpha(self, val):
        self._moonlight_alpha = val
        if self._moonlight_alpha >= 255:
            self.moonlight_up = False
            self._moonlight_alpha = 255
        elif self._moonlight_alpha <= 0:
            self.moonlight_up = True
            self.current_frame += 1
            self.current_frame %= 2
            self._moonlight_alpha = 0

    def render_moonlight(self, state):
        def render_filter(self, color, alpha):
            filt = pygame.Surface(config.screen_size)
            filt.fill(color)

            filt.set_alpha(alpha)

            # blit filter over whole surface
            self.surface.blit(filt, (0, 0))

        if self.effect_is_fading_in:
            alpha = (state['effect_alpha']
                     - config.moonlight_fade_in_f
                     + self.fade_in_frame)
            render_filter(self,
                          config.moonlight_color,
                          alpha,
                          )
            self.shadows.set_alpha(255 - alpha)

        else:
            render_filter(self,
                          config.moonlight_color,
                          state['effect_alpha'],
                          )
            self.shadows.set_alpha(255 - state['effect_alpha'])

        if self.moonlight_up:
            self.moonlight_alpha += 255 // (2 * config.framerate)
        else:
            self.moonlight_alpha -= 255 // (2 * config.framerate)
        # fade moonlight in
        self.moonlight.set_alpha(self.moonlight_alpha)
        width = self.moonlight.get_width()

        for x in range(ceil(config.screen_size[0] / width)):
            self.surface.blit(self.moonlight, (width * x, 0))

        self.surface.blit(self.shadows, (0, 0))

    def render_lightning(self, state):
        self.render_filter(config.lightning_color, state['effect_alpha'])

    def render(self, state):
        mode = state['current_game_mode']

        if mode == config.Modes.GAME:
            colors_map = {'moonlight': self.render_moonlight,
                          'lightning': self.render_lightning,
                          }

            if state['effect_fade_in']:
                self.effect_is_fading_in = True
                self.fade_in_frame += 1

                if state['effect'] == 'moonlight':
                    if self.fade_in_frame == config.moonlight_fade_in_f:
                        state['effect_fade_in'] = False
                        self.effect_is_fading_in = False

                elif state['effect'] == 'lightning':
                    if self.fade_in_frame == config.lightning_fade_in_f:
                        state['effect_fade_in'] = False
                        self.effect_is_fading_in = False

                    if self.fade_in_frame % (config.lightning_fade_in_s) == 0:
                        self.area = max(self.area - 1, self.final_area)

                    self.redo_render = True
                    fade = config.lightning_fade_in_f
                    self.variance -= (self.initial_variance
                                      - self.final_variance) / fade

            if state['effect'] in colors_map:
                colors_map[state['effect']](state)
            else:
                self.reset_to_defaults()
