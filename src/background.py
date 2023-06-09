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
                      'Win',
                      'WinEnd',
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
                       'horizontal_win': rot_90(raw_imgs['Win']),
                       'mazeend_win': rot_90(raw_imgs['WinEnd']),
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

    def render_win_dialog(self, state):
        self.render_game(state)

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

        self.font = pygame.font.Font(config.fontname,
                                     config.game_over_fontsize,
                                     )
        self.font_color = pygame.Color(config.game_over_font_color)

        self.frame_counter = 0
        self.menu_frame_counter = 0
        self.current_frame = 0

        super().__init__(surface)

    def render_game_over(self, *args):
        self.surface.fill(config.main_menu_bg_color)
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

        coords = {'center': (config.screen_center[0],
                             config.screen_center[1] + 192,
                             )
                  }
        restart_text = self.font.render(config.restart_text,
                                        True,
                                        self.font_color,
                                        )
        restart_rect = restart_text.get_rect(**coords)

        self.surface.blit(game_over_text, game_over_rect)
        self.surface.blit(stone_text, stone_rect)
        self.surface.blit(restart_text, restart_rect)

    def render_intro_dialog(self, *args):
        self.surface.fill(config.main_menu_bg_color)

        self.reset_main_menu_images_transparency(0)

    def reset_main_menu_images_transparency(self, val):
        for sprite in self.main_menu_images:
            sprite.set_alpha(val)
        for sprite in self.title_images:
            sprite.set_alpha(val)

        self.logo.set_alpha(val)
        self.credits_text.set_alpha(val)

    def load_images(self):
        super().load_images()

        self.num_frames = 8
        self.fps = 5
        self._frames_per_sprite = config.framerate / self.fps

        file = 'Main_menu_spritesheet_2x2_384px.png'
        path = config.gfx_path / file
        sheet = pygame.image.load(path).convert_alpha()

        sprites = []
        width = 384
        height = 384

        coords = [(0, 0),
                  (width, 0),
                  (0, height),
                  (width, height),
                  (0, 2 * height),
                  (width, 2 * height),
                  (0, 3 * height),
                  (width, 3 * height),
                  ]

        for idx in range(self.num_frames):
            sprite_area = pygame.Rect(*coords[idx], width, height)
            sprites.append(sheet.subsurface(sprite_area))
            sprites[-1].set_alpha(0)
        self.main_menu_images = sprites
        coords = {'center': config.screen_center}
        self.menu_rect = self.menu_sprite.get_rect(**coords)
        self.menu_rect.move_ip(config.menu_sprite_padding)

        self.menu_text = self.font.render(config.main_menu_text,
                                          True,
                                          self.font_color,
                                          )
        self.menu_text_rect = self.menu_text.get_rect()
        self.menu_text_rect.midtop = self.menu_rect.midbottom
        self.menu_text_rect.move_ip(config.menu_text_padding)

        file = 'Main_menu_spritesheet_title_2x4_331x133px.png'
        path = config.gfx_path / file
        sheet = pygame.image.load(path).convert_alpha()

        sprites = []
        width = 993
        height = 399

        coords = [(0, 0),
                  (width, 0),
                  (0, height),
                  (width, height),
                  (0, 2 * height),
                  (width, 2 * height),
                  (0, 3 * height),
                  (width, 3 * height),
                  ]

        for idx in range(self.num_frames):
            sprite_area = pygame.Rect(*coords[idx], width, height)
            sprites.append(sheet.subsurface(sprite_area))
            sprites[-1].set_alpha(0)
        self.title_images = sprites

        self.title_rect = self.title_sprite.get_rect()
        self.title_rect.midbottom = config.screen_center
        self.title_rect.move_ip(config.title_padding)

        # logo
        file = 'Lemon_Pepper_Logo_148x124px.png'
        path = config.gfx_path / file
        self.logo = pygame.image.load(path).convert_alpha()

        coords = {'center': config.screen_center}
        self.logo_rect = self.logo.get_rect(**coords)
        self.logo.set_alpha(0)

        # fadein credits
        self.credits_text = self.font.render(config.fadein_credits_text,
                                             True,
                                             self.font_color,
                                             )
        self.credits_text_rect = self.credits_text.get_rect(**coords)
        self.credits_text_rect.move_ip(config.fadein_credits_text_padding)
        self.credits_text.set_alpha(0)

        self.generate_states_map()

    def advance_frame(self):
        self.frame_counter += 1
        if self.frame_counter >= self._frames_per_sprite:
            self.current_frame += 1
            self.frame_counter = 0

        self.current_frame %= self.num_frames

    @property
    def title_sprite(self):
        return self.title_images[self.current_frame]

    @property
    def menu_sprite(self):
        return self.main_menu_images[self.current_frame]

    def generate_states_map(self):
        # spaghetti code, there must be a better way
        # but i'm pretty tired

        states_map = {'fading_in_logo': {'period': config.logo_fadein_period,
                                         'next': 'hold_logo',
                                         'blit_imgs': [(self.logo,
                                                        self.logo_rect,
                                                        ),
                                                       ],
                                         'alpha_mod': 2,
                                         },
                      'hold_logo': {'period': config.logo_hold_period,
                                    'next': 'fading_out_logo',
                                    'blit_imgs': [(self.logo,
                                                   self.logo_rect,
                                                   ),
                                                  ],
                                    'alpha_mod': 0,
                                    },
                      'fading_out_logo': {'period': config.logo_fadeout_period,
                                          'next': 'fading_in_credits',
                                          'blit_imgs': [(self.logo,
                                                         self.logo_rect,
                                                         ),
                                                        ],
                                          'alpha_mod': -2,
                                          },
                      'fading_in_credits': {'period': config.credits_fadein_period,  # noqa
                                            'next': 'hold_credits',
                                            'blit_imgs': [(self.credits_text,
                                                           self.credits_text_rect,  # noqa
                                                           ),
                                                          ],
                                            'alpha_mod': 2,
                                            },
                      'hold_credits': {'period': config.credits_hold_period,
                                       'next': 'fading_out_credits',
                                       'blit_imgs': [(self.credits_text,
                                                      self.credits_text_rect,
                                                      ),
                                                     ],
                                       'alpha_mod': 0,
                                       },
                      'fading_out_credits': {'period': config.credits_fadeout_period,  # noqa
                                             'next': 'fading_in_anne',
                                             'blit_imgs': [(self.credits_text,
                                                            self.credits_text_rect,  # noqa
                                                            ),
                                                           ],
                                             'alpha_mod': -2,
                                             },
                      'fading_in_anne': {'period': config.anne_fadein_period,
                                         'next': 'fading_in_title',
                                         'blit_imgs': [(self.main_menu_images,
                                                        self.menu_rect,
                                                        ),
                                                       ],
                                         'alpha_mod': 2,
                                         },
                      'fading_in_title': {'period': config.title_fadein_period,
                                          'next': 'hold_at_menu',
                                          'blit_imgs': [(self.main_menu_images,
                                                         self.menu_rect,
                                                         ),
                                                        (self.title_images,
                                                         self.title_rect,
                                                         ),
                                                        ],
                                          'alpha_mod': 3,
                                          },
                      'hold_at_menu': {'period': config.ready_hold_period,
                                       'next': 'menu_ready',
                                       'blit_imgs': [(self.main_menu_images,
                                                      self.menu_rect,
                                                      ),
                                                     (self.title_images,
                                                      self.title_rect,
                                                      ),
                                                     ],
                                       'alpha_mod': 0,
                                       },
                      }
        self.states_map = states_map

    def render_main_menu(self, state):
        self.surface.fill(config.main_menu_bg_color)

        self.menu_frame_counter += 1

        advance_frames_on_states = ('fading_in_anne',
                                    'fading_in_title',
                                    'hold_at_menu',
                                    )

        if not state['menu_ready']:
            for key, info in self.states_map.items():
                if state[key]:
                    if self.menu_frame_counter >= info['period']:
                        state[key] = False
                        state[info['next']] = True
                        self.menu_frame_counter = 0
                    if key in advance_frames_on_states:
                        self.advance_frame()
                    for (img, rect) in info['blit_imgs']:
                        if isinstance(img, list):
                            for i in img:
                                i.set_alpha(i.get_alpha() + info['alpha_mod'])
                            blit_img = img[self.current_frame]
                        else:
                            img.set_alpha(img.get_alpha() + info['alpha_mod'])
                            blit_img = img
                        self.surface.blit(blit_img, rect)
                    break

        if state['menu_ready']:
            self.reset_main_menu_images_transparency(255)

            self.menu_frame_counter = 0
            self.advance_frame()
            self.surface.blit(self.title_sprite, self.title_rect)
            self.surface.blit(self.menu_sprite, self.menu_rect)
            self.surface.blit(self.menu_text, self.menu_text_rect)


