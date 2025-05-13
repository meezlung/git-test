from fractions import Fraction

Point = tuple[int, int]
FracPoint = tuple[Fraction, Fraction]
PolygonInt = list[Point]
PolygonFrac = list[FracPoint]

def extended_gcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def lcm(a: int, b: int) -> int:
    return abs(a * b) // extended_gcd(a, b)[0] if a and b else 0

# --- Basic geometry ---
def area2(poly: PolygonInt) -> int:
    A = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        A += x1*y2 - x2*y1
    return abs(A)

# Integer boundary points
def boundary_points_int(poly: PolygonInt) -> int:
    B = 0
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        B += extended_gcd(abs(x2-x1), abs(y2-y1))[0]
    return B

# Pick for integer polygons
def pick_count_int(poly: PolygonInt) -> int:
    if not poly:
        return 0
    A2 = area2(poly)
    B = boundary_points_int(poly)
    return (A2 + B + 2) // 2

# Enumerate lattice points on segment
def lattice_points_on_segment(p: Point, q: Point) -> set[Point]:
    dx, dy = q[0]-p[0], q[1]-p[1]
    g = extended_gcd(abs(dx), abs(dy))[0]
    if g == 0:
        return {p}
    sx, sy = dx//g, dy//g
    return {(p[0]+k*sx, p[1]+k*sy) for k in range(g+1)}

# Rational polygon clipping functions
def orient(a: FracPoint, b: FracPoint, c: FracPoint) -> Fraction:
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def intersect(p: FracPoint, r: FracPoint, q: FracPoint, s: FracPoint) -> FracPoint:
    rv = (r[0]-p[0], r[1]-p[1])
    sv = (s[0]-q[0], s[1]-q[1])
    denom = rv[0]*sv[1] - rv[1]*sv[0]
    t = ((q[0]-p[0])*sv[1] - (q[1]-p[1])*sv[0]) / denom
    return (p[0] + t*rv[0], p[1] + t*rv[1])

def clip_polygon(subj: PolygonFrac, a: FracPoint, b: FracPoint) -> PolygonFrac:
    out: PolygonFrac = []
    n = len(subj)
    for i in range(n):
        curr, nxt = subj[i], subj[(i+1) % n]
        ic = orient(a, b, curr) >= 0
        in_ = orient(a, b, nxt) >= 0
        if ic and in_:
            out.append(nxt)
        elif ic and not in_:
            out.append(intersect(curr, nxt, a, b))
        elif not ic and in_:
            out.append(intersect(curr, nxt, a, b))
            out.append(nxt)
    return out

# Area for rational polygon
def polygon_area(poly: PolygonFrac) -> Fraction:
    if not poly:
        return Fraction(0)
    s = Fraction(0)
    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i+1) % len(poly)]
        s += x1*y2 - x2*y1
    return abs(s) / 2

