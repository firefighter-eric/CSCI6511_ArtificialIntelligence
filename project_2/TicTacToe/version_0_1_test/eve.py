from game import *
from tree import *

N = 3
M = 3

G = Game(N, M)
T = Tree(N, M)

print('Start')
for i in range(9):
    Player = 1 if i % 2 == 0 else -1
    v, path = T.search(G.get_state()*Player)
    next_move = path[0]
    x, y = next_move % N, next_move // N
    print(G.Board)
    if G.input(y, x, Player) != 0:
        break
print(G.Board)
print('End')
