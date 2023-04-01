import config
import random
import numpy as np


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
                           'mazeend_left': 'x',
                           'mazeend_right': 'x',
                           'mazeend_up': 'x',
                           'mazeend_down': 'x',
                           }

        self.generate_win_map()

    def generate_win_map(self, size=config.default_map_size):
        buffer_size = config.map_buffer_size

        grid = np.full((size[0] + 2 * buffer_size,
                        size[1] + 2 * buffer_size),
                       'blank',  # buffer with blanks
                       dtype="U20",
                       )

        center = ((size[0] - 1) // 2 + buffer_size - 1,
                  (size[1] - 1) // 2 + buffer_size,
                  )

        replacement = (['mazeend_win']
                       + ['horizontal_win'] * len(grid[0, center[0]: -1]))

        grid[center[1], center[0]:] = replacement
        self.win_map = grid

    def generate_map(self, size=config.default_map_size):

        final_side = random.sample(['N', 'S', 'E', 'W'], 1)[0]
        final_loc = random.randrange(0,
                                     size[0]
                                     if final_side in ['N', 'S']
                                     else size[1],
                                     )

        grid = [[[] for _ in range(size[0])] for _ in range(size[1])]

        self.DX = {'E': 1, 'W': -1, 'N': 0, 'S': 0}
        self.DY = {'E': 0, 'W': 0, 'N': -1, 'S': 1}
        self.opposite = {'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N'}

        self.directions_map = {'ENSW': 'cross',
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
                               'Wx': 'mazeend_left',
                               'Ex': 'mazeend_right',
                               'Nx': 'mazeend_up',
                               'Sx': 'mazeend_down',
                               '': 'blank',
                               }

        self.inv_directions_map = {v: k
                                   for k, v in self.directions_map.items()
                                   }

        def carve_passages_from(cx, cy, grid):
            for direction in random.sample(['N', 'S', 'E', 'W'], 4):
                nx = cx + self.DX[direction]
                ny = cy + self.DY[direction]

                available = (0 <= ny < size[1]
                             and 0 <= nx < size[0]
                             and not grid[ny][nx]
                             )
                if available:
                    grid[cy][cx].append(direction)
                    grid[ny][nx].append(self.opposite[direction])
                    carve_passages_from(nx, ny, grid)

        carve_passages_from((size[0] - 1) // 2,
                            (size[1] - 1) // 2,
                            grid,
                            )

        # insert win piece
        mapping = {'E': (size[0] - 1, final_loc),
                   'W': (0, final_loc),
                   'N': (final_loc, 0),
                   'S': (final_loc, size[1] - 1),
                   }
        coords = mapping[final_side]
        grid[coords[1]][coords[0]].append(final_side)

        for y, col in enumerate(grid):
            for x, row in enumerate(col):
                grid[y][x] = self.directions_map[''.join(sorted(grid[y][x]))]

        buffer_size = config.map_buffer_size
        buffered_grid = np.full((size[0] + 2 * buffer_size,
                                 size[1] + 2 * buffer_size),
                                'blank',  # buffer with blanks
                                dtype='U20',
                                )

        buffered_grid[buffer_size: -buffer_size,
                      buffer_size: -buffer_size] = grid

        # insert win piece
        mapping = {'E': (size[0] + buffer_size, final_loc + buffer_size),
                   'W': (buffer_size - 1, final_loc + buffer_size),
                   'N': (final_loc + buffer_size, buffer_size - 1),
                   'S': (final_loc + buffer_size, size[1] + buffer_size),
                   }
        xy = mapping[final_side]

        win_piece = f"{self.opposite[final_side]}x"
        buffered_grid[xy[1]][xy[0]] = self.directions_map[win_piece]

        self.map = buffered_grid.tolist()

        grid = np.full(buffered_grid.shape, '', dtype='U1')
        self.ai_map = self.flood_fill(xy[0], xy[1], grid, '')
        self.generate_item_map(buffered_grid.shape)

    def generate_item_map(self, shape):
        grid = np.full(shape, ' ', dtype='U7')

        objects = [' ', ' ', ' ', 'firefly' 'firefly', 'snail']
        unique_objs = ['firefly', 'snail']
        t_objs = [' ', ' ', ' ', ' ', 'firefly', 'firefly', 'snail', 'snail']
        corner_objs = [' '] * 45 + ['firefly'] * 4 + ['snail']
        straight_objs = [' '] * 45 + ['firefly'] * 4 + ['snail']

        for y, row in enumerate(self.map):
            for x, tile in enumerate(row):
                if tile.startswith('deadend'):
                    # pick one item at random
                    item = random.sample(objects, 1)[0]
                    grid[y][x] = item
                elif tile == 'cross':
                    # guarantee an item at a cross
                    item = random.sample(unique_objs, 1)[0]
                    grid[y][x] = item
                elif tile.startswith('t_'):
                    item = random.sample(t_objs, 1)[0]
                    grid[y][x] = item
                elif tile.startswith('corner_'):
                    item = random.sample(corner_objs, 1)[0]
                    grid[y][x] = item
                elif tile.startswith('straight_'):
                    item = random.sample(straight_objs, 1)[0]
                    grid[y][x] = item

        # set center to no item
        grid[grid.shape[0] // 2, grid.shape[1] // 2] = ' '

        self.item_map = grid.tolist()

    def flood_fill(self, x, y, grid, ignore_direction):
        for direction in ['E', 'N', 'S', 'W']:
            if direction == ignore_direction:
                continue
            nx = x + self.DX[direction]
            ny = y + self.DY[direction]

            next_directions = self.inv_directions_map[self.map[ny][nx]]
            available = self.opposite[direction] in next_directions
            if available:
                grid[ny][nx] = self.opposite[direction]
                grid = self.flood_fill(nx, ny, grid, self.opposite[direction])
        return grid

    def pretty_print(self):
        for row in self.map:
            for item in row:
                print(self.characters[item], end="")
            print()

    def pretty_print_ai(self):
        for row in self.ai_map:
            for item in row:
                print(f'{item} ', end="")
            print()

    def pretty_print_item(self):
        m = {'firefly': 'f', 'snail': 's', ' ': ' '}
        for y, row in enumerate(self.map):
            for x, item in enumerate(row):
                print(self.characters[item] + m[self.item_map[y][x]],
                      end="",
                      )
            print()


if __name__ == '__main__':
    import time

    m = Map()

    start_time = time.time()
    m.generate_map((21, 21))
    print(f'Time taken to generate map: {time.time() - start_time}')
    print('\n\n')
    m.pretty_print()
    # m.pretty_print_ai()
    # m.pretty_print_item()
