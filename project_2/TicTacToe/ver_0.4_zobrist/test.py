import numpy as np
import time
N = 10000

a = np.arange(10)

t = time.time()
for i in range(N):
    b = np.bitwise_xor.reduce(a)
t1 = time.time() - t

t = time.time()
c = 0
for i in range(N):
    for n in a:
        c ^= i
t2 = time.time() - t

print(t2/t1)
