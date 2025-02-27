def game_outcome(board_size, starting_position, goal_number, board_values):
    frog_position = starting_position - 1  # Adjust for zero-based indexing
    visited_positions = set()
    hop_count = 0

    while True:
        if board_values[frog_position] == goal_number:
            return "magic", hop_count
        elif frog_position < 0:
            return "left", hop_count
        elif frog_position >= board_size:
            return "right", hop_count
        elif frog_position in visited_positions:
            return "cycle", hop_count

        visited_positions.add(frog_position)
        hop_distance = board_values[frog_position]
        frog_position += hop_distance
        hop_count += 1

if __name__ == "__main__":
    board_size, starting_position, goal_number = map(int, input().split())
    board_values = list(map(int, input().split()))
    fate, hops = game_outcome(board_size, starting_position, goal_number, board_values)
    print(fate)
    print(hops)