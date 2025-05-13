# lab11e.py
from collections.abc import Sequence
from math import hypot, inf
import heapq

Point = tuple[int, int]
Rect  = tuple[float, float, float, float]  # xmin, ymin, xmax, ymax

class Bond:
    def __init__(self, buildings: Sequence[tuple[Point, Point]]):
        # store each building as (xmin, ymin, xmax, ymax)
        self.rects = []
        for (a, b), (c, d) in buildings:
            self.rects.append((float(a), float(b),
                               float(c), float(d)))

        # cache all four corners of every rect
        pts = set()
        for xmin, ymin, xmax, ymax in self.rects:
            pts |= {
                (xmin, ymin),
                (xmin, ymax),
                (xmax, ymin),
                (xmax, ymax),
            }
        self.corner_pts = list(pts)

    def shortest_path(self, p: Point, r: Point) -> float | None:
        # 1) build the full node list for this query
        nodes = [
            (float(p[0]), float(p[1])),
            (float(r[0]), float(r[1])),
            *self.corner_pts
        ]
        N = len(nodes)

        # 2) nested visibility test that looks at exactly this `nodes` list
        def blocked(i: int, j: int) -> bool:
            x1, y1 = nodes[i]
            x2, y2 = nodes[j]
            dx, dy = x2 - x1, y2 - y1

            for xmin, ymin, xmax, ymax in self.rects:
                # Compute t‐interval where segment is *strictly inside* the open rectangle (xmin,xmax)×(ymin,ymax).
                # If that open interval overlaps (0,1), we block.
                if dx == 0:
                    # vertical line: x=x1; check if that x lies strictly inside the open slab
                    if not (xmin < x1 < xmax):
                        continue
                    # for y we still look at the open interval
                    t_enter, t_exit = (ymin - y1) / dy, (ymax - y1) / dy
                    t_min, t_max = min(t_enter, t_exit), max(t_enter, t_exit)
                elif dy == 0:
                    # horizontal line: y=y1
                    if not (ymin < y1 < ymax):
                        continue
                    t_enter, t_exit = (xmin - x1) / dx, (xmax - x1) / dx
                    t_min, t_max = min(t_enter, t_exit), max(t_enter, t_exit)
                else:
                    # oblique segment: intersect open x‐ and y‐slabs
                    t1, t2 = (xmin - x1)/dx, (xmax - x1)/dx
                    tx_min, tx_max = min(t1, t2), max(t1, t2)
                    t3, t4 = (ymin - y1)/dy, (ymax - y1)/dy
                    ty_min, ty_max = min(t3, t4), max(t3, t4)
                    t_min, t_max = max(tx_min, ty_min), min(tx_max, ty_max)

                # Now (t_min, t_max) is exactly where the segment is *strictly inside* the rectangle.
                # If that open interval overlaps (0,1), we block it:
                if t_min < t_max and t_min < 1 and t_max > 0:
                    return True

            return False
        # 3) build visibility graph
        adj = [[] for _ in range(N)]
        for i in range(N):
            for j in range(i+1, N):
                if not blocked(i, j):
                    d = hypot(nodes[i][0] - nodes[j][0],
                                   nodes[i][1] - nodes[j][1])
                    adj[i].append((j, d))
                    adj[j].append((i, d))

        # 4) Dijkstra from node 0 → node 1
        dist = [inf]*N
        dist[0] = 0.0
        pq = [(0.0, 0)]
        while pq:
            d,u = heapq.heappop(pq)
            if u == 1:
                return d
            if d > dist[u]:
                continue
            for v,w in adj[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

        return None

bond = Bond([
    ((1, 1), (2, 2)),
])

assert abs(bond.shortest_path((0, 0), (3, 3)) - 4.47213595499957939) < 1e-8

bond = Bond([
    ((3, 3), (5, 7)),
    ((1, 1), (3, 5)),
])

print(bond.shortest_path((4, 1), (2, 6)))
assert abs(bond.shortest_path((4, 1), (2, 6)) - 8.41421356237309505) < 1e-8

bond = Bond([
    ((0, 0), (1, 1)),
    ((1, 1), (2, 2)),
])

assert abs(bond.shortest_path((2, 0), (0, 2)) - 4.0) < 1e-8
