def gcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def largest_picture(r: int, c: int, w: int, h: int) -> tuple[int, int]:
    # First, reduce the aspect ratio to simplest form.
    aspect_gcd, _, _ = gcd(w, h)
    w, h = w // aspect_gcd, h // aspect_gcd
    
    # Check for necessary tiling conditions
    if c % w != 0 or r % h != 0:
        return (-1, -1)
    
    # Compute the maximum scale, let A and B be how many reduced units fit into the frame
    A = c // w
    B = r // h
    max_scale, _, _ = gcd(A, B)
    
    return (w * max_scale, h * max_scale)

# print(largest_picture(4, 9, 3, 2))
# print(largest_picture(5, 4, 2, 1))
# print(largest_picture(5, 5, 1, 1))
# print(largest_picture(1, 1, 1, 1))
# print(largest_picture(6, 6, 4, 4))
