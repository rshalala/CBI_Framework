import numpy as np


def analyze_solution(solution_method_name: str, module):
    solution = getattr(module, solution_method_name)
    check_score = solution(0.05, 50, 5)
    if not check_score or not isinstance(check_score, (int, float, np.number)):
        return None

    sol_dict = {
        'different_proportion': __test_different_proportion(solution),
        'different_malformed_prob': __test_different_malformed_prob(solution),
        'different_sample_size': __test_different_sample_size(solution)
    }

    return sol_dict


def __test_different_proportion(solution):
    malformed_prob = 0.05
    bag_size = 200
    num_of_malformed_low = 5
    num_of_malformed_high = 50

    expected_higher_score = solution(malformed_prob, bag_size, num_of_malformed_high)
    expected_lower_score = solution(malformed_prob, bag_size, num_of_malformed_low)

    return expected_higher_score > expected_lower_score


def __test_different_sample_size(solution):
    malformed_prob = 0.05
    num_of_malformed_small_bag = 5
    num_of_malformed_large_bag = 20
    small_bag_size = 50
    large_bag_size = 200

    expected_higher_score = solution(malformed_prob, large_bag_size, num_of_malformed_large_bag)
    expected_lower_score = solution(malformed_prob, small_bag_size, num_of_malformed_small_bag)

    return expected_higher_score > expected_lower_score


def __test_different_malformed_prob(solution):
    malformed_prob_low = 0.05
    malformed_prob_high = 0.5
    bag_size = 200
    num_of_malformed = 40

    expected_higher_score = solution(malformed_prob_low, bag_size, num_of_malformed)
    expected_lower_score = solution(malformed_prob_high, bag_size, num_of_malformed)

    return expected_higher_score > expected_lower_score
