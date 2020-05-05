from eve import Eve
from pve import Pve
from online import Online


class Config:
    N = 12
    M = 6
    DEPTH = 4
    SAVE_PERMISSION = False


def main():
    c = Config()
    mode = int(input('choose game mode:\n0: eve, 1: pve, 2:online'))
    if mode == 0:
        g = Eve(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION)
    elif mode == 1:
        g = Pve(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION)
    elif mode == 2:
        # user_id = input('user id:')
        # team_id = input('team id:')
        game_id = input('game id:')
        fast_list = [[848, 1201, game_id], [923, 1216, game_id]]
        ind = int(input('fast list:\n0: 848, 1:923'))
        user_id, team_id, game_id = fast_list[ind]
        g = Online(c.N, c.M, c.DEPTH, c.SAVE_PERMISSION, user_id, team_id, game_id)
    g.start_game()
    return g


if __name__ == '__main__':
    G = main()
