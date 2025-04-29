def main():
    # Read the three stick lengths
    a, b, c = map(int, input().split())
    
    # Sort so x <= y <= z
    x, y, z = sorted((a, b, c))
    
    # If x + y > z, we already have a valid triangle → 0 moves
    # Else we need (z + 1) - (x + y) increases
    need = max(0, z - (x + y) + 1)
    
    print(need)

if __name__ == "__main__":
    main()