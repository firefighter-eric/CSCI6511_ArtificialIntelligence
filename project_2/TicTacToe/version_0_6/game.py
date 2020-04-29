import numpy as np


class Game:
    def __init__(self, n, m):
        self.N = n
        self.M = m
        self.Board = np.zeros((n, n), dtype=np.int8)
        self.move_count = 0
        self.SIGNAL = ('-', 'X', 'O')
        self.SIGNAL_2 = ('-', 'x', 'o')
        self.last_move = None

    def __str__(self):
        print('Step:', self.move_count,
              '\tPlayer:', self.SIGNAL[self.move_count % 2 + 1])
        print('\t', end='')
        for i in range(self.N):
            print(i, '\t', end='')
        print()
        for y, line in enumerate(self.Board):
            print(y, end='\t')
            for x, n in enumerate(line):
                if (y, x) == self.last_move:
                    print(self.SIGNAL_2[n], '\t', end='')
                else:
                    print(self.SIGNAL[n], '\t', end='')
            print()
        return '\n'

    def input(self, y, x, player):
        # out   1: win
        #      -1: tie
        #       0: not end
        if self.Board[y, x]:
            print('illegal input! x:', x, 'y:', y)
        self.move(y, x, player)
        self.last_move = (y, x)
        print(self)
        out = self.check_win(y, x, player)
        return out

    def move(self, y, x, player):
        self.Board[y, x] = player
        self.move_count += 1

    def check_win(self, y, x, player):
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
                return 1
        if self.move_count == self.N ** 2:
            print('Tie')
            return -1
        else:
            return 0

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
