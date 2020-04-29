import numpy as np


class Zobrist:
    def __init__(self, n):
        self.board_b = np.random.randint(2 ** 60, size=(n, n))
        self.board_w = np.random.randint(2 ** 60, size=(n, n))
        self.dict = {}

    def get(self, state):
        _hash = self.get_hash(state)
        if _hash in self.dict:
            return self.dict[_hash]
        else:
            return False

    def put(self, state, value):
        _hash = self.get_hash(state)
        self.dict[_hash] = value

    def get_hash(self, state):
        _hash = 0
        state_b = state == 1
        state_w = state == -1
        for i in self.board_b[state_b]:
            _hash ^= i
        for i in self.board_w[state_w]:
            _hash ^= i
        return _hash


if __name__ == '__main__':
    N, M = 3, 3
    Zob = Zobrist(N)

    # State = np.eye(N)

    State1 = np.array([[1, 0, -1],
                       [0, 1, 1],
                       [-1, -1, 1]])
    Out1 = Zob.get(State1)
    Zob.put(State1, 5)
