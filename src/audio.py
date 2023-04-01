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


class SFX(object):
    def __init__(self):
        self.sfx_path = config.sfx_path

        self.paths = {'hp_drain': 'Hp_draining.wav',
                      'pickup': 'Item_pickup.wav',
                      'item_use': 'Item_use_Menu_select.wav',
                      'anne_normal': 'Anne_speaking_normal.wav',
                      'anne_negative': 'Anne_speaking_negative.wav',
                      }
        self.loops = {'hp_drain': -1,
                      'pickup': 0,
                      'item_use': 0,
                      'anne_normal': 0,
                      'anne_negative': 0,
                      }
        self.sfx = {name: self.load_sound(path)
                    for name, path in self.paths.items()
                    }
        self.channels = {name: pygame.mixer.Channel(idx)
                         for idx, name in enumerate(self.sfx.keys())
                         }

        self.sfx['anne_normal'].set_volume(0.3)
        self.sfx['item_use'].set_volume(0.3)
        self.sfx['pickup'].set_volume(0.3)

    def load_sound(self, path):
        return pygame.mixer.Sound(self.sfx_path / path)

    def play(self, state):
        for name, sfx in self.sfx.items():
            if name in state['active_sfx']:
                # if the sound is "active", but not playing
                # or if it's anne speaking
                if not self.channels[name].get_busy() or name == 'anne_normal':
                    # then play it
                    self.channels[name].play(sfx, loops=self.loops[name])
            else:
                # if the sound is "not active", but playing,
                # and won't end by itself
                if self.channels[name].get_busy() and self.loops[name] == -1:
                    # then stop it with a fadeout
                    sfx.fadeout(100)
