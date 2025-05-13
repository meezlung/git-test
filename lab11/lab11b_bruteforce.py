from fractions import Fraction

Point = tuple[int,int]
Polygon = list[Point]

def extended_gcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def area2(poly: Polygon) -> int:
    A=0
    n=len(poly)
    for i in range(n):
        x1,y1=poly[i]
        x2,y2=poly[(i+1)%n]
        A+=x1*y2-x2*y1
    return abs(A)

def boundary_points(poly: Polygon) -> int:
    B=0
    n=len(poly)
    for i in range(n):
        x1,y1=poly[i]
        x2,y2=poly[(i+1)%n]
        dx=abs(x2-x1)
        dy=abs(y2-y1)
        B+=extended_gcd(dx,dy)[0]
    return B

def pick_count(poly: Polygon) -> int:
    if not poly:
        return 0
    A2=area2(poly)
    B=boundary_points(poly)
    return (A2 + B + 2)//2

# New helpers for degenerate cases:

def lattice_points_on_segment(p: Point, q: Point) -> set[Point]:
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    g = extended_gcd(abs(dx), abs(dy))[0]
    pts = set()
    if g == 0:
        pts.add(p)
    else:
        step = (dx//g, dy//g)
        for k in range(g+1):
            pts.add((p[0] + k*step[0], p[1] + k*step[1]))
    return pts


def lattice_points_triangle_int(p1: Point, p2: Point, p3: Point) -> set[Point]:
    # if degenerate (collinear), union points on edges
    if area2([p1,p2,p3]) == 0:
        pts = set()
        pts |= lattice_points_on_segment(p1,p2)
        pts |= lattice_points_on_segment(p2,p3)
        pts |= lattice_points_on_segment(p3,p1)
        return pts
    # else, generate interior + boundary via Pick's theorem enumeration
    # bounding box
    xs = [p1[0], p2[0], p3[0]]
    ys = [p1[1], p2[1], p3[1]]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    pts = set()
    # barycentric or area test
    def orient_int(a,b,c):
        return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            pt = (x,y)
            # check inside or on boundary
            w1 = orient_int(p1,p2,pt)
            w2 = orient_int(p2,p3,pt)
            w3 = orient_int(p3,p1,pt)
            if (w1>=0 and w2>=0 and w3>=0) or (w1<=0 and w2<=0 and w3<=0):
                pts.add(pt)
    return pts

# Main union count:
def union_tri_lattice_points(p1: Point, p2: Point, p3: Point,
                               p4: Point, p5: Point, p6: Point) -> int:

    # get sets of lattice points for each triangle
    pts1 = lattice_points_triangle_int(p1,p2,p3)
    pts2 = lattice_points_triangle_int(p4,p5,p6)

    # union count = |pts1| + |pts2| - |intersection|
    inter = pts1 & pts2
    return len(pts1) + len(pts2) - len(inter)

# # Example tests
# def test_cases():
#     print(union_tri_lattice_points((3,1),(2,3),(1,1),(3,1),(2,2),(2,0)))
#     print(union_tri_lattice_points((3,1),(2,3),(1,1),(3,1),(4,0),(2,0)))

# if __name__ == "__main__":
#     test_cases()

# print(union_tri_lattice_points((3, 1), (2, 3), (1, 1), (3, 1), (2, 2), (2, 0)))
# print(union_tri_lattice_points((3,1),(2,3),(1,1),(3,1),(4,0),(2,0)))
# print(union_tri_lattice_points((3,3),(0,0),(3,0),(2,1),(1,0),(2,0)))
# print(union_tri_lattice_points((3,3),(0,0),(3,0),(3,3),(0,0),(3,0)))
# print(union_tri_lattice_points((3,3),(0,0),(0,0),(0,0),(0,0),(0,0)))
# print(union_tri_lattice_points((3,3),(0,0),(0,0),(3,0),(0,0),(0,0)))