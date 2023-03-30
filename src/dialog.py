import pygame
import config


class Dialog(object):
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(config.font_color)

    @property
    def position(self):
        return {'midtop': (config.screen_size[0] // 2,
                           3 * config.screen_size[1] // 4),
                }

    def render_box_bg(self, width, height):
        # create filled in rect for border
        border = pygame.Surface((width + 20, height + 10))
        border.fill(config.dialog_border_color)
        border_rect = border.get_rect(**self.position)

        # create bg to overlay on border
        bg = pygame.Surface((border_rect.width - 10, border_rect.height - 10))
        bg.fill(config.dialog_box_color)
        bg_rect = bg.get_rect(midtop=(border_rect.width / 2, 5))

        # blit bg onto border to achieve a border effect
        border.blit(bg, bg_rect)

        # blit the result onto screen
        self.surface.blit(border, border_rect)

    def render_text(self, text):
        render = self.font.render(text, True, self.font_color)
        rect = render.get_rect(**self.position)
        return render, rect

    def blit_text(self, text, rect):
        self.surface.blit(text, rect)

    def render(self, state):
        mode = state['current_game_mode']
        message = state['active_message']

        if mode == config.Modes.INTRO:
            text, rect = self.render_text(config.intro_messages[message])
            self.render_box_bg(rect.width, rect.height)
            self.blit_text(text, rect)
        elif mode == config.Modes.GAME:
            if state['effect'] == 'moonlight' and state['effect_fade_in']:
                text, rect = self.render_text(config.moonlight_text)
                self.render_box_bg(rect.width, rect.height)
                self.blit_text(text, rect)