class Foreground(AbstractBG):
    def __init__(self, surface):
        self.image_type = 'Tree'

        self.font = pygame.font.Font(config.fontname,
                                     config.credits_fontsize,
                                     )
        self.font_color = pygame.Color(config.credits_font_color)

        coords = {'center': (config.screen_center[0], 5)}
        self.credits_text = self.font.render(config.credits_text,
                                             True,
                                             self.font_color,
                                             )
        self.credits_rect = self.credits_text.get_rect(**coords)
        self.credits_rect.move_ip(config.credits_padding)

        self.intro_font = pygame.font.Font(config.fontname,
                                           config.advance_fontsize,
                                           )
        self.intro_font_color = pygame.Color(config.advance_color)

        coords = {'center': (config.screen_size[0] - 128,
                             config.screen_size[1] - 64,
                             )
                  }
        self.advance_text = self.font.render(config.advance_text,
                                             True,
                                             self.font_color,
                                             )
        self.advance_rect = self.advance_text.get_rect(**coords)
        self.advance_rect.move_ip(config.advance_padding)

        self.version_color = pygame.Color(config.version_color)
        self.version_text = self.font.render(config.version_text,
                                             True,
                                             self.version_color,
                                             )
        coords = {'bottomright': config.screen_size}
        self.version_rect = self.version_text.get_rect(**coords)
        self.version_rect.move_ip(config.version_text_padding)

        super().__init__(surface)

    def render_intro_dialog(self, state):
        super().render_intro_dialog(state)

        # press any key to advance
        self.surface.blit(self.advance_text, self.advance_rect)

    def render_win_dialog(self, state):
        super().render_win_dialog(state)

        if state['ready_for_win']:
            # press any key to advance
            self.surface.blit(self.advance_text, self.advance_rect)

    def render_main_menu(self, state):
        super().render_main_menu(state)

        if state['menu_ready']:
            # credits
            self.surface.blit(self.credits_text, self.credits_rect)
            self.surface.blit(self.version_text, self.version_rect)


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
        self.redo_render = True
        self.shadows = None
        self.default_shadows = None
        self.default_variance = variance
        self.variance = variance
        self._item = 'none'
        self.frame_counter = 0
        self.current_frame = 0
        self.num_flash_frames = 0

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area):
        self._area = area
        self.redo_render = True

    @property
    def variance(self):
        return self._variance

    @variance.setter
    def variance(self, variance):
        self._variance = variance
        if self._variance == self.default_variance:
            self.shadows = self.default_shadows
        else:
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

        if config.debug_mode:
            pass
            # print('rerender')

        return shadow

    def update_item(self, item):
        if self._item == item:
            return
        elif item == 'none':
            self.variance = self.default_variance
        elif item == 'candle':
            self.variance = config.item_variances[item]
        elif item == 'firefly':
            self.variance = config.firefly_default_variance
        self._item = item

    def advance_frame(self):
        if self._item == 'firefly':
            self.frame_counter += 1
            if self.frame_counter >= config.firefly_flash_frames_freq:
                self.frame_counter = 0
                self.num_flash_frames = config.firefly_flash_frames
                self.variance = config.item_variances['firefly']

            if self.num_flash_frames > 0:
                self.num_flash_frames -= 1
                if self.num_flash_frames <= 0:
                    self.num_flash_frames = 0
                    self.variance = config.firefly_default_variance

    def render(self, state):
        mode = state['current_game_mode']

        if mode == config.Modes.GAME:
            self.update_item(state['item'])
            self.advance_frame()
            if self.redo_render or self.shadows is None:
                self.shadows = self.render_shadows('black', 255)
                if self.default_shadows is None:
                    self.default_shadows = self.shadows

            if state['effect'] == 'regular':
                self.surface.blit(self.shadows, (0, 0))


