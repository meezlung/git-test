from utils import Point, gcd, dot, cross, norm2, dist2, orient, on_segment, on_open_segment, segments_intersect, same_point

def polygon_area2(poly: list[Point]):
    ensure_valid_polygon(poly)

    A2 = 0
    n = len(poly)
    for i in range(n):
        A2 += cross(poly[i], poly[(i+1)%n])
    return abs(A2) # note that if A2 (signed area) is negative, then one reverses the enumeration of the vertices

    # if vertices are enumerated CCW, then A2 is positive, otherwise negative

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

def is_point_in_polygon(p: Point, poly: list[Point]):
    """
    Ray-crossing test; True if p is inside or on boundary.
    Validates polygon.
    """
    ensure_valid_polygon(poly)
    n = len(poly)
    # boundary
    for i in range(n):
        if on_segment(poly[i], poly[(i+1)%n], p):
            return True
    inside = False
    for i in range(n):
        a, b = poly[i], poly[(i+1)%n]
        if (a.y > p.y) != (b.y > p.y):
            if orient(a, b, p) > 0:
                inside = not inside
    return inside

def polygon_triangulation(poly: list[Point]):
    """
    Ear-clipping triangulation. Validates polygon.
    """
    ensure_valid_polygon(poly)
    def in_tri(p: Point, a: Point, b: Point, c: Point):
        return (orient(a,b,p) >= 0
             and orient(b,c,p) >= 0
             and orient(c,a,p) >= 0)
    V = poly[:]
    tris = []
    while len(V) > 3:
        m = len(V)
        for i in range(m):
            a, b, c = V[i-1], V[i], V[(i+1)%m]
            if orient(a,b,c) <= 0:
                continue
            ear = True
            for p in V:
                if p not in (a, b, c) and in_tri(p, a, b, c):
                    ear = False
                    break
            if ear:
                tris.append((a, b, c))
                del V[i]
                break
    tris.append((V[0], V[1], V[2]))
    return tris # a list of triangles (a, b, c)


def point_in_polygon_crossing(p, poly):
    """Return True if p is inside or on the boundary of a simple polygon poly."""
    inside = False
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        if on_segment(a, b, p):
            return True
        # check if edge straddles horizontal ray right from p
        if (a.y > p.y) != (b.y > p.y):
            if cross(b - a, p - a) * (b.y - a.y) > 0:
                inside = not inside
    return inside

def point_in_polygon_winding(p, poly):
    """Return True if p is inside or on the boundary via winding number."""
    wn = 0
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i+1) % n]
        if on_segment(a, b, p):
            return True
        if a.y <= p.y:
            if b.y > p.y and orient(a, b, p) > 0:
                wn += 1
        else:
            if b.y <= p.y and orient(a, b, p) < 0:
                wn -= 1
    return wn != 0

def point_in_convex_polygon(p, poly):
    """Assumes poly is convex and vertices CCW-ordered. O(log n) check."""
    n = len(poly)
    if n < 3:
        return False
    # p must be between edges from poly[0]
    if orient(poly[0], poly[1], p) < 0 or orient(poly[0], poly[-1], p) > 0:
        return False
    lo, hi = 1, n-1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if orient(poly[0], poly[mid], p) >= 0:
            lo = mid
        else:
            hi = mid
    return orient(poly[lo], poly[hi], p) >= 0

# --- Point-in-Convex-Polygon (CCW-based) ------------------------------

def is_convex_polygon(poly):
    """
    Returns True if poly is simple, non-degenerate, and convex (no interior angle > 180°).
    """
    n = len(poly)
    if n < 3 or not is_simple_polygon(poly):
        return False
    # determine orientation of polygon via signed area
    A2 = 0
    for i in range(n):
        A2 += cross(poly[i], poly[(i+1)%n])
    if A2 == 0:
        return False  # degenerate
    sign = 1 if A2 > 0 else -1
    # each triple must turn consistently
    for i in range(n):
        a = poly[i]
        b = poly[(i+1)%n]
        c = poly[(i+2)%n]
        if sign * orient(a,b,c) < 0:
            return False
    return True

