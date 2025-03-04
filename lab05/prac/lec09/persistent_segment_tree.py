from typing import Optional

class PSTNode:
    __slots__ = ('left', 'right', 'count')
    def __init__(self, left: Optional['PSTNode'] = None, right: Optional['PSTNode'] = None, count: int = 0):
        self.left = left
        self.right = right
        self.count = count

def pst_update(prev: Optional[PSTNode], start: int, end: int, pos: int) -> PSTNode:
    """
    Returns a new PSTNode that is an update of 'prev' with a new occurrence at 'pos'.
    The update is done in the segment tree interval [start, end).
    """
    new_node = PSTNode()
    if prev:
        new_node.left = prev.left
        new_node.right = prev.right
        new_node.count = prev.count
    else:
        new_node.count = 0
    if start + 1 == end:
        new_node.count += 1
        return new_node
    mid = (start + end) // 2
    if pos < mid:
        new_node.left = pst_update(prev.left if prev else None, start, mid, pos)
    else:
        new_node.right = pst_update(prev.right if prev else None, mid, end, pos)
    new_node.count = (new_node.left.count if new_node.left else 0) + (new_node.right.count if new_node.right else 0)
    return new_node

def pst_query(u: PSTNode | None, v: Optional[PSTNode], start: int, end: int, k: int) -> int:
    """
    Given two persistent segment tree roots:
      - u: version for prefix ending at index j
      - v: version for prefix ending at index i
    This function returns the compressed coordinate of the kth smallest element in the subarray [i, j),
    where k is 1-indexed.
    """
    assert u is not None

    if start + 1 == end:
        return start
    mid = (start + end) // 2
    # Count how many numbers go to the left child in the range.
    left_count = (u.left.count if u.left else 0) - (v.left.count if v and v.left else 0)
    if k <= left_count:
        return pst_query(u.left, v.left if v else None, start, mid, k)
    else:
        return pst_query(u.right, v.right if v else None, mid, end, k - left_count)

# Additional useful functions
def pst_range_count(u: PSTNode | None, v: Optional[PSTNode], start: int, end: int, l: int, r: int) -> int:
    """
    Counts the number of elements in the range [l, r) in the segment tree.
    """
    if not u:
        return 0
    if start >= r or end <= l:
        return 0
    if start >= l and end <= r:
        return (u.count - v.count) if v else u.count
    mid = (start + end) // 2
    return pst_range_count(u.left, v.left if v else None, start, mid, l, r) + pst_range_count(u.right, v.right if v else None, mid, end, l, r)

# Example usage for 3.2:
if __name__ == "__main__":

    def kth_smallest_pst(l: int, r: int, k: int) -> int:
        """
        Returns the kth smallest element (0-indexed k) in arr[l:r] using PST.
        (k is 0-indexed; we add 1 for 1-indexed kth query inside pst_query.)
        """
        comp_index = pst_query(versions[r], versions[l], 0, m, k + 1)
        return sorted_vals[comp_index]

    arr = [4, 2, 6, 1, 5, 3]
    n = len(arr)
    
    # Coordinate compression
    sorted_vals = sorted(set(arr))
    comp = {val: i for i, val in enumerate(sorted_vals)}
    comp_arr = [comp[x] for x in arr]
    m = len(sorted_vals)  # number of distinct values
    
    # Build persistent segment tree versions:
    # version[0] corresponds to an empty prefix.
    versions: list[Optional[PSTNode]] = [None] * (n + 1)
    # Initially, an empty tree (we use None to denote a tree with count 0)
    versions[0] = PSTNode(count=0)
    
    # Build each version by updating the previous version with the current element.
    for i in range(n):
        versions[i + 1] = pst_update(versions[i], 0, m, comp_arr[i])
    
    # Query example: find the 2nd smallest (k=1 for 0-indexed) in subarray arr[1:5] = [2,6,1,5]
    i, j, k = 1, 5, 1
    result = kth_smallest_pst(i, j, k)
    print("3.2: kth smallest (k={} in arr[{}:{}]) is {}".format(k, i, j, result))