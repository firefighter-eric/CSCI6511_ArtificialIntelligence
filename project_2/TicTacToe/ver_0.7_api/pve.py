from game import Game
from tree import Tree
from save import Save
import time


class Pve:
    def __init__(self, n, m, depth, save_permission):
        self.N = n
        self.M = m
        self.DEPTH = depth
        self.SAVE_PERMISSION = save_permission

        self.G = Game(n, m)
        self.T = Tree(n, m, depth)

        # load cache
        self.S = Save(n, m, self.SAVE_PERMISSION)
        out = self.S.load()
        if out:
            print('loaded')
            self.T.EF.Hash = out

    def start_game(self):
        side = int(input('choose your side\n0: O, 1: X'))
        player_1 = 1 if side == 0 else -1
        # player_2 = -player_1

        print('Start\n', self.G)

        t = time.time()

        player = 1
        for i in range(100):
            if player == player_1:
                y, x = self.T.search(self.G.get_state() * player_1)
            else:
                y = int(input('y:'))
                if y < 0:
                    break
                x = int(input('x:'))
            if self.G.input(y, x, player):
                break
            player = -player

        t = time.time() - t
        print('Time:', t)

        # save cache
        self.S.save(self.T.EF.Hash)

        print('End')
