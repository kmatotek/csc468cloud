def find_closest_ending_in_99():
    N = int(input())
    closest_number = None
    diff1 = float('inf')
    diff2 = float('inf')

    for i in range(N-99, N+100):
        if i % 100 == 99:
            diff = abs(i - N)
            if diff < diff1:
                closest_number = i
                diff1 = diff
            elif diff == diff1:
                closest_number = max(closest_number, i)

    print(closest_number)

find_closest_ending_in_99()