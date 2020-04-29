import tensorflow as tf
import numpy as np


class Filter:
    def __init__(self, n, m):
        self.filters, self.filter_index = self.init_filter(m)

    @staticmethod
    def init_filter(m):
        filters = []
        filter_index = []

        for _m in range(2, m + 1):
            f1 = np.eye(_m)
            f2 = np.rot90(f1)
            f3 = np.zeros((_m, _m))
            f3[_m // 2, :] = 1
            f4 = np.rot90(f3)
            filter_index.append(_m)

            _filter = np.empty(shape=(_m, _m, 1, 4))
            _filter[:, :, 0, 0] = f1
            _filter[:, :, 0, 1] = f2
            _filter[:, :, 0, 2] = f3
            _filter[:, :, 0, 3] = f4
            filters.append(tf.constant(_filter, shape=(_m, _m, 1, 4), dtype=tf.int32))
        return filters, filter_index


class CNN:
    def __init__(self, n, m):
        ft = Filter(n, m)
        self.filters, self.filter_index = ft.filters, ft.filter_index
        self.N = n
        self.filter_next_state = tf.constant(np.ones((5, 5)), shape=(5, 5, 1, 1))

    def cal(self, state):
        # state (batch, N*N)
        # scores (batch, filter_num)
        batch, n = state.shape
        scores = np.empty((batch, len(self.filter_index)))
        res = np.empty(())
        for i, _filter in enumerate(self.filters):
            output = tf.nn.conv2d(state.reshape((-1, self.N, self.N, 1)), _filter,
                                  strides=[1, 1, 1, 1], padding='SAME')
            scores[:, i] = np.sum(output.numpy().reshape((batch, -1)) == self.filter_index[i], axis=1)
        return scores

    def cal_next_state(self, state, player):
        # states        (N*N, )
        # next_state    (batch, N*N)
        state_abs = np.abs(state)
        output = tf.nn.conv2d(state_abs.reshape((1, self.N, self.N, 1)), self.filter_next_state,
                              strides=[1, 1, 1, 1], padding='SAME')
        next_state = output.numpy().reshape((-1,)) > 0

        position = np.where(next_state - state_abs == 1)[0]

        next_states = np.dot(np.ones((len(position), 1)), state.reshape((1, -1)))

        for i, n in enumerate(position):
            next_states[i, n] = player
        return next_states


if __name__ == '__main__':
    N = 12
    M = 5
    f = Filter(N, M)
    a = f.filters
    # print(f.filters)
    cnn = CNN(N, M)
    # State = np.array([np.eye(15) * -1, np.eye(15)]).reshape(2, -1)
    # s = cnn.cal(State)

    State = (np.eye(12) * -1).reshape((-1,))
    NextState = cnn.cal_next_state(State, 1)
    print(NextState)
