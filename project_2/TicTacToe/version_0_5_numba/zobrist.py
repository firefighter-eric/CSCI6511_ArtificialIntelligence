import numpy as np
from numba import njit, int64, int8


class Zobrist:
    def __init__(self, n):
        self.board_b = np.random.randint(2 ** 60, size=(n, n))
        self.board_w = np.random.randint(2 ** 60, size=(n, n))
        self.dict = {}

    def __getitem__(self, state):
        _hash = get_hash(state, self.board_b, self.board_w)
        if _hash in self.dict:
            return self.dict[_hash]
        else:
            return False

    def __setitem__(self, state, value):
        _hash = get_hash(state, self.board_b, self.board_w)
        self.dict[_hash] = value


@njit(int64(int8[:, :], int64[:, :], int64[:, :]))
def get_hash(state, board_b, board_w):
    _hash = 0
    n = state.shape[0]
    for y in range(n):
        for x in range(n):
            if state[y, x] == 1:
                _hash ^= board_b[y, x]
            elif state[y, x] == 0:
                _hash ^= board_w[y, x]
    return _hash


if __name__ == '__main__':
    N, M = 3, 3
    Zob = Zobrist(N)

    # State = np.eye(N)

    State1 = np.array([[1, 0, -1],
                       [0, 1, 1],
                       [-1, -1, 1]], dtype=np.int8)
    Out1 = Zob[State1]
    Zob[State1] = 5
    Out2 = Zob[State1]
