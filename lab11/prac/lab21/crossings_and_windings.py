def crossings_and_winding(polygon, point):
    """
    Compute the ray-crossing count and winding number for a point in a polygon.

    Args:
        polygon: List of vertices [(x0, y0), (x1, y1), ..., (xn-1, yn-1)].
                 The polygon may be open or closed; if open, the function
                 will treat it as closed by implicitly connecting the last
                 vertex back to the first.
        point:   Tuple (px, py) of the query point.

    Returns:
        crossings: int, number of times a horizontal ray to the right
                   crosses polygon edges.
        winding:   int, the winding number of the polygon around the point.
    """
    px, py = point
    crossings = 0
    winding = 0
    n = len(polygon)
    # Make sure we wrap around
    for i in range(n):
        x0, y0 = polygon[i]
        x1, y1 = polygon[(i + 1) % n]

        # Check if edge crosses the horizontal ray to the right of (px, py)
        # Edge crosses ray if one endpoint is above py and the other is at or below
        # py, and the intersection x > px.
        if ((y0 > py) != (y1 > py)):
            # Compute the x-coordinate of the intersection of the edge with the horizontal line y = py
            t = (py - y0) / (y1 - y0)
            x_int = x0 + t * (x1 - x0)
            if x_int > px:
                crossings += 1

        # Winding number update:
        # If edge goes upward past the ray and is to the left, +1
        if y0 <= py:
            if y1 > py:  # upward crossing
                # isLeft > 0 means point is left of the edge
                if (x1 - x0) * (py - y0) - (px - x0) * (y1 - y0) > 0:
                    winding += 1
        else:
            if y1 <= py:  # downward crossing
                # isLeft < 0 means point is right of the edge
                if (x1 - x0) * (py - y0) - (px - x0) * (y1 - y0) < 0:
                    winding -= 1

    return crossings, winding


# Example usage:
if __name__ == "__main__":
    square = [(0, 0), (10, 0), (10, 10), (0, 10)]
    test_points = [(5, 5), (15, 5), (5, -5), (10, 5)]
    for pt in test_points:
        cr, wn = crossings_and_winding(square, pt)
        inside_cn = (cr % 2 == 1)
        inside_wn = (wn != 0)
        print(f"Point {pt}: crossings={cr}, winding={wn}, "
              f"inside_cn={inside_cn}, inside_wn={inside_wn}")