from utils import Point, gcd, dot, cross, norm2, dist2, orient, on_segment, on_open_segment, segments_intersect, same_point

def closest_pair(points: list[Point]):
    pts = sorted(points, key=lambda p: (p.x, p.y))
    def rec(l: int, r: int):
        if r - l <= 3:
            dmin = 10**30
            for i in range(l, r):
                for j in range(i+1, r):
                    d = dist2(pts[i], pts[j])
                    if d < dmin:
                        dmin = d
            pts[l:r] = sorted(pts[l:r], key=lambda p: p.y)
            return dmin
        m = (l + r)//2
        midx = pts[m].x
        d = min(rec(l, m), rec(m, r))
        merged = []
        i, j = l, m
        while i < m or j < r:
            if j == r or (i < m and pts[i].y < pts[j].y):
                merged.append(pts[i]); i += 1
            else:
                merged.append(pts[j]); j += 1
        pts[l:r] = merged
        strip = [p for p in pts[l:r] if (p.x - midx)**2 < d]
        for i in range(len(strip)):
            for j in range(i+1, min(i+7, len(strip))):
                d2 = dist2(strip[i], strip[j])
                if d2 < d:
                    d = d2
        return d
    return rec(0, len(pts))

def convex_hull(points):
    pts = sorted(set((p.x, p.y) for p in points))
    pts = [Point(x,y) for x,y in pts]
    if len(pts) <= 1:
        return pts
    lower = []
    for p in pts:
        while len(lower) >= 2 and orient(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and orient(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]

def farthest_pair(points):
    hull = convex_hull(points)
    m = len(hull)
    if m == 0:
        return None
    if m == 1:
        return (hull[0], hull[0], 0)
    j = 1
    maxd = 0
    pair = (hull[0], hull[1])
    for i in range(m):
        ni = (i+1) % m
        while True:
            nj = (j+1) % m
            cur = abs(cross(hull[ni] - hull[i], hull[nj] - hull[i]))
            prev = abs(cross(hull[ni] - hull[i], hull[j] - hull[i]))
            if cur > prev:
                j = nj
            else:
                break
        d = dist2(hull[i], hull[j])
        if d > maxd:
            maxd = d
            pair = (hull[i], hull[j])
    return (pair[0], pair[1], maxd)