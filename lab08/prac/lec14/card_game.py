# type: ignore

from collections import deque
from dataclasses import dataclass
import sys

############################################
# FLOW NETWORK (Edmonds–Karp) implementation
############################################

@dataclass
class Edge:
    i: int
    j: int
    cap: int
    flow: int = 0
    back: "Edge | None" = None

    @property
    def is_saturated(self):
        return self.cap - self.flow == 0

    @property
    def res(self):
        return self.cap - self.flow

    def add_flow(self, f):
        self._add_flow(f)
        self.back._add_flow(-f)

    def _add_flow(self, f):
        # Ensure we don't exceed capacity.
        assert self.flow + f <= self.cap, f"Flow {self.flow} + {f} > {self.cap}"
        self.flow += f

class FlowNetwork:
    def __init__(self, n, s, t):
        self.n = n        
        self.s = s        
        self.t = t        
        self.adj = [[] for _ in range(n)]

    def add_edge(self, i, j, cap):
        edge_ij = Edge(i, j, cap)
        edge_ji = Edge(j, i, 0)
        self.adj[i].append(edge_ij)
        self.adj[j].append(edge_ji)
        edge_ij.back = edge_ji
        edge_ji.back = edge_ij

    def find_augmenting_path(self):
        que = deque([self.s])
        pedge = [None] * self.n  
        pedge[self.s] = True 
        while que:
            i = que.popleft()
            if i == self.t:
                path = []
                while i != self.s:
                    path.append(pedge[i])
                    i = pedge[i].i
                return path
            for edge in self.adj[i]:
                if edge.res > 0 and pedge[edge.j] is None:
                    pedge[edge.j] = edge
                    que.append(edge.j)
        return None

    def augment(self, path):
        delta = min(edge.res for edge in path)
        for edge in path:
            edge.add_flow(delta)
        return delta

    def max_flow(self):
        max_flow_value = 0
        while (path := self.find_augmenting_path()) is not None:
            max_flow_value += self.augment(path)
        return max_flow_value

############################################
# SIEVE & PRIME CHECKING
############################################

def sieve(n):
    is_prime = [True]*(n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return is_prime

prime_table = sieve(200000)
def is_prime(x):
    if x < len(prime_table):
        return prime_table[x]
    return False

############################################
# BIPARTITE Maximum Weighted Independent Set (MWIS)
############################################
# In our bipartite graph, one part (A) will be the even cards,
# and the other part (B) the odd cards (with c != 1).
# We build a flow network as follows:
#   - Source -> a in A with capacity = power of a.
#   - b in B -> Sink with capacity = power of b.
#   - For every conflict between a in A and b in B (i.e. if is_prime(a.c + b.c) is True),
#     add an edge from a to b with infinite capacity.
# Then the minimum vertex cover has weight = (min cut value),
# and the maximum independent set weight is (total weight - min_cut).

def bipartite_mwis(even, odd):
    # even: list of tuples (p, c)
    # odd: list of tuples (p, c)
    nA = len(even)
    nB = len(odd)
    total = sum(p for (p, c) in even) + sum(p for (p, c) in odd)
    N = nA + nB + 2
    source = 0
    sink = N - 1
    net = FlowNetwork(N, source, sink)
    INF = 10**9
    # Add edges from source to even nodes.
    for i, (p, c) in enumerate(even):
        net.add_edge(source, 1+i, p)
    # Add edges from odd nodes to sink.
    for j, (p, c) in enumerate(odd):
        net.add_edge(1+nA+j, sink, p)
    # For every conflict (even, odd) add an infinite capacity edge.
    for i, (p, c) in enumerate(even):
        for j, (p2, c2) in enumerate(odd):
            if is_prime(c + c2):
                net.add_edge(1+i, 1+nA+j, INF)
    min_cover = net.max_flow()
    return total - min_cover

############################################
# Solve deck selection for a given level L
############################################

def solve_for_level(cards, L):
    # Consider only cards with level <= L.
    available = [card for card in cards if card[2] <= L]
    # Partition into three groups:
    even = []       # Cards with even magic number.
    odd = []        # Cards with odd magic number and c != 1.
    ones = []       # Cards with magic number 1.
    for (p, c, l) in available:
        if c % 2 == 0:
            even.append((p, c))
        else:
            if c == 1:
                ones.append((p, c))
            else:
                odd.append((p, c))
    best = 0
    # Option 1: Do not use any card from group C (magic number 1).
    best = max(best, bipartite_mwis(even, odd))
    # Option 2: Try using exactly one card from group C.
    if ones:
        # For each candidate card x from ones, we cannot take any even card that conflicts with it.
        # An even card (with magic number x) conflicts with x if is_prime(x + 1) holds.
        for (p_one, c_one) in ones:
            even_filtered = [(p, c) for (p, c) in even if not is_prime(c + 1)]
            candidate = p_one + bipartite_mwis(even_filtered, odd)
            best = max(best, candidate)
    return best

############################################
# Main – Binary (or Linear) search over level L
############################################

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    k = int(next(it))
    cards = []
    max_level = 0
    for _ in range(n):
        p = int(next(it))
        c = int(next(it))
        l = int(next(it))
        cards.append((p, c, l))
        max_level = max(max_level, l)
    ans = -1
    # Since levels are at most n (n<=100), we can simply iterate.
    for L in range(1, max_level+1):
        if solve_for_level(cards, L) >= k:
            ans = L
            break
    print(ans)

if __name__ == '__main__':
    main()
