import random
from queue import PriorityQueue


class Edge:
    def __init__(self, distance, cost):
        self.distance = distance
        self.cost = cost


class Preprocess:
    def __init__(self, file):
        self.V2S, self.N = self.read_v(file + '//v.txt')
        self.G, self.E = self.read_e(file + '//e.txt')

    @staticmethod
    def read_v(filename):
        f = open(filename, 'r')
        v2s = []
        for line in f:
            if line.startswith('#'):
                continue
            index, square = line.strip().split(',')
            v2s.append(int(square))
        n = len(v2s)
        return v2s, n

    @staticmethod
    def cal_distance(p1, p2):
        x1, y1, x2, y2 = p1 % 10, p1 // 10, p2 % 10, p2 // 10
        distance = 10 * ((abs(x1 - x2) - 1) ** 2 + (abs(y1 - y2) - 1) ** 2) ** 0.5
        return distance

    def read_e(self, filename):
        f = open(filename, 'r')
        g = {}
        e = {}
        for line in f:
            if line.startswith('#'):
                continue
            v1, v2, cost = line.strip().split(',')
            v1, v2, cost = int(v1), int(v2), int(cost)
            distance = self.cal_distance(self.V2S[v1], self.V2S[v2])

            if v1 not in g:
                g[v1] = []
            g[v1].append(v2)
            if v2 not in g:
                g[v2] = []
            g[v2].append(v1)
            e[(v1, v2)] = Edge(distance, cost)
            e[(v2, v1)] = Edge(distance, cost)
        return g, e


def initial(n):
    start = random.randint(0, n)
    end = random.randint(0, n)
    return start, end


def dijkstra(g, e, start, end):
    seen = set()
    pq = PriorityQueue()
    pq.put((0, start))
    parent = {(0, start): (0, start)}
    cost = 0
    while pq.queue:
        priority, v1 = pq.get()
        if v1 in seen:
            continue
        seen.add(v1)
        # cost
        v_last = parent[(priority, v1)][1]
        if v1 != v_last:
            cost += e[(v1, v_last)].cost

        # end
        if v1 == end:
            key = (priority, v1)
            li = [key]
            while key[1] != start:
                key = parent[key]
                li.append(key)
            li.reverse()
            return priority, cost, li

        for v2 in g[v1]:
            if v2 not in seen:
                p = priority + e[(v1, v2)].distance
                pq.put((p, v2))
                parent[(p, v2)] = (priority, v1)
    return -1, cost, -1


Data = Preprocess('graphs/graph2000_0.1')
# Start, End = initial(N)
Start, End = 0, 99
Distance, Cost, L, = dijkstra(Data.G, Data.E, Start, End)
