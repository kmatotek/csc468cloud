def find_closest_ending_in_99():
    N = int(input())
    closest_number1 = (N // 100) * 100 + 99
    closest_number2 = ((N // 100) + 1) * 100 + 99

    if abs(closest_number1 - N) < abs(closest_number2 - N):
        print(closest_number1)
    else:
        print(closest_number2)

find_closest_ending_in_99()