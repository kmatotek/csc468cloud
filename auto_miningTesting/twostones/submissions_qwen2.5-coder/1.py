def determine_winner(N):
    if N % 2 == 1:
        return "Alice"
    else:
        return "Bob"

# Read input from standard input
N = int(input().strip())

# Determine and print the winner
winner = determine_winner(N)
print(winner)