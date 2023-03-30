import pygame
import config


class Audio(object):
    def __init__(self):
        self.game_music = 'Anne_in_the_Woods.wav'
        self.menu_music = 'Main_menu.wav'

        self.current_music = self.menu_music
        self.playing = False

    @property
    def current_music(self):
        return self._current_music

    @current_music.setter
    def current_music(self, value):
        pygame.mixer.music.fadeout(config.music_fadeout_time_ms)

        self._current_music = value
        path = config.sfx_path / self.current_music
        pygame.mixer.music.load(path)
        self.playing = False

    def play_current_track(self):
        if not self.playing:
            pygame.mixer.music.play(loops=-1,
                                    fade_ms=config.music_fadein_time_ms,
                                    )
            self.playing = True
        else:
            pass

    def play(self, state):
        if config.debug_mode:
            pass
            pygame.mixer.music.set_volume(0)

        # keep playing the current song by default
        track = self.current_music

        if state['current_game_mode'] == config.Modes.GAME:
            track = self.game_music
        elif state['current_game_mode'] == config.Modes.MAIN_MENU:
            track = self.menu_music

        if self.current_music != track:
            self.current_music = track
        self.play_current_track()
