import config
import random
import numpy as np
from math import ceil


class Map(object):
    def __init__(self):
        self.characters = {'cross': '╬',
                           't_up': '╩',
                           't_down': '╦',
                           't_right': '╠',
                           't_left': '╣',
                           'straight_horizontal': '═',
                           'straight_vertical': '║',
                           'corner_topleft': '╝',
                           'corner_topright': '╚',
                           'corner_botleft': '╗',
                           'corner_botright': '╔',
                           'deadend_left': '╡',
                           'deadend_right': '╞',
                           'deadend_up': '╨',
                           'deadend_down': '╥',
                           'blank': ' ',
                           }

    def generate_map(self, size=config.default_map_size):
        grid = [[[] for _ in range(size[0])] for _ in range(size[1])]

        DX = {'E': 1, 'W': -1, 'N': 0, 'S': 0}
        DY = {'E': 0, 'W': 0, 'N': -1, 'S': 1}
        opposite = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}

        directions_map = {'ENSW': 'cross',
                          'ENW': 't_up',
                          'ESW': 't_down',
                          'ENS': 't_right',
                          'NSW': 't_left',
                          'EW': 'straight_horizontal',
                          'NS': 'straight_vertical',
                          'NW': 'corner_topleft',
                          'EN': 'corner_topright',
                          'SW': 'corner_botleft',
                          'ES': 'corner_botright',
                          'W': 'deadend_left',
                          'E': 'deadend_right',
                          'N': 'deadend_up',
                          'S': 'deadend_down',
                          '': 'blank',
                          }

        def carve_passages_from(cx, cy, grid):
            for direction in random.sample(['N', 'S', 'E', 'W'], 4):
                nx = cx + DX[direction]
                ny = cy + DY[direction]

                available = (0 <= ny < size[1]
                             and 0 <= nx < size[0]
                             and not grid[ny][nx]
                             )
                if available:
                    grid[cy][cx].append(direction)
                    grid[ny][nx].append(opposite[direction])
                    carve_passages_from(nx, ny, grid)

        carve_passages_from((size[0] - 1) // 2,
                            (size[1] - 1) // 2,
                            grid,
                            )

        for y, col in enumerate(grid):
            for x, row in enumerate(col):
                grid[y][x] = directions_map[''.join(sorted(grid[y][x]))]

        buffer_size = ceil(max(config.screen_size) / 384)
        buffered_grid = np.full((size[0] + 2 * buffer_size,
                                 size[1] + 2 * buffer_size),
                                'blank',  # buffer with blanks
                                dtype="U20",
                                )

        buffered_grid[buffer_size: -buffer_size,
                      buffer_size: -buffer_size] = grid

        self.map = buffered_grid.tolist()

    def pretty_print(self):
        for row in self.map:
            for item in row:
                print(self.characters[item], end="")
            print()


if __name__ == '__main__':
    import time

    m = Map()

    start_time = time.time()
    m.generate_map((21, 21))
    print(f'Time taken to generate map: {time.time() - start_time}')
    print('\n\n')
    m.pretty_print()
