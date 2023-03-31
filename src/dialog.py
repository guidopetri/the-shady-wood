import pygame
import config


class Dialog(object):
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.SysFont(config.fontname, config.fontsize)
        self.font_color = pygame.Color(config.font_color)
        self.last_text = None
        self.last_rect = None

    @property
    def position(self):
        return {'midtop': (config.screen_size[0] // 2,
                           3 * config.screen_size[1] // 4),
                }

    def render_box_bg(self, width, height):
        # create filled in rect for border
        border_rect = pygame.Rect(0,
                                  0,
                                  width + config.border_size[0],
                                  height + config.border_size[1],
                                  )
        border_rect.midtop = self.position['midtop']

        pygame.draw.rect(self.surface,
                         config.dialog_border_color,
                         border_rect,
                         border_radius=config.dialog_border_radius,
                         )

        # create bg to overlay on border
        bg_rect = pygame.Rect(0,
                              0,
                              border_rect.width - config.border_padding,
                              border_rect.height - config.border_padding,
                              )
        bg_rect.midtop = border_rect.midtop
        bg_rect.move_ip(0, config.border_padding // 2)

        # blit bg within border to achieve a border effect
        pygame.draw.rect(self.surface,
                         config.dialog_box_color,
                         bg_rect,
                         border_radius=config.dialog_border_radius,
                         )

    def render_text(self, text):
        render = self.font.render(text, True, self.font_color)
        rect = render.get_rect(**self.position)
        rect.move_ip(config.text_padding)
        return render, rect

    def blit_text(self, text, rect):
        self.surface.blit(text, rect)

    def render(self, state):
        mode = state['current_game_mode']
        message = state['active_message']

        text = None

        if mode == config.Modes.INTRO:
            text = config.intro_messages[message]
        elif mode == config.Modes.GAME:
            if state['msg_duration'] <= 0:
                self.last_text = None
                self.last_rect = None

            if state['effect_fade_in']:
                if state['effect'] == 'moonlight':
                    text = config.moonlight_text
                elif state['effect'] == 'lightning':
                    text = config.lightning_text
            elif state['effect_fade_out']:
                if state['effect'] == 'moonlight':
                    text = config.moonlight_text_end
                elif state['effect'] == 'lightning':
                    text = config.lightning_text_end
            elif state['maze_begin'] and state['msg_duration'] >= 0:
                text = config.maze_begin_message
            elif state['item'].endswith('_out'):
                item = state['item'][:-4]
                text = config.item_end_messages.get(item)
                if state['first_item_end'][item]:
                    # default to text itself
                    text = config.first_item_end_messages.get(item, text)

                if text is not None:
                    state['msg_duration'] = config.msg_duration
        elif mode == config.Modes.WIN_DIALOG:
            text = config.game_win_text[message]

        if text is not None:
            text, rect = self.render_text(text)
            self.render_box_bg(rect.width, rect.height)
            self.blit_text(text, rect)
            self.last_text = text
            self.last_rect = rect
        elif self.last_text is not None and mode == config.Modes.GAME:
            self.render_box_bg(self.last_rect.width, self.last_rect.height)
            self.blit_text(self.last_text, self.last_rect)
