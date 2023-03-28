import pygame
import config


class Gui(object):
    def __init__(self, surface):
        self.surface = surface
        self.render_font()
        self.render_base_hp_bar()
        self.render_base_item_bar()

    def render_font(self):
        self.courage_font = pygame.font.SysFont(config.courage_fontname,
                                                config.courage_fontsize,
                                                )
        self.courage_font_color = pygame.Color(config.courage_font_color)
        self.courage_text = self.courage_font.render('courage',
                                                     True,
                                                     self.courage_font_color,
                                                     )

    def render_base_hp_bar(self):
        # self.hp_icon = pygame.image.load()
        self.hp_icon = pygame.Surface((64, 64)).convert()
        self.hp_icon.fill('magenta')
        self.hp_icon_rect = self.hp_icon.get_rect()

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

        height = (self.hp_icon.get_height() - hp_indicator_size[1]) // 2
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

    def render_base_item_bar(self):
        # self.item_icons = pygame.image.load()
        item_bar_size = (config.screen_size[0] // 3,
                         config.screen_size[1] // 12,
                         )
        self.item_bar = pygame.Surface(item_bar_size).convert()
        self.item_bar.fill('red')

        item_bar_coords = {'midbottom': (config.screen_center[0],
                                         config.screen_size[1] - 10)
                           }
        self.item_bar_rect = self.item_bar.get_rect(**item_bar_coords)

    def render(self, state):
        mode = state['current_game_mode']

        if mode == config.Modes.GAME:
            self.render_gui(state['hp'], state['status'], state['inventory'])

    def color(self, hp):
        return self.empty_hp_color.lerp(self.full_hp_color, hp / 100)

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

        self.surface.blit(hp_indicator_copy, self.hp_indicator_rect)
        self.surface.blit(self.hp_icon, self.hp_icon_rect)
        self.surface.blit(self.item_bar, self.item_bar_rect)