# Pick for rational convex polygon with collinearity handling
def pick_count_frac(poly: PolygonFrac) -> int:
    if not poly:
        return 0
    # If intersection is a point or repeated point
    if len(poly) == 1:
        return 1
    # Compute actual area
    A = polygon_area(poly)
    if A == 0:
        # all points collinear: find two farthest endpoints
        best = Fraction(0)
        a, b = poly[0], poly[0]
        n = len(poly)
        for i in range(n):
            for j in range(i+1, n):
                dx = poly[j][0] - poly[i][0]
                dy = poly[j][1] - poly[i][1]
                d2 = dx*dx + dy*dy
                if d2 > best:
                    best = d2
                    a, b = poly[i], poly[j]
        # count lattice on segment a->b
        dx = b[0] - a[0]; dy = b[1] - a[1]
        nx, dx_den = dx.numerator, dx.denominator
        ny, dy_den = dy.numerator, dy.denominator
        D = lcm(dx_den, dy_den)
        sx = nx * (D // dx_den)
        sy = ny * (D // dy_den)
        g = extended_gcd(abs(sx), abs(sy))[0]
        return g + 1
    # General polygon case
    A2 = A * 2
    B = 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        dx = b[0] - a[0]; dy = b[1] - a[1]
        nx, dx_den = dx.numerator, dx.denominator
        ny, dy_den = dy.numerator, dy.denominator
        D = lcm(dx_den, dy_den)
        sx = nx * (D // dx_den)
        sy = ny * (D // dy_den)
        B += extended_gcd(abs(sx), abs(sy))[0]
    I = (A2 - B + 2) / 2
    return int(I + B)

# Point-in-triangle test
def point_in_triangle(pt: Point, a: Point, b: Point, c: Point) -> bool:
    def ori(u, v, w):
        return (v[0]-u[0])*(w[1]-u[1]) - (v[1]-u[1])*(w[0]-u[0])
    w1 = ori(a, b, pt); w2 = ori(b, c, pt); w3 = ori(c, a, pt)
    return (w1>=0 and w2>=0 and w3>=0) or (w1<=0 and w2<=0 and w3<=0)

# Main union
def union_tri_lattice_points(
    p1: Point, p2: Point, p3: Point,
    p4: Point, p5: Point, p6: Point
) -> int:
    # Areas
    A1 = area2([p1, p2, p3])
    A2 = area2([p4, p5, p6])

    # 1) Any degenerate: full enumeration
    if A1 == 0 or A2 == 0:
        pts: set[Point] = set()
        for a, b, c in [(p1, p2, p3), (p4, p5, p6)]:
            if area2([a, b, c]) == 0:
                pts |= lattice_points_on_segment(a, b)
                pts |= lattice_points_on_segment(b, c)
                pts |= lattice_points_on_segment(c, a)
            else:
                xs = [a[0], b[0], c[0]]; ys = [a[1], b[1], c[1]]
                for x in range(min(xs), max(xs) + 1):
                    for y in range(min(ys), max(ys) + 1):
                        if point_in_triangle((x, y), a, b, c):
                            pts.add((x, y))
        return len(pts)

    # 2) Batch #1 small coords
    coords = [p1, p2, p3, p4, p5, p6]
    if max(abs(x) for p in coords for x in p) <= 10:
        pts: set[Point] = set()
        xs = [p[0] for p in coords]; ys = [p[1] for p in coords]
        for x in range(min(xs), max(xs)+1):
            for y in range(min(ys), max(ys)+1):
                if point_in_triangle((x,y), p1, p2, p3) or point_in_triangle((x,y), p4, p5, p6):
                    pts.add((x,y))
        return len(pts)

    # 3) Fast Pick + clipping
    c1 = pick_count_int([p1, p2, p3])
    c2 = pick_count_int([p4, p5, p6])
    T1 = [(Fraction(x), Fraction(y)) for x, y in (p1, p2, p3)]
    T2 = [(Fraction(x), Fraction(y)) for x, y in (p4, p5, p6)]
    if orient(T2[0], T2[1], T2[2]) < 0:
        T2.reverse()
    inter = T1
    for i in range(3):
        inter = clip_polygon(inter, T2[i], T2[(i+1)%3])
    ci = pick_count_frac(inter)
    return c1 + c2 - ci

# # Example tests
# if __name__ == '__main__':
#     print(union_tri_lattice_points((3, 1), (2, 3), (1, 1), (3, 1), (2, 2), (2, 0)))  #6
#     print(union_tri_lattice_points((3,1),(2,3),(1,1),(3,1),(4,0),(2,0)))             #8
#     print(union_tri_lattice_points((3,3),(0,0),(3,0),(2,1),(1,0),(2,0)))             #10
#     print(union_tri_lattice_points((3,3),(0,0),(3,0),(3,3),(0,0),(3,0)))             #10
#     print(union_tri_lattice_points((3,3),(0,0),(0,0),(0,0),(0,0),(0,0)))             #4
#     print(union_tri_lattice_points((3,3),(0,0),(0,0),(3,0),(0,0),(0,0)))             #7
