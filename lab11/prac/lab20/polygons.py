from utils import Point, gcd, dot, cross, norm2, dist2, orient, on_segment, on_open_segment, segments_intersect, same_point

def is_simple_polyline(pts: list[Point]):
    """
    True iff:
      - ≥2 points
      - no zero-length edges
      - no 180° turns (collinear triples)
      - no non-adjacent segment intersections
    """
    n = len(pts)
    if n < 2:
        return False
    # zero-length edges
    for i in range(n-1):
        if same_point(pts[i], pts[i+1]):
            return False
    # straight angles
    for i in range(1, n-1):
        if orient(pts[i-1], pts[i], pts[i+1]) == 0:
            return False
    # self-intersection
    for i in range(n-1):
        a1, b1 = pts[i], pts[i+1]
        for j in range(i+2, n-1):
            # skip sharing at endpoints
            if j == i or j == i+1:
                continue
            if segments_intersect(a1, b1, pts[j], pts[j+1]):
                return False
    return True

def is_simple_polygon(poly):
    """
    True iff:
      - ≥3 vertices
      - no zero-length edges
      - no 180° turns (collinear triples)
      - no self-intersections beyond shared endpoints
    """
    n = len(poly)
    if n < 3:
        return False
    # zero-length edges
    for i in range(n):
        if same_point(poly[i], poly[(i+1)%n]):
            return False
    # straight angles
    for i in range(n):
        a, b, c = poly[i-1], poly[i], poly[(i+1)%n]
        if orient(a, b, c) == 0:
            return False
    # self-intersections
    for i in range(n):
        a1, b1 = poly[i], poly[(i+1)%n]
        for j in range(i+1, n):
            if j == i or j == (i+1)%n or i == (j+1)%n:
                continue
            a2, b2 = poly[j], poly[(j+1)%n]
            if segments_intersect(a1, b1, a2, b2):
                return False
    return True
    
def ensure_valid_polygon(poly, name="polygon"):
    if not is_simple_polygon(poly):
        raise ValueError(f"{name} is not a simple polygon")
    return poly

def area2(poly: list[Point]):
    ensure_valid_polygon(poly)

    A2 = 0
    n = len(poly)
    for i in range(n):
        A2 += cross(poly[i], poly[(i+1)%n])
    return abs(A2) # note that if A2 (signed area) is negative, then one reverses the enumeration of the vertices

    # if vertices are enumerated CCW, then A2 is positive, otherwise negative

def picks_theorem(poly: list[Point]):
    """
    A = i + b/2 - 1
    returns (i, b, A2)
    """
    ensure_valid_polygon(poly)
    A2 = area2(poly)
    B = 0
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i].x, poly[i].y
        x1, y1 = poly[(i+1)%n].x, poly[(i+1)%n].y
        B += gcd(abs(x1 - x0), abs(y1 - y0))
    I = (A2 - B + 2) // 2
    return I, B, A2

