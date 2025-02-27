def count_unaccepted_groups():
    N, M = map(int, input().split())
    group_sizes = list(map(int, input().split()))
    
    unaccepted_groups = 0
    total_visitors = 0
    
    for size in group_sizes:
        total_visitors += size
        if total_visitors > N:
            unaccepted_groups += 1
            total_visitors -= size

    return unaccepted_groups

print(count_unaccepted_groups())