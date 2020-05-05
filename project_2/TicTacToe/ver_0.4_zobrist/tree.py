from evaluate_function import EvaluateFunction
from zobrist import Zobrist
import numpy as np


class Tree:
    def __init__(self, n, m, depth):
        self.EF = EvaluateFunction(n, m)
        self.Depth = depth
        self.IntMax = 2e60
        self.Count = 0
        self.N = n
        self.Hash = None

    def search(self, state):
        # state (N, N)
        if not np.any(state):
            return self.N // 2, self.N // 2

        self.Hash = Zobrist(self.N)
        out_state = self.alpha_beta(state, self.Depth, -self.IntMax, self.IntMax, 1)
        next_move = np.where(state != out_state)
        # print(state, out_state)
        # print(out_state, next_move)
        print('Count:', self.Count)
        y, x = next_move
        return y[0], x[0]

    def alpha_beta(self, state, depth, alpha, beta, player):
        # state (N, N)
        self.Count += 1
        next_state = self.cal_next_state(state, player)

        # zobrist hash
        hash_value = self.Hash.get(state)
        if hash_value:
            return hash_value

        if depth == 0 or not len(next_state):
            # print(state, self.EF.cal(state))
            return self.EF.cal(state)

        # next_state_seq = [(self.EF.cal(n), i) for i, n in enumerate(next_state)]
        # next_state_seq.sort(reverse=True)
        # next_state_sorted = [next_state[n[1]] for n in next_state_seq]
        # next_state = next_state_sorted

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

        is_win = self.EF.is_win(state)
        if is_win:
            # print('win\n', state, is_win)
            return is_win * depth
            # return 2e30 * depth

        if player == 1:
            v = -self.IntMax
            for s in next_state:
                v = max(v, self.alpha_beta(s, depth - 1, alpha, beta, -1))
                alpha = max(alpha, v)
                if beta <= alpha:
                    # print(depth)
                    break
            self.Hash.put(state, v)
            return v
        else:
            v = self.IntMax
            for s in next_state:
                v = min(v, self.alpha_beta(s, depth - 1, alpha, beta, 1))
                beta = min(beta, v)
                if beta <= alpha:
                    # print(2)
                    break
            self.Hash.put(state, v)
            return v

    def cal_next_state(self, state, player):
        # state        (N, N)
        # next_state    (batch, N, N)
        next_move_set = set()
        for x in range(self.N):
            for y in range(self.N):
                if state[y, x] != 0:
                    for _x in (-2, -1, 0, 1, 2):
                        for _y in (-2, -1, 0, 1, 2):
                            next_move_set.add((x + _x, y + _y))

        next_move = []
        for x, y in next_move_set:
            if -1 < x < self.N and -1 < y < self.N and state[y, x] == 0:
                next_move.append((x, y))
        # zero = np.where(state.flatten() == 0)
        # print(state, zero)
        # batch = len(zero)
        batch = len(next_move)
        # print(next_move)
        next_states = np.dot(np.ones((batch, 1)), state.reshape((1, -1))).reshape(batch, self.N, self.N)

        for i, (x, y) in enumerate(next_move):
            next_states[i, y, x] = player
        return next_states
