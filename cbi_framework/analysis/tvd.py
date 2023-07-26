import numpy as np


def analyze_solution(solution_method_name: str, module):
    solution = getattr(module, solution_method_name)
    small_pack = np.array([6, 13, 11])
    large_pack = np.array([11, 13, 16])
    check_score = solution(small_pack, large_pack)
    if not check_score or not isinstance(check_score, (int, float, np.number)):
        return None

    sol_dict = {
        'proportion': __proportion_test(solution),
        'distance': __distance_test(solution)
    }

    return sol_dict


def __proportion_test(solution):
    uniform_small = np.array([10, 10, 10])
    uniform_large = np.array([20, 20, 20])
    uniform_huge = np.array([50, 50, 50])
    test_1 = solution(uniform_huge, uniform_large)
    test_2 = solution(uniform_small, uniform_huge)
    test_3 = solution(uniform_large, uniform_small)

    if test_1 != 0 or test_2 != 0 or test_3 != 0:
        return False
    return True


def __distance_test(solution):
    baseline = np.array([30, 20, 20, 20, 10])
    closer = np.array([30, 22, 20, 18, 10])
    further = np.array([30, 25, 20, 15, 10])

    expected_high = solution(baseline, further)
    expected_low = solution(baseline, closer)

    return expected_high > expected_low
