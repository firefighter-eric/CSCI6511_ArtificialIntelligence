from game import Game
from tree import Tree
import time

N = 6
M = 4
DEPTH = 5

G = Game(N, M)
T1 = Tree(N, M, DEPTH)
T2 = Tree(N, M, DEPTH)

print('Start\n', G)

t = time.time()

for i in range(N**2):
    if i % 2 == 0:
        Player = 1
        next_move = T1.search(G.get_state())
    else:
        Player = -1
        next_move = T2.search(-G.get_state())

    y, x = next_move
    if G.input(y, x, Player):
        break

t = time.time() - t
print('Time:', t, '\nEnd')
