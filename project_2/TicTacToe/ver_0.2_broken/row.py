import numpy as np


class Row:
    def __init__(self, n, m):
        self.RowNum = self.cal_row_num(n, m)
        self.Rows = self.init_rows(n, m)
        self.M = m

    @staticmethod
    def cal_row_num(n, m):
        row_num = []
        for i in range(2, m + 1):
            row_num.append(n * (n - i + 1) * 2 + (n - i + 1) ** 2 * 2)
        s = sum(row_num)
        # print(row_num, s, s * n ** 2)
        return row_num

    def init_rows(self, n, m):
        row = []
        for i in self.RowNum:
            row.append(np.zeros((i, n, n)))

        _m = 2
        for s in row:
            i = 0
            for j in range(n):
                for k in range(n - _m + 1):
                    s[i, j, k:k + _m] = 1
                    i += 1

            for j in range(n - _m + 1):
                for k in range(n):
                    s[i, j:j + _m, k] = 1
                    i += 1

            for j in range(n - _m + 1):
                for k in range(n - _m + 1):
                    s[i, j:j + _m, k:k + _m] = np.eye(_m)
                    i += 1

            t = np.zeros((_m, _m))
            for ii in range(_m):
                t[_m - ii - 1, ii] = 1

            for j in range(n - _m + 1):
                for k in range(n - _m + 1):
                    s[i, j:j + _m, k:k + _m] = t
                    i += 1
            _m += 1
            s.shape = (-1, n ** 2)
        return row

    def cal_score(self, state, player):
        row_score = np.empty((len(self.Rows),1))
        for i, row in enumerate(self.Rows):
            tmp = np.dot(row, state.reshape(-1, 1))
            row_score[i] = (tmp == (i + 2) * player).sum()
        return row_score

    def if_win(self, state, player):
        tmp = np.dot(self.Rows[-1], state.reshape(-1, 1))
        score = (tmp == self.M * player).sum()
        return score > 0


if __name__ == '__main__':
    R = Row(15, 5)
    S = R.Rows
    a = S[-1].reshape((-1, 225))
    b = a[-1].reshape(15, 15)
