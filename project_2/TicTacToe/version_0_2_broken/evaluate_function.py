import numpy as np
from row import Row


class EvaluateFunction:
    def __init__(self, n, m):
        self.Base = np.array([10 ** (i + 1) for i in range(m - 1)])
        self.Base[-1] *= 10
        self.R = Row(n, m)

    def cal(self, state):
        row_score = self.R.cal_score(state, 1) - self.R.cal_score(state, -1)
        # print(row_score)
        return np.dot(self.Base, row_score)

    def is_win(self, state, player):
        return self.R.if_win(state, player)
