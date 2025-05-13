from collections.abc import Sequence

Point = tuple[int, int]

def union_poly_area(poly_1: Sequence[Point], poly_2: Sequence[Point]) -> float:

    # --- helper: find all y's where edges cross one another ---
    def edge_intersections_y(p, q):
        Ys = []
        for (x0,y0),(x1,y1) in zip(p, p[1:]+p[:1]):
            dx, dy = x1-x0, y1-y0
            for (u0,v0),(u1,v1) in zip(q, q[1:]+q[:1]):
                ex, ey = u1-u0, v1-v0
                den = dx*ey - dy*ex
                if abs(den) < 1e-12:
                    continue  # parallel or nearly so
                t = ((u0-x0)*ey - (v0-y0)*ex) / den
                u = ((u0-x0)*dy - (v0-y0)*dx) / den
                # proper intersection if 0<t<1 and 0<u<1
                if 0 < t < 1 and 0 < u < 1:
                    yi = y0 + t*dy
                    Ys.append(yi)
        return Ys

    # --- helper: get x-intervals at a given y for one polygon ---
    def slice_intervals(poly, y):
        xs = []
        for (x0,y0),(x1,y1) in zip(poly, poly[1:]+poly[:1]):
            if y0 == y1:
                continue
            # strict bracket so that at exact vertex‐y we don't double‐count
            if (y0 < y < y1) or (y1 < y < y0):
                t = (y - y0) / (y1 - y0)
                xs.append(x0 + t*(x1 - x0))
        xs.sort()
        return [(xs[i], xs[i+1]) for i in range(0, len(xs), 2)]

    # 1) gather all slab‐boundary Y's
    Ys = set([y for _,y in poly_1] + [y for _,y in poly_2])
    Ys.update(edge_intersections_y(poly_1, poly_2))
    Ys = sorted(Ys)

    # 2) scan each open slab by midpoint sampling
    area = 0.0
    for i in range(len(Ys)-1):
        y0, y1 = Ys[i], Ys[i+1]
        h = y1 - y0
        if h <= 0:
            continue
        ym = 0.5*(y0 + y1)

        # collect both‐polygons' intervals at y=ym
        intervals = slice_intervals(poly_1, ym) + slice_intervals(poly_2, ym)
        intervals.sort(key=lambda seg: seg[0])

        # merge union of intervals
        merged = []
        for x0,x1 in intervals:
            if not merged or x0 > merged[-1][1]:
                merged.append([x0, x1])
            else:
                merged[-1][1] = max(merged[-1][1], x1)

        # width at midpoint × height
        w = sum(x1 - x0 for x0,x1 in merged)
        area += w * h

    return area

# print(union_poly_area([(0, 0), (0, 2), (2, 2), (2, 0)], [(1, 1), (1, -1), (-1, -1), (-1, 1)]))