def point_in_convex_polygon(p, poly):
    """O(log n) if poly is convex and CCW-ordered."""
    # require convex & CCW enumeration
    n=len(poly)
    if n<3: return False
    # check p in fan [p0,p1,pn-1]
    if orient(poly[0],poly[1],p) < 0 or orient(poly[0],poly[-1],p) > 0: return False
    # binary search which sector
    lo,hi=1,n-1
    while lo+1<hi:
        mid=(lo+hi)//2
        if orient(poly[0],poly[mid],p) >= 0: lo=mid
        else: hi=mid
    return orient(poly[lo], poly[hi], p) >= 0

# --- 1D Range Counting ------------------------------------------------

def lower_bound(arr,x):
    lo,hi=0,len(arr)
    while lo<hi:
        mid=(lo+hi)//2
        if arr[mid]<x: lo=mid+1
        else: hi=mid
    return lo

def upper_bound(arr,x):
    lo,hi=0,len(arr)
    while lo<hi:
        mid=(lo+hi)//2
        if arr[mid]<=x: lo=mid+1
        else: hi=mid
    return lo

def range_count_1d(arr,l,r):
    """Count elements x in sorted arr with l<=x<=r"""
    return upper_bound(arr,r) - lower_bound(arr,l)

# --- Fenwick Tree (1D) ------------------------------------------------

class Fenwick:
    def __init__(self, n):
        self.n=n; self.f=[0]*(n+1)
    def update(self,i,v):
        while i<=self.n:
            self.f[i]+=v; i+=i&-i
    def query(self,i):
        s=0
        while i>0:
            s+=self.f[i]; i-=i&-i
        return s
    def range_query(self,l,r): return self.query(r)-self.query(l-1)

# --- Static 2D Range Counting (Offline Sweep + Fenwick) ---------------

def static_range_count_2d(points, rects):
    """
    points: list of Point
    rects: list of (lx,rx,ly,ry), returns list of counts.
    Offline: sweep by x, insert points, answer query events.
    """
    # collect ys
    ys=[p.y for p in points]
    for lx,rx,ly,ry in rects: ys.append(ly); ys.append(ry)
    ys=sorted(set(ys)); m=len(ys)
    # map y to idx
    yi={y:i+1 for i,y in enumerate(ys)}
    # events: (x,type, y or ly, ry, idx)
    ev=[]
    for p in points:
        ev.append((p.x,0,p.y))  # insert
    for i,(lx,rx,ly,ry) in enumerate(rects):
        ev.append((rx,1,ly,ry,i))
        ev.append((lx-1,1,ly,ry,i))
    ev.sort(key=lambda e:(e[0],e[1]))
    bit=Fenwick(m)
    ans=[0]*len(rects)
    for e in ev:
        if e[1]==0:
            y=yi[e[2]]; bit.update(y,1)
        else:
            ly,ry,idx=e[2],e[3],e[4]
            cnt=bit.range_query(yi[ly], yi[ry])
            ans[idx] += cnt if e[0]>=0 else -cnt
    return ans

# --- Dynamic 2D Range Counting (2D Fenwick) ----------------------------

class Fenwick2D:
    def __init__(self, xs, ys):
        xs_sorted=sorted(set(xs)); ys_sorted=sorted(set(ys))
        self.xi={x:i+1 for i,x in enumerate(xs_sorted)}
        self.yi={y:i+1 for i,y in enumerate(ys_sorted)}
        self.nx=len(xs_sorted); self.ny=len(ys_sorted)
        self.f=[[0]*(self.ny+1) for _ in range(self.nx+1)]
    def update(self,x,y,v):
        i=self.xi[x]
        while i<=self.nx:
            j=self.yi[y]
            while j<=self.ny:
                self.f[i][j]+=v; j+=j&-j
            i+=i&-i
    def query(self,x,y):
        s=0; i=self.xi.get(x,0)
        while i>0:
            j=self.yi.get(y,0)
            while j>0:
                s+=self.f[i][j]; j-=j&-j
            i-=i&-i
        return s
    def range_query(self,x1,y1,x2,y2):
        return (self.query(x2,y2)
              - self.query(x1-1,y2)
              - self.query(x2,y1-1)
              + self.query(x1-1,y1-1))

