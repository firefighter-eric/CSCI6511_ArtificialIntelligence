import numpy as np
from cnn import CNN


class EvaluateFunction:
    def __init__(self, n, m):
        self.Base = np.array([10 ** (i + 1) for i in range(m - 1)]).reshape((-1, 1))
        self.Base[-1] *= 10
        self.cnn = CNN(n, m)

    def cal(self, state):
        # state (batch, N*N)
        # score (batch, filter_num)
        # out   (batch,)
        row_score = self.cnn.cal(state) - self.cnn.cal(-state)
        # print(row_score)
        return np.dot(row_score, self.Base).reshape(-1)

    def cal_min(self, state):
        score = self.cal(state).reshape(-1,)
        return score.min()

    def is_win(self, state, player):
        return self.R.if_win(state, player)
