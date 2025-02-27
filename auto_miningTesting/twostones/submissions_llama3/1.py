def winner(n):
    if n % 2 == 0:
        return "Bob"
    else:
        return "Alice"

n = int(input())
print(winner(n))