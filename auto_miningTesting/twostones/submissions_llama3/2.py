def find_winner(n):
    if n % 2 == 0:
        return "Bob"
    else:
        return "Alice"

n = int(input())
print(find_winner(n))