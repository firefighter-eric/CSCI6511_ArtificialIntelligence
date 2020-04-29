import random
from queue import PriorityQueue
import time


class Preprocess:
    def __init__(self):
        self.V_Pos, self.N = self.read_v('v.txt')
        self.G = self.read_e('e.txt')

    @staticmethod
    def read_v(filename):
        def get_position(v):
            p = (v % 10, v // 10)
            return p

        f = open(filename, 'r')
        v_pos = []
        for line in f:
            if line.startswith('#'):
                continue
            _, square = line.strip().split(',')
            v_pos.append(get_position(int(square)))
        f.close()
        n = len(v_pos)
        return v_pos, n

    @staticmethod
    def read_e(filename):
        f = open(filename, 'r')
        g = {}
        for line in f:
            if line.startswith('#'):
                continue
            v1, v2, dist = [int(i) for i in line.strip().split(',')]

            if v1 not in g:
                g[v1] = {}
            g[v1][v2] = dist
            if v2 not in g:
                g[v2] = {}
            g[v2][v1] = dist
        f.close()
        return g


def initial(n):
    start = random.randint(0, n - 1)
    end = random.randint(0, n - 1)
    return start, end


def get_path(parent, dist, end):
    item = (dist, end)
    path = []
    while item in parent:
        path.append(item)
        item = parent[item]
    path.append(item)
    path.reverse()
    return path


def dijkstra(g, start, end):
    seen = set()  # vertex
    pq = PriorityQueue()  # (dist, vertex)
    pq.put((0, start))
    parent = {}  # (dist2, v2): (dist1, v1)

    while pq.queue:
        dist, v1 = pq.get()
        if v1 in seen:
            continue
        seen.add(v1)

        if v1 == end:
            path = get_path(parent, dist, end)
            return dist, path

        for v2 in g[v1]:
            if v2 in seen:
                continue
            dist_v2 = dist + g[v1][v2]
            pq.put((dist_v2, v2))
            parent[(dist_v2, v2)] = (dist, v1)
    return -1, []


def a_star(g, v_pos, start, end):
    end_x, end_y = v_pos[end]

    def cal_dist(v):
        delta_x, delta_y = abs(v_pos[v][0] - end_x), abs(v_pos[v][1] - end_y)
        delta_x -= 1 if delta_x > 1 else 0
        delta_y -= 1 if delta_y > 1 else 0
        return 10 * (delta_x ** 2 + delta_y ** 2) ** 0.5

    seen = {}  # vertex
    pq = PriorityQueue()  # (h, dist, vertex)
    pq.put((cal_dist(start), 0, start))
    parent = {}  # (dist2, v2): (dist1, v1)

    while pq.queue:
        h, dist, v1 = pq.get()
        if v1 in seen and h > seen[v1]:
            continue
        seen[v1] = h

        if v1 == end:
            path = get_path(parent, dist, end)
            return dist, path

        for v2 in g[v1]:
            if v2 in seen:
                continue
            dist_v2 = dist + g[v1][v2]
            h = cal_dist(v2)
            pq.put((dist_v2 + h, dist_v2, v2))  # f = h + g
            parent[(dist_v2, v2)] = (dist, v1)
    return -1, []


def path2str(path):
    return ' -> '.join([str(i[1]) for i in path])


if __name__ == '__main__':
    Data = Preprocess()
    Start, End = initial(Data.N)

    t = time.time()
    Dist1, Path1 = dijkstra(Data.G, Start, End)
    delta_t1 = time.time() - t

    t = time.time()
    Dist2, Path2 = a_star(Data.G, Data.V_Pos, Start, End)
    delta_t2 = time.time() - t

    print('Start:', Start, 'End:', End)
    print('Dijkstra\tDistance:', Dist1, 'Time:', int(delta_t1 * 1000), 'ms\tPath:', path2str(Path1))
    print('A star\t\tDistance:', Dist2, 'Time:', int(delta_t2 * 1000), 'ms\tPath:', path2str(Path2))
