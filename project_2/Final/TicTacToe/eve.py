from game import Game
from tree import Tree
from save import Save
import time


class Eve:
    def __init__(self, n, m, depth, save_permission):
        self.N = n
        self.M = m
        self.DEPTH = depth
        self.SAVE_PERMISSION = save_permission

        self.G = Game(n, m)
        self.T1 = Tree(n, m, depth)
        self.T2 = Tree(n, m, depth)

        # load cache
        self.S = Save(n, m, self.SAVE_PERMISSION)
        out = self.S.load()
        if out:
            print('loaded')
            self.T1.EF.Hash = out
            self.T2.EF.Hash = out

    def start_game(self):
        # first move: X
        print('Start\n', self.G)

        t = time.time()

        for i in range(20):
            if i % 2 == 0:
                player = 1
                next_move = self.T1.search(self.G.get_state())
            else:
                player = -1
                next_move = self.T1.search(-self.G.get_state())

            y, x = next_move
            if self.G.input(y, x, player):
                break

        t = time.time() - t
        print('Time:', t)

        # save cache
        self.S.save(self.T1.EF.Hash, self.T2.EF.Hash)

        print('End')