class LightStatusEffects(Shadows):
    def __init__(self, surface):
        self.initial_area = 120
        self.initial_variance = 240
        self.final_area = 50
        self.final_variance = 200

        moon_num_frames = 2
        filename = 'Moonlight_Rays_2x1_384px.png'

        self.moonlight_tiles = self.load_spritesheet(moon_num_frames,
                                                     filename,
                                                     384,
                                                     384,
                                                     )

        self.rain_num_frames = 4
        filename = 'Lightning_Rain_Spritesheet_2x2_128px.png'

        self.rain_tiles = self.load_spritesheet(self.rain_num_frames,
                                                filename,
                                                128,
                                                128,
                                                )

        self.rain_fps = config.lightning_rain_fps
        self._rain_frames_per_sprite = config.framerate / self.rain_fps
        self.current_rain_frame = 0
        self.rain_frame_counter = 0

        self.calc_num_tiles_in_screen()

        super().__init__(surface,
                         area=self.initial_area,
                         variance=480,
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
        self.effect_is_fading_out = False
        self.current_frame = 0
        self.moonlight_alpha = 0
        self.moonlight_up = True
        self.current_rain_frame = 0
        self.rain_frame_counter = 0

    def render_filter(self, color, alpha):
        if self.effect_is_fading_in or self.effect_is_fading_out:

            self.filt = self.render_shadows(color, ceil(alpha))
            if self.effect_is_fading_out:
                self.filt.set_alpha(255)
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

    def calc_num_tiles_in_screen(self):
        self.h_tiles = ceil(config.screen_size[0]
                            / (2 * 128)
                            )
        self.v_tiles = ceil(config.screen_size[1]
                            / (2 * 128)
                            )

    def render_rain(self, state, alpha):
        for y in range(-self.v_tiles, self.v_tiles + 1):
            for x in range(-self.h_tiles, self.h_tiles + 1):
                h_adjustment = state['position'][0] % 128
                v_adjustment = state['position'][1] % 128

                pos = (int(128 * (x + 0.5)
                           + config.screen_center[0]
                           - h_adjustment),
                       int(128 * (y + 0.5)
                           + config.screen_center[1]
                           - v_adjustment),
                       )
                if config.debug_mode and (x, y) == (0, 0):
                    # where center tile will be plotted
                    # print(pos)
                    pygame.draw.rect(self.surface,
                                     'magenta',
                                     pygame.Rect(*pos, 5, 5)
                                     )

                    # h/v adjustment for player position
                    # also location within current tile
                    # print(h_adjustment, v_adjustment)
                    pygame.draw.rect(self.surface,
                                     'green',
                                     pygame.Rect(h_adjustment,
                                                 v_adjustment,
                                                 3,
                                                 3,
                                                 ))

                rect = self.current_rain_tile.get_rect(center=pos)
                self.current_rain_tile.set_alpha(alpha)
                self.surface.blit(self.current_rain_tile, rect)

    @property
    def current_rain_tile(self):
        return self.rain_tiles[self.current_rain_frame]

    def render_lightning(self, state):
        if self.effect_is_fading_out:
            if self.fade_in_frame % (config.lightning_fade_in_s) == 0:
                self.area = min(self.area + 1, self.initial_area)

            fade = config.lightning_fade_in_f
            self.variance += (self.initial_variance
                              - self.final_variance) / fade

            shadow_alpha = (state['effect_alpha']
                            - config.moonlight_fade_in_f
                            + self.fade_in_frame)
        else:
            shadow_alpha = state['effect_alpha']

        self.render_filter(config.lightning_color, shadow_alpha)

        self.rain_frame_counter += 1
        if self.rain_frame_counter >= self._rain_frames_per_sprite:
            self.current_rain_frame += 1
            self.rain_frame_counter = 0

        self.current_rain_frame %= self.rain_num_frames

        if self.effect_is_fading_out:
            self.fade_in_frame -= 1
            self.fade_in_frame = max(0, self.fade_in_frame)

        # alt: looked pretty good - coming on once fadein is over
        # alpha = (config.lightning_rain_alpha
        #          * int(self.fade_in_frame / config.lightning_fade_in_f))

        alpha = int(config.lightning_rain_alpha
                    * self.fade_in_frame
                    / config.lightning_fade_in_f)

        self.render_rain(state, alpha)

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

                    fade = config.lightning_fade_in_f
                    self.variance -= (self.initial_variance
                                      - self.final_variance) / fade
            elif state['effect_fade_out']:
                self.effect_is_fading_out = True

            if state['effect'] in colors_map:
                colors_map[state['effect']](state)
            else:
                self.reset_to_defaults()
