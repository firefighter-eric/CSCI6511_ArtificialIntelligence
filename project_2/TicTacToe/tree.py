from evaluate_function import EvaluateFunction
from zobrist import Zobrist
import numpy as np
import numba as nb


class Tree:
    def __init__(self, n, m, depth):
        self.N = n
        self.DEPTH = depth

        self.EF = EvaluateFunction(n, m)
        self.Hash = None

        self.IntMax = 2e60
        # self.Count = 0

    def search(self, state):
        # state (N, N)
        if not np.any(state):
            return self.N // 2, self.N // 2

        self.Hash = Zobrist(self.N)
        out_state = self.alpha_beta(state, self.DEPTH, -self.IntMax, self.IntMax, 1)
        next_move = np.where(state != out_state)

        # print('Count:', self.Count)
        y, x = next_move
        return y[0], x[0]

    def alpha_beta(self, state, depth, alpha, beta, player):
        # state       (N, N)    int8
        # player      1 or -1   int8
        # v           value     int64
        # state_out   (N, N)    int8
        # self.Count += 1

        # end: depth = 0
        if depth == 0:
            return self.EF.cal(state)

        # end: no next_state
        next_state = cal_next_states(state, player)
        if depth == 0 or not len(next_state):
            return self.EF.cal(state)

        # zobrist hash
        hash_value = self.Hash[state]
        if hash_value:
            return hash_value

        # sort state if depth > 1
        if depth > 1:
            next_state_val = np.array([self.EF.cal(n) for n in next_state])
            next_state_index = np.argsort(next_state_val)
            if player == 1:
                next_state_index = next_state_index[::-1]
            next_state = next_state[next_state_index]

        # top layer
        if depth == self.DEPTH:
            state_out = None
            for s in next_state:
                _v = self.alpha_beta(s, depth - 1, alpha, beta, -1)
                if alpha < _v:
                    alpha = _v
                    state_out = s
            return state_out

        # pruning: check if win
        is_win = self.EF.is_win(state)
        if is_win:
            return is_win * depth

        # pruning: alpha-beta pruning
        if player == 1:
            v = -self.IntMax
            for s in next_state:
                v = max(v, self.alpha_beta(s, depth - 1, alpha, beta, -1))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
            return v
        else:
            v = self.IntMax
            for s in next_state:
                v = min(v, self.alpha_beta(s, depth - 1, alpha, beta, 1))
                beta = min(beta, v)
                if beta <= alpha:
                    break
        self.Hash[state] = v
        return v


@nb.njit(nb.int8[:, :, :](nb.int8[:, :], nb.int8))
def cal_next_states(state, player):
    # state         (N, N)          int8
    # next_states   (batch, N, N)   int8
    n = state.shape[0]
    next_move = []
    unseen = [[True] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if state[y, x] != 0:
                for _x in (-2, -1, 0, 1, 2):
                    for _y in (-2, -1, 0, 1, 2):
                        iy, ix = y + _y, x + _x
                        if -1 < ix < n and -1 < iy < n and state[iy, ix] == 0:
                            if unseen[iy][ix]:
                                next_move.append((iy, ix))
                                unseen[iy][ix] = False

    batch = len(next_move)
    next_states = np.empty((batch, n, n), dtype=np.int8)
    for i, (y, x) in enumerate(next_move):
        next_states[i] = state
        next_states[i, y, x] = player
    return next_states


if __name__ == '__main__':
    N, M = 6, 3
    T = Tree(N, M, 5)

    State = np.zeros((N, N), dtype=np.int8)

    # State[1, 2:7] = 1
    State[0, 0] = -1
    State[1, 1] = -1
    State[2, 2] = -1
    # State[3, 3] = 1

    # State = np.eye(3)
    # State = np.array([[1, 0, -1],
    #                   [0, 1, 1],
    #                   [-1, -1, 1]])
    Out = cal_next_states(State, 1)
    print(Out)
