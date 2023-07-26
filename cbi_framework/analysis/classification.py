import math
import numpy as np

default_sample_size = 40  # sample size similar to the one in the Invention activity


def case_generator(size: int, mistakes_ratio=0.5, fn=-1, fp=-1):
    """
    Generate a classification case of [actual, predicted] pair. The actual data contains size/2 trues, other are false.
    False positives and false negatives are generated according to ratio, or more explicitly by fn and fp parameters.
    Ratio sets the proportion of mistakes (fn=fp). fp and fn parameters are used to manually set the number of fn and fp
    In a case in which only one input is entered (fp or fn), the other one is set to 0.\n
    :param size: Sample size
    :param mistakes_ratio: Proportion of mistakes. ratio=1 will result in accuracy=0, ratio=0 will result in accuracy=1
    :param fn: Number of false negatives
    :param fp: Number of false positives
    :return: 1: actual Numpy array, 2: predicted Numpy array, 3: number of false positives, 4: number of false negatives
    """
    actual = np.zeros(size, dtype=int)
    actual[0:math.floor(size / 2)] = 1  # default is size/2 trues, other are false
    predicted = np.array(actual)

    if fn == fp == -1:  # generate predicted np_array based on ratio: fn = fp = size /2 /2
        if mistakes_ratio < 0 or mistakes_ratio > 1:
            raise Exception('ratio should be between 0 and 1')
        fn = fp = math.floor(size / 2 * mistakes_ratio)
    else:  # generate predicted np_array based on given fn and fp
        if fn > np.count_nonzero(actual == 1):  # error - fn is higher than the number of actual positives
            raise Exception('FN higher than actual positives')
        if fp > np.count_nonzero(actual == 0):  # error - fp is higher than the number of actual negatives
            raise Exception('FP higher than actual negatives')
        # case on which only one parameter provided (the other parameter value is still -1),
        # it is estimated that the other parameter should be 0
        if fn < 0:
            fn = 0
        if fp < 0:
            fp = 0

    if fn != 0:
        predicted[0:fn] = 0
    if fp != 0:
        predicted[-fp:] = 1

    return actual, predicted, fp, fn


def analyze_solution(solution_method_name: str, module):
    solution = getattr(module, solution_method_name)
    # test solution is working
    actual, predicted, _, _ = case_generator(size=default_sample_size)
    check_score = solution(actual, predicted)
    if not check_score or not isinstance(check_score, (int, float, np.number)):
        return None

    sol_dict = {
        'accuracy': __accuracy_test(solution, default_sample_size),
        'fp_vs_fn': __fp_fn_test(solution, default_sample_size),
        'normalization': __normalization_test(solution)
    }

    return sol_dict


def __accuracy_test(solution, sample_size):
    actual, predicted, _, _ = case_generator(size=sample_size, fn=3, fp=6)
    expected_low = solution(actual, predicted)
    actual, predicted, _, _ = case_generator(size=sample_size, fn=3, fp=3)
    expected_high = solution(actual, predicted)

    return expected_high > expected_low


def __fp_fn_test(solution, sample_size, diff=3):
    actual, predicted, fp, fn = case_generator(sample_size)  # get equal number of FPs and FNs
    actual, predicted, _, _ = case_generator(sample_size, fp=fp+diff, fn=fn)
    score_high_fp = solution(actual, predicted)
    actual, predicted, _, _ = case_generator(sample_size, fp=fp, fn=fn+diff)
    score_high_fn = solution(actual, predicted)

    return score_high_fn < score_high_fp


def __normalization_test(solution):
    # test accuracy normalization
    actual, predicted, _, _ = case_generator(size=default_sample_size, mistakes_ratio=0.4)
    test_accuracy_default = solution(actual, predicted)
    actual, predicted, _, _ = case_generator(size=default_sample_size*2, mistakes_ratio=0.4)
    test_accuracy_doubled = solution(actual, predicted)
    test_1_pass = test_accuracy_default == test_accuracy_doubled

    actual, predicted, _, _ = case_generator(size=default_sample_size, mistakes_ratio=0.8)
    test_accuracy_default = solution(actual, predicted)
    actual, predicted, _, _ = case_generator(size=default_sample_size*2, mistakes_ratio=0.8)
    test_accuracy_doubled = solution(actual, predicted)
    test_2_pass = test_accuracy_default == test_accuracy_doubled

    return test_1_pass and test_2_pass
