from evaluate_function import EvaluateFunction
import numpy as np
from cnn import CNN


class Tree:
    def __init__(self, n, m, depth):
        self.EF = EvaluateFunction(n, m)
        self.cnn = CNN(n, m)
        self.Depth = depth
        self.IntMax = 2e32
        self.Count = 0
        self.N = n

    def search(self, state):
        if not np.any(state, 0):
            return 0, self.N // 2 * self.N + self.N // 2

        v, out_state = self.alpha_beta(state, self.Depth, -self.IntMax, self.IntMax, True)
        next_move = np.where(state != out_state)[0][0]
        print('Count:', self.Count)
        return v, next_move

    def alpha_beta(self, state, depth, alpha, beta, max_player):
        player = 1 if depth % 2 == 1 else -1
        self.Count += 1
        next_state = self.cnn.cal_next_state(state, player)

        # print(next_state_seq)

        if not len(next_state):
            return self.EF.cal(state.reshape((1, -1)))

        if depth == 0:
            return self.EF.cal_min(next_state)

        next_state_seq = [(n, i) for i, n in enumerate(self.EF.cal(next_state))]
        next_state_seq.sort()
        next_state_sorted = [next_state[n[1]] for n in next_state_seq]
        next_state = next_state_sorted

        if depth == self.Depth:
            v = -self.IntMax
            state_out = None
            for s in next_state:
                _v = self.alpha_beta(s, depth - 1, alpha, beta, False)
                if v <= _v:
                    v = _v
                    state_out = s
                alpha = max(alpha, v)
            return v, state_out

        # if self.EF.is_win(state, player):
        #     return self.IntMax * player

        if max_player:
            v = -self.IntMax
            for s in next_state:
                v = max(v, self.alpha_beta(s, depth - 1, alpha, beta, False))
                alpha = max(alpha, v)
                if beta <= alpha:
                    # print(depth)
                    break
            return v
        else:
            v = self.IntMax
            for s in next_state:
                v = min(v, self.alpha_beta(s, depth - 1, alpha, beta, True))
                beta = min(beta, v)
                if beta <= alpha:
                    # print(2)
                    break
            return v

    @staticmethod
    def cal_next_state(state, player):
        # states        (N*N, )
        # next_state    (n, N*N)
        zero = np.where(state == 0)[0]
        next_states = np.dot(np.ones((len(zero), 1)), state.reshape((1, -1)))

        for i, n in enumerate(zero):
            next_states[i, n] = player
        return next_states
