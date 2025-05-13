import sys
input = sys.stdin.readline

def kmp_count(text: str, pattern: str) -> int:
    n, m = len(text), len(pattern)
    # build prefix-function for pattern
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
            pi[i] = j

    # search
    count = 0
    j = 0
    for ch in text:
        while j > 0 and ch != pattern[j]:
            j = pi[j - 1]
        if ch == pattern[j]:
            j += 1
            if j == m:
                count += 1
                j = pi[j - 1]
    return count

def main():
    s = input().rstrip('\n')
    p = input().rstrip('\n')
    print(kmp_count(s, p))

if __name__ == "__main__":
    main()
