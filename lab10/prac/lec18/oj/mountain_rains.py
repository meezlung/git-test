import sys

N = int(sys.stdin.readline())

A = list(map(int, sys.stdin.readline().split()))

# compute x1 as alternating sum
s = 0
sign = 1

for ai in A:
    s += ai * sign
    sign *= -1

x1 = s // 2

# calculate x_i based from x1
x = [0] * N
x[0] = x1

for i in range(N - 1):
    x[i + 1] = A[i] - x[i]

# times two each for the actual value of rain that has fallen to mountain i
result = [2*xi for xi in x]    
print(*result)