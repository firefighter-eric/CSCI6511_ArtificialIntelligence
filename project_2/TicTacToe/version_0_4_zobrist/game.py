import numpy as np


class Game:
    def __init__(self, n, m):
        self.Board = np.zeros((n, n), dtype=np.int)
        self.N = n
        self.M = m
        self.MoveCount = 0

    def input(self, y, x, player):
        if self.Board[y, x] != 0:
            print('illegal input! x:', x, 'y:', y)
        self.move(y, x, player)
        w = self.check_win(y, x, player)

        return w

    def get_state(self):
        # out   (N, N)
        return self.Board.copy()

    def move(self, y, x, player):
        self.Board[y, x] = player
        self.MoveCount += 1

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
                print(player, 'win!')
                return 1
        if self.MoveCount == self.N ** 2:
            print('Tie')
            return -1
        else:
            return 0

    def show(self):
        print('\t', end='')
        [print(i, '\t', end='') for i in range(self.N)]
        print()
        for i, b in enumerate(self.Board):
            print(i, end='')
            for j in b:
                if j == 1:
                    print('\tX', end='')
                elif j == -1:
                    print('\tO', end='')
                else:
                    print('\t-', end='')
            print()
        print()


if __name__ == '__main__':
    g = Game(8, 5)

    # g.input(0, 2, 1)
    # g.input(1, 1, 1)
    # g.input(2, 0, 1)
    g.Board[2:7, 4] = 1
    Win = g.check_win(6, 4, 1)

    g.show()
