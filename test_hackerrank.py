"""
pytest test file for HackerRank.py

pytest discovery rules (why this file is named/shaped the way it is):
  - the FILE must start with `test_` or end with `_test.py` for pytest to find it
  - each FUNCTION inside must start with `test_` for pytest to run it as a test
  - just running `pytest` in the terminal (no arguments) auto-discovers every
    file/function matching those patterns in the current directory and below
"""

import pytest
from fractions import Fraction

# HackerRank.py's `if __name__ == '__main__':` block only runs when the file is
# executed directly, not when it's imported - so importing mehtaLazy here is safe,
# it won't try to read stdin or write to OUTPUT_PATH.
from HackerRank import mehtaLazy
from HackerRank import findPoint


# @pytest.mark.parametrize lets one test function run multiple times, once per
# tuple in the list, instead of writing a near-identical test per case.
# The string "n, expected" names the two values pytest will unpack from each
# tuple below and pass in as arguments to the test function.
@pytest.mark.parametrize("n, expected", [
    (2, 0),                 # proper divisor of 2 is just {1}; 1 is odd -> no even perfect squares -> 0
    (8, Fraction(1, 3)),    # proper divisors {1,2,4}; only 4 is an even perfect square -> 1/3
    (36, Fraction(1, 8)),   # proper divisors {1,2,3,4,6,9,12,18}; only 4 qualifies -> 1/8
    (900, Fraction(3, 26)), # 26 proper divisors; 4, 36, 100 are even perfect squares -> 3/26
])
def test_mehtaLazy_given_examples(n, expected):
    # assert raises an AssertionError (which pytest reports as a failed test)
    # if the condition is False. Comparing a Fraction to an int (like the `0`
    # case above) works fine - Fraction implements __eq__ against plain numbers.
    assert mehtaLazy(n) == expected


# Edge cases worth testing separately from the given examples, and why:
@pytest.mark.parametrize("n, expected", [
    (1, 0),   # smallest possible input - no proper divisors exist at all
    (13, 0),  # a prime number - its only proper divisor is 1, which can never
              # be an even perfect square (1 is odd) - stresses the "always 0" path
])
def test_mehtaLazy_edge_cases(n, expected):
    assert mehtaLazy(n) == expected

@pytest.mark.parametrize("px, py, qx, qy, expected1, expected2", [
    (0, 0, 1, 1, 2, 2),
    (1, 1, 2, 2, 3, 3)
])

def test_findPoint_examples(px, py, qx, qy, expected1, expected2):
    assert findPoint (px, py, qx, qy) == f"{(expected1)} {(expected2)}"