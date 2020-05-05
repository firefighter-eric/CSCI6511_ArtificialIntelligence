from evaluate_function import  EvaluateFunction


class Tree:
    def __init__(self, n, m):
        self.EF = EvaluateFunction(n, m)
        self.Depth = 7
        self.IntMax = 2e32
        self.count = 0

    def search(self, state):
        node = (state, [])  # (state, path)
        ab = self.alpha_beta(node, self.Depth, -self.IntMax, self.IntMax, True)
        return ab

    def alpha_beta(self, node, depth, alpha, beta, max_player):
        player = 1 if depth % 2 == 1 else -1
        next_state = self.cal_next_state(node, player)
        if depth == 0 or not next_state:
            state, path = node
            return self.EF.cal(state), path
        if max_player:
            v, path = -self.IntMax, []
            for n in next_state:
                _v, _path = self.alpha_beta(n, depth - 1, alpha, beta, False)
                if v < _v:
                    v, path = _v, _path
                alpha = max(alpha, v)
                if beta < alpha:
                    break
            return v, path
        else:
            v, path = self.IntMax, []
            for n in next_state:
                _v, _path = self.alpha_beta(n, depth - 1, alpha, beta, True)
                if _v < v:
                    v, path = _v, _path
                beta = min(beta, v)
                if beta < alpha:
                    break
            return v, path

    @staticmethod
    def cal_next_state(node, player):
        state, path = node
        next_states = []
        for i, s in enumerate(state):
            if s == 0:
                _state = state.copy()
                _state[i] += player
                _path = path.copy()
                _path.append(i * player)
                next_states.append((_state, _path))
        return next_states
