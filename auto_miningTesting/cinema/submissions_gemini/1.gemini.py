def calculate_rejected_groups(theater_capacity, group_counts):
  """
  Calculates the number of visitor groups that won't fit in the theater.

  Args:
    theater_capacity: The maximum capacity of the theater.
    group_counts: A list of integers representing the size of each group.

  Returns:
    The number of groups that will be rejected.
  """
  remaining_seats = theater_capacity
  rejected_count = 0

  for group_size in group_counts:
    if group_size <= remaining_seats:
      remaining_seats -= group_size
    else:
      rejected_count += 1

  return rejected_count


def main():
  """Reads input, calculates and prints the number of rejected groups."""
  max_seats, num_groups = map(int, input().split())
  group_sizes = list(map(int, input().split()))

  rejected_groups = calculate_rejected_groups(max_seats, group_sizes)
  print(rejected_groups)


if __name__ == "__main__":
  main()