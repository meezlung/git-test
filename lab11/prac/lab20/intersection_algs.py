from utils import Point, gcd, dot, cross, norm2, dist2, orient, on_segment, on_open_segment, segments_intersect, same_point

# --- Segment–Segment Unique Intersection -------------------------------

def segment_intersection_point(a, b, c, d):
    """
    Unique intersection of closed segments AB and CD.
    Returns (Xnum, Ynum, Den) or a unit‐denominator point if one segment is a point.
    Returns None if:
      - they do not meet,
      - or they overlap in >1 point (collinear overlap).
    """
    # degenerate cases: A==B or C==D
    if same_point(a,b):
        return (a.x, a.y, 1) if on_segment(c, d, a) else None
    if same_point(c,d):
        return (c.x, c.y, 1) if on_segment(a, b, c) else None

    v = b - a
    w = d - c
    denom = cross(v, w)
    if denom == 0:
        # parallel or collinear—no unique point
        return None

    num_t = cross(c - a, w)
    num_u = cross(c - a, v)
    # check t,u in [0,1]
    if denom > 0:
        if not (0 <= num_t <= denom and 0 <= num_u <= denom):
            return None
    else:
        if not (denom <= num_t <= 0 and denom <= num_u <= 0):
            return None

    Xnum = a.x*denom + v.x*num_t
    Ynum = a.y*denom + v.y*num_t
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom


# --- Ray–Line Segment ---------------------------------------------------

def ray_segment_intersection_point(r0, r1, a, b):
    """
    Intersection of ray R0→R1 (t>=0) with closed segment AB (u in [0,1]).
    Degenerate cases:
      • If R is a point (R0==R1), falls back to point-on-segment.
      • If AB is a point, falls back to point-on-ray.
    Returns (Xnum, Ynum, Den) or None.
    """
    # degenerate ray
    if same_point(r0, r1):
        return (r0.x, r0.y, 1) if on_segment(a, b, r0) else None
    # degenerate segment
    if same_point(a, b):
        # point A on ray?
        v = r1 - r0
        if orient(r0, r1, a) == 0:
            # check t>=0  ⇒  dot(a−r0, v) >= 0
            if dot(a - r0, v) >= 0:
                return (a.x, a.y, 1)
        return None

    v = r1 - r0
    w = b - a
    denom = cross(v, w)
    if denom == 0:
        return None

    num_t = cross(a - r0, w)
    num_u = cross(a - r0, v)
    # t>=0 and 0<=u<=1
    if denom > 0:
        if num_t < 0 or not (0 <= num_u <= denom):
            return None
    else:
        if num_t > 0 or not (denom <= num_u <= 0):
            return None

    Xnum = r0.x*denom + v.x*num_t
    Ynum = r0.y*denom + v.y*num_t
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom


# --- Line–Segment -------------------------------------------------------

def line_segment_intersection(a, b, c, d):
    """
    Intersection of infinite line AB with closed segment CD.
    Degenerate cases:
      • If CD is a point, same as line-point check.
      • If AB is a point, same as segment-point check.
    Returns (Xnum, Ynum, Den) or None.
    """
    # degenerate line AB
    if same_point(a, b):
        return (a.x, a.y, 1) if on_segment(c, d, a) else None
    # degenerate segment CD
    if same_point(c, d):
        return (c.x, c.y, 1) if orient(a, b, c) == 0 else None

    v = b - a
    w = d - c
    denom = cross(v, w)
    if denom == 0:
        return None

    num_t = cross(c - a, w)
    num_u = cross(c - a, v)
    # only u in [0,1] matters
    if denom > 0:
        if not (0 <= num_u <= denom):
            return None
    else:
        if not (denom <= num_u <= 0):
            return None

    Xnum = a.x*denom + v.x*num_t
    Ynum = a.y*denom + v.y*num_t
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom


# --- Ray–Line ----------------------------------------------------------

def ray_line_intersection(r0, r1, c, d):
    """
    Intersection of ray R0→R1 (t>=0) with infinite line CD.
    Degenerate cases:
      • If R is a point, same as point-on-line.
      • If CD is a point, same as ray-on-point.
    Returns (Xnum, Ynum, Den) or None.
    """
    # degenerate ray
    if same_point(r0, r1):
        return (r0.x, r0.y, 1) if orient(c, d, r0) == 0 else None
    # degenerate line CD
    if same_point(c, d):
        # point‐on‐ray?
        v = r1 - r0
        if orient(r0, r1, c) == 0 and dot(c - r0, v) >= 0:
            return (c.x, c.y, 1)
        return None

    v = r1 - r0
    w = d - c
    denom = cross(v, w)
    if denom == 0:
        return None

    num_t = cross(c - r0, w)
    # t>=0
    if denom > 0:
        if num_t < 0:
            return None
    else:
        if num_t > 0:
            return None

    Xnum = r0.x*denom + v.x*num_t
    Ynum = r0.y*denom + v.y*num_t
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom


# --- Line–Line ----------------------------------------------------------

def line_line_intersection(a, b, c, d):
    """
    Intersection of infinite lines AB and CD.
    Degenerate cases:
      • If AB is a point, same as point-on-line CD.
      • If CD is a point, same as point-on-line AB.
    Returns (Xnum, Ynum, Den) or None.
    """
    # degeneracies
    if same_point(a, b):
        return (a.x, a.y, 1) if orient(c, d, a) == 0 else None
    if same_point(c, d):
        return (c.x, c.y, 1) if orient(a, b, c) == 0 else None

    v = b - a
    w = d - c
    denom = cross(v, w)
    if denom == 0:
        return None
    num = cross(c - a, w)
    Xnum = a.x*denom + v.x*num
    Ynum = a.y*denom + v.y*num
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom


# --- Ray–Ray ------------------------------------------------------------

def ray_ray_intersection(r0, r1, s0, s1):
    """
    Intersection of rays R0→R1 and S0→S1.
    Degenerate cases:
      • If either ray is a point, fall back to point-on-ray & point-on-other-ray.
    Returns (Xnum, Ynum, Den) or None.
    """
    # degenerate rays
    if same_point(r0, r1):
        return (r0.x, r0.y, 1) if on_segment(s0, s1, r0) else None
    if same_point(s0, s1):
        return (s0.x, s0.y, 1) if on_segment(r0, r1, s0) else None

    v = r1 - r0
    w = s1 - s0
    denom = cross(v, w)
    if denom == 0:
        return None

    num_t = cross(s0 - r0, w)
    num_u = cross(s0 - r0, v)
    # t>=0, u>=0
    if denom > 0:
        if num_t < 0 or num_u < 0:
            return None
    else:
        if num_t > 0 or num_u > 0:
            return None

    Xnum = r0.x*denom + v.x*num_t
    Ynum = r0.y*denom + v.y*num_t
    if denom < 0:
        denom, Xnum, Ynum = -denom, -Xnum, -Ynum
    return Xnum, Ynum, denom
