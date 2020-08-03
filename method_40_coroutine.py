from collections import namedtuple
from functools import partial
import numpy as np

def my_coroutine():
    while True:
        received = yield # 第一次执行next(it)时把生成器推到这里，执行了yield后面的语句
        print('Received: ', received) # send之后，把send的值赋给recieved，然后执行yield下面的语句


def minimize():
    # 生成器协程：每收到一个数值，就会给出当前统计到的最小值
    current = yield
    while True:
        value = yield current
        current = min(value, current)

# 生命游戏
# 每个细胞都表示为一个协程
ALIVE = '*'
EMPTY = '-'
Query = namedtuple('Query', ('y', 'x'))
Transition = namedtuple('Transition', ('y', 'x', 'state'))

def count_neighbors(y, x):
    # 每一个yield表达式的结果，要么是ALIVE，要么是EMPTY
    # 返回本细胞周边的存活细胞个数
    n_ = yield Query(y+1, x) # North
    ne = yield Query(y+1, x+1) # Northeast
    nw = yield Query(y+1, x-1)
    s_ = yield Query(y-1, x)
    se = yield Query(y-1, x+1)
    sw = yield Query(y-1, x-1)
    e_ = yield Query(y, x+1)
    w_ = yield Query(y, x-1)


    neighbor_states = [n_, ne, e_, se, s_, sw, w_, nw]
    count = 0
    for state in neighbor_states:
        if state == ALIVE:
            count += 1
    return count


def game_logic(state, neighbors):
    if state == ALIVE:
        if neighbors > 3 or neighbors < 2:
            return EMPTY
    else:
        if neighbors == 3:
            return ALIVE
    return state



def step_cell(y, x):
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)
    # 消耗掉count_neighbors之后执行后面的语句
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)

# TICK 对象用以表示当前这代的细胞已经全部迁移完毕
TICK = object()

def simulate(height, width):
    while True:
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)
        yield TICK


class Grid(object):
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



def live_a_generation(grid, sim):
    # grid: 旧的格子
    # progeny: 新生成的格子
    progeny = Grid(grid.height, grid.width)
    item = next(sim)
    while item is not TICK: # 推动simulate，从而推动step_cell和ount_neighbors
        if isinstance(item, Query): # 一个点执行9次
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else: # Must be a Transition # 一个点执行1次
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)
    return progeny


class ColumnPrinter():

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






if __name__ == '__main__':



    grid = Grid(5, 9)
    alive_list = [(0, 3), (1, 4), (2, 2), (2, 3), (2, 4)]
    for alive in alive_list:
        grid.assign_alive(*alive)
    columns = ColumnPrinter()
    sim = simulate(grid.height, grid.width)
    for i in range(6):
        columns.append(str(grid))
        grid = live_a_generation(grid, sim)
    print(columns)


    # gen_0 = range(5)

    # def gen_1():
    #     yield -1
    #     c = yield from gen_0
    #     print(c)
    #     yield 10

    # def gen_2():
    #     yield 99
    #     yield from gen_1()


    

















