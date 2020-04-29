import copy
import random
import numpy as np
from time import time


class DataPreprocess:
    def __init__(self, filename):
        self.filename = filename
        self.out = self.exc()

    def exc(self):
        raw = []
        f = open(self.filename, 'r')
        for line in f:
            for i, c in enumerate(line):
                if c == '#':
                    line = line[:i]
            if not line or line.isspace():
                continue
            raw.append(line.strip().split(','))
        f.close()

        grid_len = int(raw[0][0])
        gamma = float(raw[1][0])
        noise = [0] * 4
        for i, n in enumerate(raw[2]):
            noise[i] = float(n)
        data = raw[3:]
        for i in range(grid_len):
            data[i] = [float(j) if j != 'X' else j for j in data[i]]
        return grid_len, gamma, noise, data


class MDP:
    def __init__(self, grid, grid_len, gamma, noise):
        self.grid = grid
        self.grid_len = grid_len
        self.gamma = gamma
        self.noise = noise
        self.values = None
        self.policy = None
        self.direction_value = [None] * 4

    def init_value(self):
        values = copy.deepcopy(self.grid)
        value_min = float('inf')
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if values[y][x] != 'X':
                    value_min = min(values[y][x], value_min)

        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if values[y][x] == 'X':
                    values[y][x] = value_min - 1
        last_values = copy.deepcopy(values)
        return values, last_values

    def gen_yx2i(self):
        i = 0
        yx2i = {}
        i2yx = []
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if self.grid[y][x] == 'X':
                    yx2i[(y, x)] = i
                    i2yx.append((y, x))
                    i += 1
        return yx2i, i2yx

    def get_4_direction_value(self, values, y, x):
        d_v = self.direction_value
        d_v[0] = values[y - 1][x] if -1 < y - 1 else values[y][x]
        d_v[1] = values[y][x - 1] if -1 < x - 1 else values[y][x]
        d_v[2] = values[y + 1][x] if y + 1 < self.grid_len else values[y][x]
        d_v[3] = values[y][x + 1] if x + 1 < self.grid_len else values[y][x]
        return d_v

    def is_wall(self, y, x):
        is_wall_list = [y == 0, x == 0, y == self.grid_len - 1, x == self.grid_len - 1]
        return is_wall_list

    def get_rewards(self, values, y, x):
        d = self.get_4_direction_value(values, y, x)
        r_list = [None] * 4
        for ind in range(4):
            r_list[ind] = d[ind - 4] * self.noise[0] + d[ind - 3] * self.noise[1] \
                          + d[ind - 1] * self.noise[2] + d[ind - 2] * self.noise[3]
        return r_list

    def get_policy(self, values, *exist_policy):
        policy = exist_policy[0] if exist_policy else copy.deepcopy(self.grid)
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if self.grid[y][x] == 'X':
                    d = self.get_rewards(values, y, x)
                    for i, is_wall in enumerate(self.is_wall(y, x)):
                        if is_wall:
                            d[i] = float('-inf')
                    policy[y][x] = d.index(max(d))
        return policy

    def print_policy(self):
        policy_char = {0: '↑', 1: '←', 2: '↓', 3: '→'}
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if self.grid[y][x] == 'X':
                    print(policy_char[self.policy[y][x]], '\t', end='')
                else:
                    print('#', '\t', end='')
            print()
        print()

    def print_value(self):
        for line in self.values:
            for v in line:
                print(format(v, '.5f'), '\t', end='')
            print()
        print()


class ValueIteration(MDP):
    def __init__(self, grid, grid_len, gamma, noise):
        MDP.__init__(self, grid, grid_len, gamma, noise)

        values, last_values = self.init_value()
        delta = 0.01
        value_sum, last_value_sum = 2 * delta, 0
        while delta < abs((value_sum - last_value_sum) / value_sum):
            value_sum, last_value_sum = 0, value_sum
            for y in range(grid_len):
                for x in range(grid_len):
                    if grid[y][x] == 'X':
                        values[y][x] = self.get_r(last_values, y, x)
                        value_sum += values[y][x]
            values, last_values = last_values, values
        self.values = values
        self.policy = self.get_policy(values)

    def get_r(self, values, y, x):
        d = self.get_4_direction_value(values, y, x)
        r = [None] * 4
        for ind in range(4):
            r[ind] = d[ind - 4] * self.noise[0] + d[ind - 3] * self.noise[1] \
                     + d[ind - 1] * self.noise[2] + d[ind - 2] * self.noise[3]
        return self.gamma * max(r)


class PolicyIteration(MDP):
    def __init__(self, grid, grid_len, gamma, noise):
        MDP.__init__(self, grid, grid_len, gamma, noise)
        values, last_values = self.init_value()
        policy, last_policy = self.init_policy()
        self.yx2i, self.i2yx = self.gen_yx2i()
        len_i = len(self.i2yx)

        while self.policy_not_equal(policy, last_policy):
            self.mat_1 = np.eye(len_i)
            self.mat_2 = np.zeros((len_i, 1))
            for i, (y, x) in enumerate(self.i2yx):
                direct_list = [(y - 1, x), (y, x - 1), (y + 1, x), (y, x + 1)]
                ii_list = [-4, -3, -1, -2]
                ind = policy[y][x]
                for _i, ii in enumerate(ii_list):
                    _y, _x = direct_list[ind + ii]
                    self.set_mat(i, _y, _x, self.noise[_i])

            ans = np.linalg.solve(self.mat_1, self.mat_2)
            for i in range(len_i):
                y, x = self.i2yx[i]
                values[y][x] = ans[i, 0]

            last_policy, policy = policy, last_policy
            policy = self.get_policy(values, policy)
        self.values = values
        self.policy = policy

    def set_mat(self, i, y, x, noise):
        if -1 < x < self.grid_len and -1 < y < self.grid_len:
            if self.grid[y][x] == 'X':
                self.mat_1[i, self.yx2i[(y, x)]] = -noise * self.gamma
            else:
                self.mat_2[i, 0] += noise * self.grid[y][x] * self.gamma

    def init_policy(self):
        policy = copy.deepcopy(self.grid)
        last_policy = copy.deepcopy(self.grid)
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if policy[y][x] == 'X':
                    policy[y][x] = random.randint(0, 4)
                    last_policy[y][x] = 0
        return policy, last_policy

    def policy_not_equal(self, policy, last_policy):
        for y in range(self.grid_len):
            for x in range(self.grid_len):
                if policy[y][x] != last_policy[y][x]:
                    return True
        return False

    def get_r(self, value, policy, y, x):
        d = self.get_4_direction_value(value, y, x)
        ind = policy[y][x]
        r = d[ind - 4] * self.noise[0] + d[ind - 3] * self.noise[1] \
            + d[ind - 1] * self.noise[2] + d[ind - 2] * self.noise[3]
        return self.gamma * r


if __name__ == '__main__':
    DP = DataPreprocess('input_100.txt')
    Grid_Len, Gamma, Noise, Grid = DP.out

    t = time()
    VI = ValueIteration(Grid, Grid_Len, Gamma, Noise)
    t_VI = time() - t
    # VI.print_value()
    print('Value Iteration:', t_VI * 1000, 'ms')
    VI.print_policy()

    t = time()
    PI = PolicyIteration(Grid, Grid_Len, Gamma, Noise)
    t_PI = time() - t
    # PI.print_value()
    print('Policy Iteration:', t_PI * 1000, 'ms')
    PI.print_policy()
