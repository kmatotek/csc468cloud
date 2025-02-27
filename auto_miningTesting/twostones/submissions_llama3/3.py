def stone_game(n):
    if n % 4 == 0:
        return "Bob"
    elif n % 4 == 1:
        return "Alice"
    elif n % 4 == 2:
        return "Bob"
    else:
        return "Alice"

n = int(input())
print(stone_game(n))