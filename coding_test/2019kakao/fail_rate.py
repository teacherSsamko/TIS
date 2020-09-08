from collections import Counter
import copy


def sort_key(q):
    return q


def solution(N, stages):
    answer = []

    players = len(stages)
    solved = {x: 0 for x in range(1, N+1)}
    fail_rate = copy.deepcopy(solved)
    for s in stages:
        for l in solved.keys():
            if s > l:
                solved[l] += 1
    # print(solved)
    current = Counter(stages)
    del current[N + 1]
    trial = current + Counter(solved)
    trial = dict(trial)
    current = dict(current)
    for i in range(1, N + 1):
        try:
            fail_rate[i] = current[i] / trial[i]
        except:
            continue

    fail_rate = sorted(fail_rate.items(), key=lambda x: x[1], reverse=True)
    # print(current)
    # print(trial)
    # print(fail_rate)
    answer = [x[0] for x in fail_rate]
    # print(answer)

    return answer


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
