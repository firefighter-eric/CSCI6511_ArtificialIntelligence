import numpy as np
import numba as nb


class Feature:
    def __init__(self, n, m):
        self.N = n
        self.M = m
        self.n_feature = m - 1
        self.win_row = self.init_win_rows()
        self.rot = np.rot90(np.arange(n * n).reshape((n, n)))

    def init_win_rows(self):
        # win_row       (len_row, n, n)
        # win_row_out   (len_row, n * n)
        n, m = self.N, self.M
        len_row = (n * (n - m + 1) + (n - m + 1) ** 2) * 2
        win_row = np.zeros((len_row, n, n), dtype=np.int8)

        i = 0
        for j in range(n):
            for k in range(n - m + 1):
                win_row[i, j, k:k + m] = 1
                i += 1

        for j in range(n - m + 1):
            for k in range(n):
                win_row[i, j:j + m, k] = 1
                i += 1

        for j in range(n - m + 1):
            for k in range(n - m + 1):
                win_row[i, j:j + m, k:k + m] = np.eye(m)
                i += 1

        t = np.zeros((m, m))
        for ii in range(m):
            t[m - ii - 1, ii] = 1

        for j in range(n - m + 1):
            for k in range(n - m + 1):
                win_row[i, j:j + m, k:k + m] = t
                i += 1

        return win_row.reshape(-1, n * n)

    def cal(self, state):
        # state (N, N)
        # out   (n_feature,)
        without_o = np.dot(self.win_row, (state.reshape((self.N * self.N, 1)) == -1)) <= 0
        win = np.dot(self.win_row, state.reshape((self.N * self.N, 1)))[without_o]

        return win2out(win, self.n_feature)


@nb.njit(nb.int8[:](nb.int8[:], nb.int8))
def win2out(win, n_feature):
    out = np.zeros(n_feature, dtype=np.int8)
    for i, n in enumerate(win):
        if n > 1:
            out[n - 2] += 1
    return out


if __name__ == '__main__':
    N, M = 6, 5
    F = Feature(N, M)

    State = np.zeros((N, N), dtype=np.int8)

    # State[1, 2:7] = 1
    State[1, 1] = 1
    State[2, 2] = 1
    State[3, 3] = 1
    State[5, 5] = 1

    # State = np.eye(3)
    # State = np.array([[1, 0, -1],
    #                   [0, 1, 1],
    #                   [-1, -1, 1]], dtype=np.int8)
    Out = F.cal(State)
