from fractions import Fraction

Point = tuple[int,int]

# Helper: convert raw ints to Fraction‐points
def Fpt(p):
    return (Fraction(p[0]), Fraction(p[1]))

# Signed "twice area" (cross product) of triangle a,b,c
def orient(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

# Exact intersection of the line segments curr->nxt with clip‐edge a->b
def intersect(p, r, q, s):
    rv = (r[0]-p[0], r[1]-p[1])
    sv = (s[0]-q[0], s[1]-q[1])
    denom = rv[0]*sv[1] - rv[1]*sv[0]
    # assume denom ≠ 0 when called (i.e. not parallel)
    t = ((q[0]-p[0])*sv[1] - (q[1]-p[1])*sv[0]) / denom
    return (p[0] + t*rv[0], p[1] + t*rv[1])

# Sutherland–Hodgman: clip convex 'subj' polygon by half‐plane a->b (keep orient(a,b,pt) ≥ 0)
def clip_polygon(subj: list[tuple[Fraction,Fraction]],
                    a: tuple[Fraction,Fraction],
                    b: tuple[Fraction,Fraction]) -> list[tuple[Fraction,Fraction]]:
    out = []
    n = len(subj)
    for i in range(n):
        curr = subj[i]
        nxt  = subj[(i+1)%n]
        ic = orient(a,b,curr) >= 0
        in_ = orient(a,b,nxt ) >= 0
        if ic and in_:
            out.append(nxt)
        elif ic and not in_:
            out.append(intersect(curr,nxt,a,b))
        elif not ic and in_:
            out.append(intersect(curr,nxt,a,b))
            out.append(nxt)
        # else both out → nothing
    return out

# Absolute polygon area via shoelace
def polygon_area(pts: list[tuple[Fraction,Fraction]]) -> Fraction:
    if not pts:
        return Fraction(0)
    s = Fraction(0)
    for i in range(len(pts)):
        x1,y1 = pts[i]
        x2,y2 = pts[(i+1)%len(pts)]
        s += x1*y2 - x2*y1
    return abs(s) / 2

def union_tri_area(p1: Point, p2: Point, p3: Point, p4: Point, p5: Point, p6: Point) -> Fraction:

    # Build Fraction‐point lists
    T1 = list(map(Fpt, (p1,p2,p3)))
    T2 = list(map(Fpt, (p4,p5,p6)))

    # Compute their areas
    A1 = polygon_area(T1)
    A2 = polygon_area(T2)

    # Handle degeneracy: if either is zero‐area, union is just the other
    if A1 == 0 and A2 == 0:
        return Fraction(0)
    if A1 == 0:
        return A2
    if A2 == 0:
        return A1

    # Ensure T2 is CCW so that its interior is on the "left" of each edge
    if orient(T2[0], T2[1], T2[2]) < 0:
        T2.reverse()

    # Clip T1 by each edge of T2 to get the intersection polygon
    inter = T1
    for i in range(3):
        a, b = T2[i], T2[(i+1)%3]
        inter = clip_polygon(inter, a, b)

    # Intersection area
    Ai = polygon_area(inter)

    # Union area = A1 + A2 − intersection
    return A1 + A2 - Ai

# print(union_tri_area((3, 1), (2, 3), (1, 1), (3, 1), (2, 2), (2, 0)))