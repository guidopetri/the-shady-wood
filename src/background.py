import pygame
import config


class Background(object):
    def __init__(self, surface):
        self.surface = surface
        self.cross_bg = pygame.image.load(
            f"{config.gfx_path}/sample_cross_bg.bmp"
            )

        self._position_x = 0
        self._position_y = 0

    @property
    def position(self):
        return (self._position_x, self._position_y)

    def render(self, mode):
        self.surface.fill('black')
        if mode == config.Modes.MAIN_MENU:
            pass
        elif mode == config.Modes.GAME:
            self.surface.blit(self.cross_bg, self.position)

            # to the left
            self.surface.blit(self.cross_bg,
                              (self._position_x
                               - self.cross_bg.get_width()
                               + config.img_buffer,
                               self._position_y)
                              )
            # to the top
            self.surface.blit(self.cross_bg,
                              (self._position_x,
                               self._position_y
                               - self.cross_bg.get_height()
                               + config.img_buffer)
                              )

            # diagonal
            self.surface.blit(self.cross_bg,
                              (self._position_x
                               - self.cross_bg.get_width()
                               + config.img_buffer,
                               self._position_y
                               - self.cross_bg.get_height()
                               + config.img_buffer)
                              )

    def move(self, amount):
        self._position_x += amount[0]
        self._position_x %= self.cross_bg.get_width()
        self._position_y += amount[1]
        self._position_y %= self.cross_bg.get_height()
