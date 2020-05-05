import numpy as np


class Feature:
    def __init__(self, n, m):
        self.N = n
        self.M = m
        self.n_feature = m

    def cal(self, state):
        # state (N, N)
        # out   (n_feature,)
        # out = self.cal_2_direction(state, self.N, self.M) + self.cal_2_direction(np.rot90(state), self.N, self.M)
        out = self.cal_2_direction(state) + self.cal_2_direction(np.rot90(state))
        return out

    def cal_2_direction(self, state):
        # state (N, N)
        # out   (n_feature,)
        out = np.zeros((self.n_feature,))
        unseen1 = [[True] * self.N for _ in range(self.N)]
        unseen2 = [[True] * self.N for _ in range(self.N)]

        for y in range(self.N):
            for x in range(self.N - 1):
                if state[y, x] == 1 and state[y, x + 1] == 1 and unseen1[y][x]:
                    count = 1
                    for i in range(1, self.M):
                        _x = x + i
                        if _x < self.N and state[y, _x] == 1:
                            count += 1
                            unseen1[y][x] = False
                        else:
                            break

                    quality = 0
                    if -1 < x - 1 and state[y, x - 1] == 0:
                        quality += 1
                    if x + count < self.N and state[y, x + count] == 0:
                        quality += 1

                    if count == self.M:
                        out[-1] += 1
                    elif quality != 0:
                        i = count + quality - 3
                        out[i] += 1

        for y in range(self.N - 1):
            for x in range(self.N - 1):
                if state[y, x] == 1 and state[y + 1, x + 1] == 1 and unseen2[y][x]:
                    count = 1
                    for i in range(1, self.M):
                        _x = x + i
                        _y = y + i
                        if _x < self.N and _y < self.N and state[_y, _x] == 1:
                            count += 1
                            unseen2[y][x] = False
                        else:
                            break

                    quality = 0
                    if -1 < x - 1 and -1 < y - 1 and state[y - 1, x - 1] == 0:
                        quality += 1
                    if x + count < self.N and y + count < self.N and state[y + count, x + count] == 0:
                        quality += 1

                    if count == self.M:
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
                      [-1, -1, 1]])
    Out = F.cal(State)
