import pygame
import config


class Dialog(object):
    def __init__(self, surface):
        self.surface = surface
        self.font = pygame.font.Font(config.fontname, config.fontsize)
        self.font_color = pygame.Color(config.font_color)
        self.last_text = None
        self.last_rect = None
        self._default_position = {'midtop': (config.screen_size[0] // 2,
                                             3 * config.screen_size[1] // 4),
                                  }
        self.position = self._default_position

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

        tone_text = ('anne_normal', None)
        self.position = self._default_position

        if mode == config.Modes.INTRO:
            tone_texts = config.intro_messages[:message + 1]
            for idx, (tone, text) in enumerate(tone_texts):
                if state['message_sfx_played']:
                    tone = None

                self.position = {'midtop': (config.screen_size[0] // 2,
                                            int((idx + 1) / 3
                                                * config.screen_size[1]
                                                // 4)),
                                 }
                text, rect = self.render_text(text)
                self.blit_text(text, rect)

            # return to empty string for the last section of this
            # method to still handle sound
            # spaghetti code
            tone = tone_texts[-1][0]
            if state['message_sfx_played']:
                tone = None
            tone_text = (tone, ' ')
        elif mode == config.Modes.GAME:
            if state['msg_duration'] <= 0:
                self.last_text = None
                self.last_rect = None

            if state['effect_fade_in']:
                if state['effect'] == 'moonlight':
                    tone_text = config.moonlight_text
                    if state['message_sfx_played']:
                        tone_text = (None, tone_text[1])
                elif state['effect'] == 'lightning':
                    tone_text = config.lightning_text
                    if state['message_sfx_played']:
                        tone_text = (None, tone_text[1])
            elif state['effect_fade_out']:
                if state['effect'] == 'moonlight':
                    tone_text = config.moonlight_text_end
                    if state['message_sfx_played']:
                        tone_text = (None, tone_text[1])
                elif state['effect'] == 'lightning':
                    tone_text = config.lightning_text_end
                    if state['message_sfx_played']:
                        tone_text = (None, tone_text[1])
            elif state['maze_begin'] and state['msg_duration'] >= 0:
                tone_text = config.maze_begin_message
            elif state['item'].endswith('_out'):
                item = state['item'][:-4]
                tone_text = config.item_end_messages.get(item,
                                                         (None, None),
                                                         )
                if state['first_item_end'][item]:
                    # default to text itself
                    tone_text = config.first_item_end_messages.get(item, tone_text)  # noqa
                if tone_text is not None:
                    state['msg_duration'] = config.msg_duration
                if state['message_sfx_played']:
                    tone_text = (None, tone_text[1])
            elif state['pickup']:
                item = state['last_item_picked_up']
                state['pickup'] = False
                if state['first_item_pickup'].get(item):
                    tone_text = config.first_item_messages.get(item,
                                                               (None, None),
                                                               )
                    state['first_item_pickup'][item] = False

                if tone_text[1] is not None:
                    state['msg_duration'] = config.msg_duration
            elif state['tried_to_use_item']:
                tone_text = config.cant_use_item_text
                if state['message_sfx_played']:
                    tone_text = (None, tone_text[1])
        elif mode == config.Modes.WIN_DIALOG:
            tone_text = config.game_win_text[message]
            if state['message_sfx_played']:
                tone_text = (None, tone_text[1])

        tone, text = tone_text

        if text is not None:
            if tone is not None:
                state['active_sfx'].add(tone)
                state['message_sfx_played'] = True
            text, rect = self.render_text(text)
            self.blit_text(text, rect)
            self.last_text = text
            self.last_rect = rect
        elif self.last_text is not None and mode == config.Modes.GAME:
            self.blit_text(self.last_text, self.last_rect)
