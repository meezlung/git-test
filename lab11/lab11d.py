from math import sqrt

# Cross product of OA and OB vectors: >0 for counter-clockwise turn
def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

# Build convex hull via Monotone Chain
def convex_hull(points):
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts

    lower = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    upper = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenate lower and upper, excluding duplicate endpoints
    return lower[:-1] + upper[:-1]

# Find farthest-pair squared distance using Rotating Calipers
def farthest_pair_distance2(hull):
    m = len(hull)
    if m < 2:
        return 0
    if m == 2:
        dx = hull[0][0] - hull[1][0]
        dy = hull[0][1] - hull[1][1]
        return dx*dx + dy*dy

    def dist2(a, b):
        dx = a[0] - b[0]
        dy = a[1] - b[1]
        return dx*dx + dy*dy

    max_d2 = 0
    j = 1
    for i in range(m):
        ni = (i + 1) % m
        # Advance j while area increases
        while True:
            curr = abs(cross(hull[i], hull[ni], hull[j]))
            nxt = abs(cross(hull[i], hull[ni], hull[(j + 1) % m]))
            if nxt > curr:
                j = (j + 1) % m
            else:
                break
        # Update max distance squared
        d2 = dist2(hull[i], hull[j])
        if d2 > max_d2:
            max_d2 = d2
        d2 = dist2(hull[ni], hull[j])
        if d2 > max_d2:
            max_d2 = d2

    return max_d2

# Main function: compute minimum required power
def min_power(positions):
    hull = convex_hull(positions)
    max_d2 = farthest_pair_distance2(hull)
    return sqrt(max_d2)

# print(min_power(((1, 1), (1, 0), (0, 1))))
# print(min_power(((1, 1), (1, 0), (1, 1))))
