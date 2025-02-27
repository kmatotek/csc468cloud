def determine_winner(N):
    if N % 2 == 0:
        return "Bob"
    else:
        return "Alice"

# Read input
N = int(input().strip())

# Determine and print the winner
print(determine_winner(N))