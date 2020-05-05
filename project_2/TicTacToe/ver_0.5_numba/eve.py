from game import Game
from tree import Tree
import time

N = 6
M = 4
DEPTH = 4

G = Game(N, M)
T1 = Tree(N, M, DEPTH)
T2 = Tree(N, M, DEPTH)

print('Start')
G.show()

t = time.time()

for i in range(30):
    if i % 2 == 0:
        Player = 1
        next_move = T1.search(G.get_state())
    else:
        Player = -1
        next_move = T2.search(-G.get_state())

    y, x = next_move
    if G.input(y, x, Player) != 0:
        break
    G.show()

t = time.time() - t
print('Time:', t)

G.show()
print('End')
