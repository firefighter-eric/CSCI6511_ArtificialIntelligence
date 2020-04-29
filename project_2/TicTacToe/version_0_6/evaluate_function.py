import numpy as np
from feature import Feature
from zobrist import Zobrist


class EvaluateFunction:
    def __init__(self, n, m):
        self.FT = Feature(n, m)
        self.Hash = Zobrist(n)
        self.BASE = np.array([10 ** i for i in range(self.FT.n_feature)])
        # self.BASE[-1] *= 10
        self.BIAS = np.array([[n - abs(n // 2 - i) - abs(n // 2 - j) for i in range(n)]
                              for j in range(n)]).flatten()

    def cal(self, state):
        # state (N, N)
        # score (n_feature,)
        # out   ()
        hash_score = self.Hash[state]
        if hash_score is False:
            score = self.FT.cal(state) - self.FT.cal(-state)
            self.Hash[state] = score
        else:
            score = hash_score
        out = np.dot(score, self.BASE)
        out += np.dot(state.flatten(), self.BIAS)
        return out

    def is_win(self, state):
        # state (N, N)
        # out   ()
        hash_score = self.Hash[state]
        if hash_score is False:
            score = self.FT.cal(state) - self.FT.cal(-state)
            self.Hash[state] = score
        else:
            score = hash_score
        out = score[-1] * self.BASE[-1]
        return out


if __name__ == '__main__':
    N, M = 5, 3
    EF = EvaluateFunction(N, M)

    # State = np.eye(N)

    # State = np.array([[1, 0, -1],
    #                   [0, 1, 1],
    #                   [-1, -1, 1]], dtype=np.int8)
    # Out = EF.cal(State)
    # Win = EF.is_win(State)
