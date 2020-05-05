from evaluate_function import EvaluateFunction
from zobrist import Zobrist
import numpy as np
import numba as nb


class Tree:
    def __init__(self, n, m, depth):
        self.N = n
        self.Depth = depth

        self.EF = EvaluateFunction(n, m)
        self.Hash = None

        self.IntMax = 2e60
        self.Count = 0

    def search(self, state):
        # state (N, N)
        if not np.any(state):
            return self.N // 2, self.N // 2

        self.Hash = Zobrist(self.N)
        out_state = self.alpha_beta(state, self.Depth, -self.IntMax, self.IntMax, 1)
        next_move = np.where(state != out_state)

        print('Count:', self.Count)
        y, x = next_move
        return y[0], x[0]

    def alpha_beta(self, state, depth, alpha, beta, player):
        # state       (N, N)    int8
        # v           ()        int64
        # state_out   (N, N)    int8
        self.Count += 1

        # zobrist hash
        hash_value = self.Hash[state]
        if hash_value:
            return hash_value

        # check if end
        next_state = self.cal_next_state(state, player)
        if depth == 0 or not len(next_state):
            return self.EF.cal(state)

        next_state_seq = [(self.EF.cal(n), i) for i, n in enumerate(next_state)]
        next_state_seq.sort(reverse=player == 1)
        next_state_sorted = [next_state[n[1]] for n in next_state_seq]
        next_state = next_state_sorted

        # top layer
        if depth == self.Depth:
            v = -self.IntMax
            state_out = None
            for s in next_state:
                _v = self.alpha_beta(s, depth - 1, alpha, beta, -1)
                if v < _v:
                    v = _v
                    state_out = s
                alpha = max(alpha, v)
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

    def cal_next_state(self, state, player):
        # state        (N, N)
        # next_state    (batch, N, N)
        next_position = cal_next_position(state)
        batch = len(next_position)
        next_states = np.repeat(state.reshape((1, self.N, self.N)), batch, axis=0)

        for i, (y, x) in enumerate(next_position):
            next_states[i, y, x] = player

        return next_states


@nb.njit
def cal_next_position(state):
    # state     (N, N)
    # next_move (batch, 2)
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
    return next_move


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
    Out = T.cal_next_state(State, 1)
    print(Out)
