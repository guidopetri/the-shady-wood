import pygame
import config


class Audio(object):
    def __init__(self):
        self.game_music = 'Anne_in_the_Woods.wav'
        self.menu_music = 'Main_menu.wav'
        self.game_over_music = 'Game_over.wav'
        self.win_music = 'Game_win.wav'
        self.lightning_music = 'Lightning.wav'
        self.moonlight_music = 'Moonlight.wav'

        self.current_music = self.menu_music
        self.playing = False

    @property
    def current_music(self):
        return self._current_music

    @current_music.setter
    def current_music(self, value):
        if value == self.game_over_music:
            fadeout = config.music_death_fadeout_time_ms
        else:
            fadeout = config.music_fadeout_time_ms
        pygame.mixer.music.fadeout(fadeout)

        self._current_music = value
        path = config.sfx_path / self.current_music
        pygame.mixer.music.load(path)
        self.playing = False

    def play_current_track(self):
        if not self.playing:
            pygame.mixer.music.play(loops=self.loops,
                                    fade_ms=config.music_fadein_time_ms,
                                    )
            self.playing = True
        else:
            pass

    def play(self, state):
        if config.debug_mode:
            pass
            # pygame.mixer.music.set_volume(0)

        mapper = {config.Modes.GAME: {'regular': self.game_music,
                                      'lightning': self.lightning_music,
                                      'moonlight': self.moonlight_music,
                                      },
                  config.Modes.MAIN_MENU: self.menu_music,
                  config.Modes.GAME_OVER: self.game_over_music,
                  config.Modes.WIN_DIALOG: self.win_music,
                  }

        loops_mapper = {config.Modes.GAME: -1,
                        config.Modes.MAIN_MENU: -1,
                        config.Modes.GAME_OVER: 0,
                        config.Modes.WIN_DIALOG: 0,
                        }

        # keep playing the current song by default
        track = mapper.get(state['current_game_mode'], self.current_music)
        if isinstance(track, dict):
            track = track.get(state['effect'], self.current_music)
        self.loops = loops_mapper.get(state['current_game_mode'], 0)

        if self.current_music != track:
            self.current_music = track
        self.play_current_track()
