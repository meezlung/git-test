class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Point') -> 'Point':
        return Point(self.x - other.x, self.y + other.y)

    def __mul__(self, k: int) -> 'Point':
        return Point(self.x * k, self.y *k)
    
    def __repr__(self):
        return f"Point({self.x}, {self.y})"
    
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def dot(a: Point, b: Point):
    return a.x * b.x + a.y * b.y

def cross(a: Point, b: Point):
    return a.x * b.y - a.y * b.x

def norm2(a: Point):
    return dot(a, a)

def dist2(a: Point, b: Point):
    return norm2(a, b)

def orient(a: Point, b: Point, c: Point):
    # ensures 
    
    # return >0 if a->b->c is CCW
    # return <0 if a->b->c is CW
    # return 0, if straight and collinear

    return cross(b - a, c - a)

def on_segment(a: Point, b: Point, p: Point): 
    # true if point p is in the closed line segment (a,b)
    return orient(a, b, p) == 0 and dot(p - a, p - b) <= 0

def on_open_segment(a: Point, b: Point, p: Point):
    # true if point p is in the closed line segment (a,b)
    return orient(a, b, p) == 0 and dot(p - a, p - b) < 0

def segments_intersect(a, b, c, d):
    # true if segments AB and CD intersect (incl. endpoints)
    o1, o2 = orient(a,b,c), orient(a,b,d)
    o3, o4 = orient(c,d,a), orient(c,d,b)
    if o1*o2 < 0 and o3*o4 < 0:
        return True
    return (on_segment(a,b,c) or on_segment(a,b,d)
            or on_segment(c,d,a) or on_segment(c,d,b))

def same_point(p, q):
    return p.x == q.x and p.y == q.y

def translate_polygon(poly: list[Point], v: Point) -> list[Point]:
    # v translates the poly
    return [Point(p.x + v.x, p.y + v.y) for p in poly]