# life game using generator as an demonstration of coroutine.
# 用简单的协程实现生命游戏的模拟

from collections import namedtuple

# define the state of cell
ALIVE = '*'
EMPTY = '-'

# define Query and Transition

Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

# mark the end of an iteration
TICK = object()

class Grid(object):
    # define the grid

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []
        
        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        str_rows = [''.join(row) for row in self.rows]
        return '\n'.join(str_rows)

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state

    def assign_alive(self, y, x):
        self.assign(y, x, ALIVE)


class ColumnPrinter(object):

    def __init__(self):
        self._container = []

    def __str__(self):
        if not self._container:
            return ''
        if len(self._container) == 1:
            return self._container[0]

        old_string_list = []

        for string in self._container:
            splited = string.split('\n')
            old_string_list.append(splited)

        new_string_list = []

        for i in range(len(old_string_list[0])):
            sub_string = '|'.join([old_string_list[j][i] for j in range(len(old_string_list))])
            new_string_list.append(sub_string)

        return '\n'.join(new_string_list)



    def append(self, string):
        self._container.append(string)

# The generators and implementation of coroutine
def game_logic(state, neighbors):
    
    if state == ALIVE:
        if neighbors > 3 or neighbors < 2:
            return EMPTY

    else:
        if neighbors == 3:
            return ALIVE

    return state

# count_neighbors, step_cell, simulate嵌套组成一个大的generator
def count_neighbors(y, x):
    n_ = yield Query(y+1, x)
    ne = yield Query(y+1, x+1)
    nw = yield Query(y+1, x-1)
    s_ = yield Query(y-1, x)
    se = yield Query(y-1, x+1)
    sw = yield Query(y-1, x-1)
    e_ = yield Query(y, x+1)
    w_ = yield Query(y, x-1)

    neighbors = [n_, ne, nw, s_, se, sw, e_, w_] # 来自live_a_generation的send()
    count = sum([neighbor == ALIVE for neighbor in neighbors])
    return count


def step_cell(y, x):
    state = yield Query(y, x) # 格点本身的状态
    neighbors = yield from count_neighbors(y, x) # 格点周围的状态
    state = game_logic(state, neighbors)
    yield Transition(y, x, state)

    
def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK

# 消耗generator的函数
def live_a_generation(grid, sim):
    # Query和Transition相当于generator吐给主函数的请求
    # 主函数处理这些请求，访问及更新grid
    # 若是Query，主函数将访问的结果发送给generator
    # 若是Transition，主函数更新grid，并推动generator
    new_grid = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:
            new_grid.assign(item.y, item.x, item.state)
            item = next(sim)
    return new_grid



# ---------------------- TEST CODE ------------------------------

if __name__ == '__main__':
    grid = Grid(5, 9)
    alive_list = [(0, 3), (1, 4), (2, 2), (2, 3), (2, 4)]
    for alive in alive_list:
        grid.assign_alive(*alive)
    print(grid)
    columns = ColumnPrinter()
    sim = simulate(grid.height, grid.width)
    for i in range(6):
        columns.append(str(grid))
        grid = live_a_generation(grid, sim)
    print(columns)





