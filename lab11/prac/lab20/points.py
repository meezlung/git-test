from utils import Point, gcd, dot, cross, norm2, dist2, orient, on_segment, on_open_segment, segments_intersect, same_point

def on_closed_segment(a: Point, b: Point, p: Point): 
    # true if point p is in the closed line segment (a,b)
    return orient(a, b, p) == 0 and dot(p - a, p - b) <= 0

def on_open_segment(a: Point, b: Point, p: Point):
    # true if point p is in the closed line segment (a,b)
    return orient(a, b, p) == 0 and dot(p - a, p - b) < 0

def line_intersection(a: Point, b: Point, c: Point, d: Point):
    # intersection of lines ab and cd
    v = b - a 
    w = d - c
    denom = cross(v, w)
    if denom == 0:
        return None # collinear/parallel
    
    P_x_numerator = a.x * cross(v, w) + v.x * cross(c - a, w)
    P_y_numerator  = a.y * cross(v, w) + v.y * cross(c - a, w)

    if denom < 0: # normalize
        denom, P_x_numerator, P_y_numerator = -denom, -P_x_numerator, -P_y_numerator

    return P_x_numerator, P_y_numerator, denom 

def closed_segments_intersect(a: Point, b: Point, c: Point, d: Point):
    # true if closed segments AB and CD intersect
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)

    if o1*o2 < 0 and o3*o4 < 0: # if negative, that means one is CCW and one is CW, which means intersecting!
        return True
    
    # handle collinear and endpoint
    return (on_closed_segment(a, b, c) or on_closed_segment(a, b, d) 
            or on_closed_segment(c, d, a) or on_closed_segment(c, d, b))

def open_segments_intersect(a: Point, b: Point, c: Point, d: Point):
    # true if open segments AB and CD intersect
    o1 = orient(a, b, c)
    o2 = orient(a, b, d)
    o3 = orient(c, d, a)
    o4 = orient(c, d, b)

    if o1*o2 < 0 and o3*o4 < 0: # if negative, that means one is CCW and one is CW, which means intersecting!
        return True
    
    # handle collinear and endpoint
    return (on_open_segment(a, b, c) or on_open_segment(a, b, d) 
            or on_open_segment(c, d, a) or on_open_segment(c, d, b))
