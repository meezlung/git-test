
class TrieNode:
    def __init__(self, alpha=26):
        self.count = 0 # number of words in this subtree
        self.end = 0 # number of words that end with this node
        self.next = [None] * alpha

class Trie:
    def __init__(self, alpha=26, base_char='a'):
        self.root = TrieNode(alpha)
        self.alpha = alpha
        self.base = ord(base_char)

    def insert(self, word: str) -> None:
        v = self.root
        v.count += 1
        for char in word:
            i = ord(char) - self.base
            if v.next[i] is None:
                v.next[i] = TrieNode(self.alpha)
            v = v.next[i]
            v.count += 1
        v.end += 1

    def delete(self, word: str) -> bool:
        def _delete(node, word, depth):
            if node is None:
                return False
            if depth == len(word):
                if node.end == 0:  # word not present
                    return False
                node.end -= 1
                node.count -= 1
                # if node has no children and no words end here, it can be pruned
                return node.count == 0 and node.end == 0
            idx = ord(word[depth]) - self.base
            should_prune = _delete(node.next[idx], word, depth + 1)
            if should_prune:
                node.next[idx] = None
            node.count -= 1
            # prune this node if it’s now empty
            return node.count == 0 and node.end == 0
        
        return _delete(self.root, word, 0)

    def count_word(self, word: str) -> int:
        v = self.root
        for c in word:
            i = ord(c) - self.base
            if not v.next[i]:
                return 0
            v = v.next[i]
        return v.end

    def count_prefix(self, prefix: str) -> int:
        v = self.root
        for char in prefix:
            i = ord(char) - self.base
            if v.next[i] is None:
                return 0
            v = v.next[i]
        return v.count
        
    def search(self, word: str) -> bool:
        v = self.root
        for char in word:
            i = ord(char) - self.base
            if v.next[i] is None:
                return False
            v = v.next[i]
        return v.end > 0
    
    def longest_prefix_match(self, word: str) -> int:
        v = self.root
        length = 0
        for char in word:
            i = ord(char) - self.base
            if v.next[i] is None:
                break
            v = v.next[i]
            length += 1
        return length
    
    def first_mismatch_index(self, word: str) -> int:
        v = self.root
        for idx, char in enumerate(word):
            i = ord(char) - self.base
            if v.next[i] is None:
                return i
            v = v.next[i]
        return len(word)
    
    def words_with_prefix(self, prefix: str, limit: int = None) -> list[str]:
        v = self.root
        for c in prefix:
            i = ord(c) - self.base
            if not v.next[i]:
                return []
            v = v.next[i]
        results = []
        def dfs(node, path):
            if node.end:
                results.extend([prefix + ''.join(path)] * node.end)
                if limit and len(results) >= limit:
                    return True
            for idx, child in enumerate(node.next):
                if child:
                    if dfs(child, path + [chr(self.base + idx)]):
                        return True
            return False
        dfs(v, [])
        return results[:limit] if limit else results
    
    def match(self, pattern: str) -> bool: # supported with wildletter
        def dfs(node, i):
            if not node:
                return False
            if i == len(pattern):
                return node.end > 0
            c = pattern[i]
            if c == '.':
                return any(dfs(child, i+1) for child in node.next if child)
            idx = ord(c) - self.base
            return dfs(node.next[idx], i+1)
        return dfs(self.root, 0)