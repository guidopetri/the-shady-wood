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

        self.item_font = pygame.font.SysFont(config.courage_fontname,
                                             config.item_fontsize,
                                             )
        self.item_font_color = pygame.Color(config.item_font_color)

        key_filename = 'ItemBar_Key_10x10px.png'
        path = config.gfx_path / key_filename
        key_img = pygame.image.load(path).convert_alpha()
        img_rect = key_img.get_rect()
        for item in config.items:
            img = key_img.copy()
            text = self.item_font.render(config.keys[item],
                                         True,
                                         self.item_font_color,
                                         )
            rect = text.get_rect(center=img_rect.center)
            img.blit(text, rect)

            self.shortcut[item] = img

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
                     'dead': 'heart_gameover_sprite_48px.png',
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
        for item in config.items:
            coords = {'center': self.item_rects[item].midbottom}
            rect = self.shortcut[item].get_rect(**coords)
            rect.move_ip(config.item_key_padding)
            self.item_bar_template.blit(self.shortcut[item], rect)

    def render_item_counts(self):
        self.item_count_texts = {}
        self.item_count_rects = {}

        for item in config.items:
            text = self.font.render(str(self.item_count[item]),
                                    True,
                                    self.item_font_color,
                                    )
            coords = {'topright': self.item_rects[item].topright}
            rect = text.get_rect(**coords)
            rect.move_ip(config.item_count_padding)
            self.item_count_texts[item] = text
            self.item_count_rects[item] = rect

    def load_item_icons(self):
        item_bar_size = config.item_bar_size
        item_icon_size = config.item_icon_size
        self.icons = {}
        self.item_rects = {}

        filename = 'ItemBar_184x68px.png'
        path = config.gfx_path / filename
        self.item_bar_template = pygame.image.load(path).convert_alpha()

        coords = {'midbottom': (config.screen_center[0],
                                config.screen_size[1] - 10)
                  }
        self.item_bar_rect = self.item_bar_template.get_rect(**coords)

        filenames = {'candle': 'Candle_sprite_itembar_48px_v2.png',
                     'firefly': 'Firefly_sprite_itembar_48px_v3.png',
                     'snail': 'Snail_sprite_itembar_48px_v3.png',
                     }

        coords = {'candle': {'midleft': (config.item_padding,
                                         item_bar_size[1] // 2),
                             },
                  'firefly': {'midleft': (2 * config.item_padding
                                          + item_icon_size,
                                          item_bar_size[1] // 2),
                              },
                  'snail': {'midleft': (3 * config.item_padding
                                        + 2 * item_icon_size,
                                        item_bar_size[1] // 2),
                            },
                  }

        for item in config.items:
            # load item icon
            path = config.gfx_path / filenames[item]
            self.icons[item] = pygame.image.load(path).convert_alpha()

            # set item coords in item bar
            self.item_rects[item] = self.icons[item].get_rect(**coords[item])

        self.blit_keys_on_item_bar()

    def render_base_item_bar(self):
        self.item_bar = self.item_bar_template.copy()
        self.render_item_counts()

        for item in config.items:
            fn = lambda x: x  # noqa
            if self.item_count[item] == 0:
                fn = pygame.transform.grayscale
            self.item_bar.blit(fn(self.icons[item]), self.item_rects[item])
            self.item_bar.blit(self.item_count_texts[item],
                               self.item_count_rects[item],
                               )

    @property
    def item_count(self):

        class X:
            def __getitem__(s, x):
                return self._inventory_tracker.get(x, 0)

        return X()

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
