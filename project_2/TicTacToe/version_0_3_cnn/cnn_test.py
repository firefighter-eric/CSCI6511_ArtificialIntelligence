import tensorflow as tf
import numpy as np
import time

if __name__ == '__main__':
    N = 10
    M = 10
    n_filter = 1
    state = np.eye(N).reshape((1, N, N, 1))
    filter1 = tf.Variable(tf.eye(M * int(n_filter**0.5)))
    filter1 = tf.reshape(filter1, (M, M, 1, n_filter))
    state = np.eye(N).reshape((1, N, N, 1))
    # x = state + filter1
    # print(filter1)
    # y = tf.add(x, filter1)
    t1 = time.time()
    for i in range(1):
        y = tf.nn.conv2d(state, filter1, strides=[1, 1, 1, 1], padding='VALID')
        y = y.numpy().reshape(n_filter, -1)
        # a = (1 == y).sum(axis=1)
    print(time.time() - t1)
