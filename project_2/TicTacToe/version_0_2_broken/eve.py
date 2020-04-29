from game import *
from tree import *
import time

N = 4
M = 3

G = Game(N, M)

depth = 5  # must be odd
T = Tree(N, M, depth)


print('Start')
print(G.Board)

t = time.time()
for i in range(10):
    Player = 1 if i % 2 == 0 else -1
    v, next_move = T.search(G.get_state() * Player)
    # print(v)
    x, y = next_move % N, next_move // N
    if G.input(y, x, Player) != 0:
        break
    print(G.Board)
t = time.time() - t
print('Time:', t)
print('End')
print(G.Board)
