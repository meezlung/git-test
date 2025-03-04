import bisect
from typing import List, Optional

# Node for the merge-sort tree
class MergeSortTreeNode:
    def __init__(self, l: int, r: int, sorted_list: List[int], left: Optional['MergeSortTreeNode'] = None, right: Optional['MergeSortTreeNode'] = None):
        self.l = l          # interval start (inclusive)
        self.r = r          # interval end (exclusive)
        self.sorted_list = sorted_list  # sorted list of elements in [l, r)
        self.left = left    # left child
        self.right = right  # right child
        self.sum = sum(sorted_list)  # store sum for range sum query
        self.min_val = min(sorted_list) if sorted_list else float('inf')  # store min for range min query
        self.max_val = max(sorted_list) if sorted_list else float('-inf')  # store max for range max query

def build_merge_sort_tree(arr: List[int], l: int, r: int) -> MergeSortTreeNode:
    """Builds a merge-sort tree for arr[l:r]."""
    if l + 1 == r:
        # Leaf node: one element in the segment
        return MergeSortTreeNode(l, r, [arr[l]])
    mid = (l + r) // 2
    left_node = build_merge_sort_tree(arr, l, mid)
    right_node = build_merge_sort_tree(arr, mid, r)
    # Merge the sorted lists from the two children
    merged = merge_sorted_lists(left_node.sorted_list, right_node.sorted_list)
    node = MergeSortTreeNode(l, r, merged, left_node, right_node)
    node.sum = left_node.sum + right_node.sum
    node.min_val = min(left_node.min_val, right_node.min_val)
    node.max_val = max(left_node.max_val, right_node.max_val)
    return node

def merge_sorted_lists(left_list: List[int], right_list: List[int]) -> List[int]:
    """Merges two sorted lists."""
    merged: list[int] = []
    i = j = 0
    while i < len(left_list) and j < len(right_list):
        if left_list[i] <= right_list[j]:
            merged.append(left_list[i])
            i += 1
        else:
            merged.append(right_list[j])
            j += 1
    merged.extend(left_list[i:])
    merged.extend(right_list[j:])
    return merged

def query_count(node: MergeSortTreeNode | None, ql: int, qr: int, x: int) -> int:
    """
    Returns the count of numbers <= x in the interval [ql, qr)
    using the merge-sort tree node.
    """
    assert node is not None
    
    # No overlap
    if node.r <= ql or node.l >= qr:
        return 0
    # Total overlap
    if ql <= node.l and node.r <= qr:
        return bisect.bisect_right(node.sorted_list, x)
    # Partial overlap: query both children.
    return query_count(node.left, ql, qr, x) + query_count(node.right, ql, qr, x)

def kth_smallest_merge_sort(root: MergeSortTreeNode, ql: int, qr: int, k: int, sorted_vals: List[int]) -> Optional[int]:
    """
    Answers index(ql, qr, k): what is the kth element (0-indexed) in
    the sorted order of arr[ql:qr]? We binary search over sorted_vals.
    """
    lo, hi = 0, len(sorted_vals) - 1
    ans = None
    while lo <= hi:
        mid = (lo + hi) // 2
        candidate = sorted_vals[mid]
        # Count numbers ≤ candidate in [ql, qr)
        count = query_count(root, ql, qr, candidate)
        if count >= k + 1:
            ans = candidate
            hi = mid - 1
        else:
            lo = mid + 1
    return ans

def query_sum(node: MergeSortTreeNode, ql: int, qr: int) -> int:
    """Returns the sum of elements in the interval [ql, qr)."""
    if node.r <= ql or node.l >= qr:
        return 0  # No overlap
    if ql <= node.l and node.r <= qr:
        return node.sum  # Total overlap
    assert node.left is not None and node.right is not None
    return query_sum(node.left, ql, qr) + query_sum(node.right, ql, qr)  # Partial overlap

def query_min(node: MergeSortTreeNode, ql: int, qr: int) -> float:
    """Returns the minimum element in the interval [ql, qr)."""
    if node.r <= ql or node.l >= qr:
        return float('inf')  # No overlap
    if ql <= node.l and node.r <= qr:
        return node.min_val  # Total overlap
    assert node.left is not None and node.right is not None
    return min(query_min(node.left, ql, qr), query_min(node.right, ql, qr))  # Partial overlap

def query_max(node: MergeSortTreeNode, ql: int, qr: int) -> float:
    """Returns the maximum element in the interval [ql, qr)."""
    if node.r <= ql or node.l >= qr:
        return float('-inf')  # No overlap
    if ql <= node.l and node.r <= qr:
        return node.max_val  # Total overlap
    assert node.left is not None and node.right is not None
    return max(query_max(node.left, ql, qr), query_max(node.right, ql, qr))  # Partial overlap

# Example usage
if __name__ == "__main__":
    arr = [4, 2, 6, 1, 5, 3]
    n = len(arr)
    # Build the persistent merge-sort tree (static structure)
    root = build_merge_sort_tree(arr, 0, n)
    # Get sorted unique values (for binary search)
    sorted_vals = sorted(set(arr))
    
    # Example Queries
    i, j, k = 1, 5, 1
    print("kth smallest:", kth_smallest_merge_sort(root, i, j, k, sorted_vals))
    print("Range Sum:", query_sum(root, 1, 5))
    print("Range Min:", query_min(root, 1, 5))
    print("Range Max:", query_max(root, 1, 5))
