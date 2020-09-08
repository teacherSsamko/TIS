def solution(N, stages):
    result = {}
    denominator = len(stages)
    for stage in range(1, N+1):
        if denominator != 0:
            count = stages.count(stage)
            result[stage] = count / denominator
            denominator -= count
        else:
            result[stage] = 0
    return sorted(result, key=lambda x: result[x], reverse=True)


def test_solution():
    N = 5
    stages = [2, 1, 2, 6, 2, 4, 3, 3]
    result = [3, 4, 2, 1, 5]
    assert(solution(N, stages) == result)
    N = 4
    stages = [4, 4, 4, 4, 4]
    result = [4, 1, 2, 3]
    assert(solution(N, stages) == result)
    print('pass')


if __name__ == "__main__":
    test_solution()
