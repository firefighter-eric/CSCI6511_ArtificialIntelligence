from game import *
from tree import *
import time

N = 10

M = 5
DEPTH = 4

G = Game(N, M)
T = Tree(N, M, DEPTH)

print('Start\n', G)

t = time.time()

side = int(input('choose your side\n0: white, 1:black'))

for i in range(100):
    if i % 2 == side:
        Player = 1
        next_move = T.search(G.get_state() * Player)
        y, x = next_move
    else:
        Player = -1
        y = int(input('y:'))
        if y < 0:
            break
        x = int(input('x:'))

    if G.input(y, x, Player):
        break

t = time.time() - t
print('Time:', t, '\nEnd')
