def determine_winner(n):
    if n % 2 == 1:
        return "Alice"
    else:
        return "Bob"

# Read input
n = int(input())

# Determine and print the winner
print(determine_winner(n))