# --- k-d Tree for Nearest Neighbor -------------------------------------

class KDNode:
    def __init__(self, pts, depth=0):
        k=2; axis=depth%2
        pts.sort(key=lambda p: (p.x,p.y)[axis])
        mid=len(pts)//2
        self.point=pts[mid]
        self.left=KDNode(pts[:mid],depth+1) if mid>0 else None
        self.right=KDNode(pts[mid+1:],depth+1) if mid+1<len(pts) else None
        self.axis=axis

def kd_nearest(node, target, best=None, depth=0):
    if node is None: return best
    d=dist2(target,node.point)
    if best is None or d<best[1]: best=(node.point,d)
    axis=node.axis
    diff=(target.x-node.point.x) if axis==0 else (target.y-node.point.y)
    first,second=(node.left,node.right) if diff<0 else (node.right,node.left)
    best=kd_nearest(first, target, best, depth+1)
    if diff*diff < best[1]:
        best=kd_nearest(second, target, best, depth+1)
    return best

if __name__ == "__main__":
    # Sample polygons
    convex_square = [Point(0,0), Point(2,0), Point(2,2), Point(0,2)]
    concave_poly  = [Point(0,0), Point(2,0), Point(1,1), Point(2,2), Point(0,2)]
    print("is_simple_polygon(convex_square):", is_simple_polygon(convex_square))
    print("is_convex_polygon(convex_square):", is_convex_polygon(convex_square))
    print("polygon_area2(convex_square):", polygon_area2(convex_square))
    p1 = Point(1,1)
    print("point_in_polygon_crossing(p1, convex_square):", point_in_polygon_crossing(p1, convex_square))
    print("point_in_polygon_winding(p1, convex_square):", point_in_polygon_winding(p1, convex_square))
    print("point_in_convex_polygon(p1, convex_square):", point_in_convex_polygon(p1, convex_square))
    print()
    print("is_simple_polygon(concave_poly):", is_simple_polygon(concave_poly))
    print("is_convex_polygon(concave_poly):", is_convex_polygon(concave_poly))
    p2 = Point(1,0)
    print("point_in_polygon_crossing(p2, concave_poly):", point_in_polygon_crossing(p2, concave_poly))
    print("point_in_polygon_winding(p2, concave_poly):", point_in_polygon_winding(p2, concave_poly))
    print("point_in_convex_polygon(p2, concave_poly): (undefined for non-convex)")

    # 1D Range Count and Fenwick
    arr = [1,2,3,4,5]
    print("range_count_1d 2..4:", range_count_1d(arr,2,4))
    fw = Fenwick(5)
    for i,val in enumerate(arr, start=1):
        fw.update(i, val)
    print("Fenwick prefix sum up to 3:", fw.query(3))
    print("Fenwick range sum 2..4:", fw.range_query(2,4))

    # Static 2D Range Count
    pts2 = [Point(1,1), Point(2,3), Point(3,2)]
    rects = [(0,2,0,2), (2,4,1,3)]
    print("static_range_count_2d:", static_range_count_2d(pts2, rects))

    # Dynamic 2D Range Count
    xs = [p.x for p in pts2]
    ys = [p.y for p in pts2]
    fw2 = Fenwick2D(xs, ys)
    for p in pts2:
        fw2.update(p.x, p.y, 1)
    print("Fenwick2D range_query(1,1,3,2):", fw2.range_query(1,1,3,2))

    # KD-tree Nearest Neighbor
    kd = KDNode(pts2)
    best = kd_nearest(kd, Point(2,2))
    print("Nearest to (2,2):", best)
