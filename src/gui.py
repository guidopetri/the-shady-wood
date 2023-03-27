import pygame
import config


class Gui(object):
    def __init__(self, surface):
        self.surface = surface
        # self.hp_icon = pygame.image.load()
        self.courage_font = pygame.font.SysFont(config.courage_fontname,
                                                config.courage_fontsize,
                                                )
        self.courage_font_color = pygame.Color(config.courage_font_color)

        # self.item_icons = pygame.image.load()

    def render(self, state):
        mode = state['current_game_mode']

        if mode == config.Modes.GAME:
            self.render_gui(state['hp'], state['status'], state['inventory'])

    def render_gui(self, hp, status, inventory):
        hp_bar = pygame.Surface((config.screen_size[0] // 8,
                                 config.screen_size[1] // 20,
                                 ))
        hp_bar.fill('green')
        hp_bar_rect = hp_bar.get_rect(topright=(config.screen_size[0] - 10,
                                                10))

        item_bar = pygame.Surface((config.screen_size[0] // 3,
                                   config.screen_size[1] // 12,
                                   ))
        item_bar.fill('red')
        item_bar_rect = item_bar.get_rect(midbottom=(config.screen_center[0],
                                                     config.screen_size[1]
                                                     - 10))

        self.surface.blit(hp_bar, hp_bar_rect)
        self.surface.blit(item_bar, item_bar_rect)
