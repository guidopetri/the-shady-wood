import pygame
import config


class Gui(object):
    def __init__(self, surface):
        self.surface = surface
        self._inventory_tracker = {}
        self.current_status = 'safe'
        self.current_frame = 0
        self.shortcut = {}

        self.render_text()
        self.load_hp_icons()
        self.load_item_icons()
        self.render_base_hp_bar()
        self.render_base_item_bar()

    def render_text(self):
        self.font = pygame.font.SysFont(config.courage_fontname,
                                        config.courage_fontsize,
                                        )
        self.font_color = pygame.Color(config.courage_font_color)
        self.courage_text = self.font.render('courage',
                                             True,
                                             self.font_color,
                                             )

        for item in config.items:
            self.shortcut[item] = self.font.render(config.keys[item],
                                                   True,
                                                   self.font_color,
                                                   )

    @property
    def num_frames(self):
        return self.num_frames_map[self.current_status]

    @property
    def fps(self):
        return self.fps_map[self.current_status]

    @property
    def _frames_per_sprite(self):
        return self._frames_per_sprite_map[self.current_status]

    def load_hp_icons(self):
        self.hp_icons = {}
        self.num_frames_map = {'safe': 2,
                               'unsafe': 3,
                               'dead': 1}
        self.fps_map = {'safe': 1,
                        'unsafe': 4,
                        'dead': 1}
        self._frames_per_sprite_map = {k: config.framerate // v
                                       for k, v in self.fps_map.items()
                                       }
        self.frame_counter = 0

        filenames = {'safe': 'heart_hp_spritesheet_2x1_48px.png',
                     'unsafe': 'heart_hp_spritesheet_2x2_3frames_48px_vGuido.png',  # noqa
                     # 'dead': '',
                     }

        for status, filename in filenames.items():
            path = config.gfx_path / filename
            sheet = pygame.image.load(path).convert_alpha()

            sprites = []
            width = 48
            height = 48

            coords = [(0, 0),
                      (width, 0),
                      (0, height),
                      ]

            for idx in range(self.num_frames_map[status]):
                sprite_area = pygame.Rect(*coords[idx], width, height)
                sprites.append(sheet.subsurface(sprite_area))

            self.hp_icons[status] = sprites

        self.hp_icon_rect = self.hp_sprite.get_rect()

    def advance_heart_frames(self):
        self.frame_counter += 1
        if self.frame_counter >= self._frames_per_sprite:
            self.frame_counter = 0
            self.current_frame += 1
            self.current_frame %= self.num_frames

    @property
    def hp_sprite(self):
        return self.hp_icons[self.current_status][self.current_frame]

    def render_base_hp_bar(self):
        self.hp_bg_bar_color = pygame.Color(config.hp_bar_bg_color)
        self.hp_bar_radius = config.hp_bar_border_radius

        hp_indicator_size = config.hp_indicator_size
        self.hp_indicator = pygame.Surface(hp_indicator_size).convert()
        pygame.draw.rect(self.hp_indicator,
                         self.hp_bg_bar_color,
                         pygame.Rect(0, 0, *hp_indicator_size),
                         border_radius=self.hp_bar_radius,
                         )
        self.hp_indicator.fill(self.hp_bg_bar_color)

        coords = {'midtop': (hp_indicator_size[0] // 2, 0)}
        self.courage_rect = self.courage_text.get_rect(**coords)
        self.hp_indicator.blit(self.courage_text, self.courage_rect)

        height = (self.hp_sprite.get_height() - hp_indicator_size[1]) // 2
        coords = {'topright': (config.screen_size[0] - 10, height)}
        self.hp_indicator_rect = self.hp_indicator.get_rect(**coords)
        self.hp_icon_rect.midright = self.hp_indicator_rect.midleft

        self.hp_bg_bar_rect = pygame.Rect(0,
                                          0,
                                          hp_indicator_size[0] - 20,
                                          10,
                                          )
        self.hp_bg_bar_rect.midtop = self.courage_rect.midbottom

        self.full_hp_color = pygame.Color(config.full_hp_color)
        self.empty_hp_color = pygame.Color(config.empty_hp_color)

    def blit_keys_on_item_bar(self):

        coords = {'candle': {'center': self.candle_rect.midbottom},
                  'firefly': {'center': self.firefly_rect.midbottom},
                  'snail': {'center': self.snail_rect.midbottom},
                  }

        for item in config.items:
            rect = self.shortcut[item].get_rect(**coords[item])
            self.item_bar_template.blit(self.shortcut[item], rect)

    def render_item_counts(self):
        self.candle_count_text = self.font.render(str(self.candle_count),
                                                  True,
                                                  self.font_color,
                                                  )
        coords = {'topright': self.candle_rect.topright}
        self.candle_count_rect = self.candle_count_text.get_rect(**coords)

        self.firefly_count_text = self.font.render(str(self.firefly_count),
                                                   True,
                                                   self.font_color,
                                                   )
        coords = {'topright': self.firefly_rect.topright}
        self.firefly_count_rect = self.firefly_count_text.get_rect(**coords)

        self.snail_count_text = self.font.render(str(self.snail_count),
                                                 True,
                                                 self.font_color,
                                                 )
        coords = {'topright': self.snail_rect.topright}
        self.snail_count_rect = self.snail_count_text.get_rect(**coords)

    def load_item_icons(self):
        item_bar_size = config.item_bar_size
        icon_size = config.item_icon_size

        self.item_bar_template = pygame.Surface(item_bar_size).convert()
        self.item_bar_template.fill('red')

        coords = {'midbottom': (config.screen_center[0],
                                config.screen_size[1] - 10)
                  }
        self.item_bar_rect = self.item_bar_template.get_rect(**coords)

        # load candle icon
        self.candle_icon = pygame.Surface((icon_size, icon_size)).convert()
        self.candle_icon.fill('white')

        # set candle coords in item bar
        coords = {'midleft': (config.item_padding,
                              item_bar_size[1] // 2),
                  }
        self.candle_rect = self.candle_icon.get_rect(**coords)

        # load firefly icon
        self.firefly_icon = pygame.Surface((icon_size, icon_size)).convert()
        self.firefly_icon.fill('yellow')

        # set firefly coords in item bar
        coords = {'midleft': (2 * config.item_padding
                              + self.candle_icon.get_width(),
                              item_bar_size[1] // 2),
                  }
        self.firefly_rect = self.firefly_icon.get_rect(**coords)

        # load snail icon
        self.snail_icon = pygame.Surface((icon_size, icon_size)).convert()
        self.snail_icon.fill('brown')

        # set snail coords in item bar
        coords = {'midleft': (3 * config.item_padding
                              + self.candle_icon.get_width()
                              + self.firefly_icon.get_width(),
                              item_bar_size[1] // 2),
                  }
        self.snail_rect = self.snail_icon.get_rect(**coords)

        self.blit_keys_on_item_bar()

    def render_base_item_bar(self):
        self.item_bar = self.item_bar_template.copy()
        self.item_bar.blit(self.candle_icon, self.candle_rect)
        self.item_bar.blit(self.firefly_icon, self.firefly_rect)
        self.item_bar.blit(self.snail_icon, self.snail_rect)

        self.render_item_counts()

        self.item_bar.blit(self.candle_count_text, self.candle_count_rect)
        self.item_bar.blit(self.firefly_count_text, self.firefly_count_rect)
        self.item_bar.blit(self.snail_count_text, self.snail_count_rect)

    @property
    def candle_count(self):
        return self._inventory_tracker.get('candle', 0)

    @property
    def firefly_count(self):
        return self._inventory_tracker.get('firefly', 0)

    @property
    def snail_count(self):
        return self._inventory_tracker.get('snail', 0)

    def render(self, state):
        mode = state['current_game_mode']

        if mode == config.Modes.GAME:
            self.render_gui(state['hp'], state['status'], state['inventory'])

    def color(self, hp):
        return self.empty_hp_color.lerp(self.full_hp_color, hp / 100)

    def update_status(self, status):
        if status != self.current_status:
            self.current_status = status
            self.current_frame = 0

    def inventory_changed(self, new_inventory):
        return any([self._inventory_tracker.get(key, 0) != new_val
                    for key, new_val in new_inventory.items()])

    def render_gui(self, hp, status, inventory):
        hp_indicator_copy = self.hp_indicator.copy()
        pygame.draw.rect(hp_indicator_copy,
                         self.hp_bg_bar_color,
                         self.hp_bg_bar_rect,
                         border_radius=self.hp_bar_radius,
                         )

        hp_bar_rect = pygame.Rect(0,
                                  0,
                                  self.hp_bg_bar_rect.width * hp // 100,
                                  self.hp_bg_bar_rect.height,
                                  )
        hp_bar_rect.topleft = self.hp_bg_bar_rect.topleft

        pygame.draw.rect(hp_indicator_copy,
                         self.color(hp),
                         hp_bar_rect,
                         border_radius=self.hp_bar_radius,
                         )

        self.update_status(status)

        if self.inventory_changed(inventory):
            self._inventory_tracker = inventory.copy()
            self.render_base_item_bar()

        self.advance_heart_frames()

        self.surface.blit(hp_indicator_copy, self.hp_indicator_rect)
        self.surface.blit(self.hp_sprite, self.hp_icon_rect)
        self.surface.blit(self.item_bar, self.item_bar_rect)
