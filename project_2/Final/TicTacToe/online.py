from game import Game
from tree import Tree
from save import Save
from api import Api
import time


class Online:
    def __init__(self, n, m, depth, save_permission, user_id, team_id, game_id):
        self.N = n
        self.M = m
        self.DEPTH = depth
        self.SAVE_PERMISSION = save_permission
        self.SLEEP_TIME = 5

        self.G = Game(n, m)
        self.T = Tree(n, m, depth)
        self.API = Api(user_id, team_id)
        self.API.set_game_id(game_id)

        # load cache
        self.S = Save(n, m, self.SAVE_PERMISSION)
        out = self.S.load()
        if out:
            print('loaded')
            self.T.EF.Hash = out

    def start_game(self):
        # first move: O
        side = int(input('choose side\n0: O, 1: X'))
        player = 1 if side == 1 else -1

        print('Start\n', self.G)

        while True:
            while True:
                players_turn = self.G.input_board_list(self.API.get_board())
                if players_turn == player:
                    break
                else:
                    print('Waiting for Player', 'X' if players_turn == 1 else 'O')
                    time.sleep(self.SLEEP_TIME)
            print(self.G)

            t = time.time()
            y, x = self.T.search(self.G.get_state() * player)
            print('Time:', time.time() - t)

            self.API.make_move(y, x)
            if self.G.input(y, x, player):
                break

        # save cache
        self.S.save(self.T.EF.Hash)

        print('End')
