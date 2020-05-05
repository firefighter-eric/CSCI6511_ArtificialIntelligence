from game import Game
from tree import Tree

N = 4
M = 3

G = Game(N, M)
T = Tree(N, M)

print('Start')
print(G.Board)

for i in range(100):
    if i % 2 == 0:
        Player = 1
        v, next_move = T.search(G.get_state() * Player)
        # print(v)
        x, y = next_move % N, next_move // N
    else:
        Player = -1
        y = int(input('y'))
        x = int(input('x'))
    if G.input(y, x, Player) != 0:
        break
    print(G.Board)

print(G.Board)
print('End')
