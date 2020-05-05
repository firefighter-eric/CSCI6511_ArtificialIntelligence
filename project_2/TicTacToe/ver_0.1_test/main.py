from game import *
from row import *
from evaluate_function import *
from tree import *

N = 10
M = 5

G = Game(N, M)
G.input(0, 0, 1)
G.input(1, 1, 1)
G.input(2, 2, -1)
G.input(3, 3, -1)
G.input(4, 4, -1)
G.input(2, 0, 1)

print(G.Board)
State = G.get_state()

print('Row')
R = Row(N, M)
row_score1 = R.cal_score(State, 1)
row_score2 = R.cal_score(State, -1)
print(row_score1, row_score2)

print('EvaluateFunction')
EF = EvaluateFunction(N, M)
g = EF.cal(State)
print(g)

print('Tree')
T = Tree(N, M)
v, path = T.search(State, 1)
print(v, path)
next_move = path[0]
x = next_move % N
y = next_move // N
G.input(y, x, 1)

print(G.Board)
