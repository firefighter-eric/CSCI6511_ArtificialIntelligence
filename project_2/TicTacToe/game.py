import numpy as np


class Game:
    def __init__(self, n, m):
        self.N = n
        self.M = m

        self.Board = np.zeros((n, n), dtype=np.int8)
        self.SIGNAL = ('-', 'X', 'O')
        self.SIGNAL_2 = ('-', 'x', 'o')
        self.last_move = ((None, None), None)  # ((y, x), player)

    def __str__(self):
        print('Step:', np.sum(np.abs(self.Board)), '\tPlayer:', self.last_move[1])
        print('\t', end='')
        for i in range(self.N):
            print(i, '\t', end='')
        print()
        for y, line in enumerate(self.Board):
            print(y, end='\t')
            for x, n in enumerate(line):
                if (y, x) == self.last_move[0]:
                    print(self.SIGNAL_2[n], '\t', end='')
                else:
                    print(self.SIGNAL[n], '\t', end='')
            print()
        return ''

    def input(self, y, x, player):
        # out   True: win or tie
        #       False: not end
        if self.Board[y, x]:
            print('illegal input! x:', x, 'y:', y)
        self.Board[y, x] = player
        self.last_move = ((y, x), player)
        print(self)
        out = self.check_win(y, x, player)
        return out

    def input_board_list(self, board_list):
        # player X moves first
        # board_list    (N * N,)
        # next_player   1 or -1
        self.Board = np.array(board_list, dtype=np.int8).reshape((self.N, self.N))
        c_x = np.count_nonzero(self.Board == 1)
        c_o = np.count_nonzero(self.Board == -1)
        next_player = -1 if c_x == c_o else 1
        return next_player

    def check_win(self, y, x, player):
        # out: if end
        incs = ((0, 1), (0, -1),
                (1, 0), (-1, 0),
                (1, 1), (-1, -1),
                (-1, 1), (1, -1))
        record = []
        for inc in incs:
            count, i = 0, 0
            _x, _y = x + inc[0], y + inc[1]
            while -1 < _x < self.N and -1 < _y < self.N and i < self.M:
                if self.Board[_y, _x] != player:
                    break
                count += 1
                _x += inc[0]
                _y += inc[1]
                i += 1
            record.append(count)

        for i in range(0, 8, 2):
            if record[i] + record[i + 1] + 1 >= self.M:
                print(self.SIGNAL[player], 'win!')
                return True
        if np.all(self.Board):
            print('Tie')
            return True
        else:
            return False

    def get_state(self):
        # out   (N, N)
        return self.Board.copy()


if __name__ == '__main__':
    g = Game(8, 5)

    g.input(0, 2, 1)
    g.input(1, 1, 1)
    g.input(2, 0, 1)
    g.Board[2:7, 4] = 1
    Win = g.check_win(6, 4, 1)

    print(g)
