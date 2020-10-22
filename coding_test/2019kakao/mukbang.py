def solution(food_times, k):
    answer = 0
    food_count = len(food_times)
    time_last = sum(food_times)
    c_time = 0

    while k > c_time:
        for i in range(food_count):
            if food_times[i] > 0:
                food_times[i] -= 1
            else:
                continue
            # print(i+1)
            # print(food_times)
            # print(c_time, "~", c_time + 1)
            c_time += 1
            if time_last == c_time:
                return -1
    if food_times[i] == 0:
        while food_times[i] == 0:
            if i == (food_count - 1):
                i = 0
            else:
                i += 1
    elif i == (food_count - 1) and food_times[i]:
        i = 0
        while food_times[i] == 0:
            # if i == (food_count - 1):
            #     i = 0
            # else:
            i += 1

    answer = (i + 1)

    # print(answer)
    # print(food_times)

    return answer


def test_solution():
    food_times = [3, 1, 2]
    k = 5
    assert(solution(food_times, k) == 1)
    # food_times = [3, 1, 40, 1, 4]
    # k = 15
    # # assert(solution(food_times, k) == 3)
    food_times = [3, 6, 8, 4, 15]
    k = 15
    assert(solution(food_times, k) == 2)
    # food_times = [3, 1, 4, 8, 5]
    # k = 30
    # assert(solution(food_times, k) == -1)
    print('pass')


if __name__ == "__main__":
    test_solution()
