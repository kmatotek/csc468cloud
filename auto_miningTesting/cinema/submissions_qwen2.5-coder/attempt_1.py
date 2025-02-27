def count_unaccepted_groups(total_seats, number_of_groups, group_sizes):
    unaccepted_groups = 0
    remaining_seats = total_seats

    for group_size in group_sizes:
        if group_size > remaining_seats:
            unaccepted_groups += 1
        else:
            remaining_seats -= group_size

    return unaccepted_groups

# Reading input from user
total_seats, number_of_groups = map(int, input().split())
group_sizes = list(map(int, input().split()))

# Calculating the result
result = count_unaccepted_groups(total_seats, number_of_groups, group_sizes)

# Printing the output
print(result)