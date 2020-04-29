import numpy as np
from numba import njit, int8


class Feature:
    def __init__(self, n, m):
        self.N = n
        self.M = m
        self.n_feature = m
        self.rot = np.rot90(np.arange(n * n).reshape((n, n)))

    def cal(self, state):
        # state (N, N)
        # out   (n_feature,)
        out = cal_2_direction(state, self.N, self.M) + cal_2_direction(state.flatten()[self.rot], self.N, self.M)
        return out


@njit(int8[:](int8[:, :], int8, int8))
def cal_2_direction(state, n, m):
    # state (N, N)
    # out   (n_feature,)
    out = np.zeros((m,), dtype=np.int8)
    unseen1 = [[True] * n for _ in range(n)]
    unseen2 = [[True] * n for _ in range(n)]

    for y in range(n):
        for x in range(n - 1):
            if state[y, x] == 1 and state[y, x + 1] == 1 and unseen1[y][x]:
                count = 1
                for i in range(1, m):
                    _x = x + i
                    if _x < n and state[y, _x] == 1:
                        count += 1
                        unseen1[y][x] = False
                    else:
                        break

                quality = 0
                if -1 < x - 1 and state[y, x - 1] == 0:
                    quality += 1
                if x + count < n and state[y, x + count] == 0:
                    quality += 1

                if count == m:
                    out[-1] += 1
                elif quality != 0:
                    i = count + quality - 3
                    out[i] += 1

    for y in range(n - 1):
        for x in range(n - 1):
            if state[y, x] == 1 and state[y + 1, x + 1] == 1 and unseen2[y][x]:
                count = 1
                for i in range(1, m):
                    _x = x + i
                    _y = y + i
                    if _x < n and _y < n and state[_y, _x] == 1:
                        count += 1
                        unseen2[y][x] = False
                    else:
                        break

                quality = 0
                if -1 < x - 1 and -1 < y - 1 and state[y - 1, x - 1] == 0:
                    quality += 1
                if x + count < n and y + count < n and state[y + count, x + count] == 0:
                    quality += 1

                if count == m:
                    out[-1] += 1
                elif quality != 0:
                    i = count + quality - 3
                    out[i] += 1
    return out


if __name__ == '__main__':
    N, M = 3, 3
    F = Feature(N, M)

    State = np.zeros((N, N))

    # State[1, 2:7] = 1
    State[1, 1] = 1
    State[2, 2] = 1
    # State[3, 3] = 1

    # State = np.eye(3)
    State = np.array([[1, 0, -1],
                      [0, 1, 1],
                      [-1, -1, 1]], dtype=np.int8)
    Out = F.cal(State)
