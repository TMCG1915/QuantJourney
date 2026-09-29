import pytest
from SANDBOX.class_practice import Multiply  # Adjust if your file is named differently

# Test multiplying two positive numbers
def test_multiply_positive():
    m = Multiply(2, 3)
    assert m.multiply() == 6  # 2 * 3 should be 6

# Test multiplying by zero
def test_multiply_zero():
    m = Multiply(0, 5)
    assert m.multiply() == 0  # 0 * 5 should be 0

# Test multiplying a negative and a positive number
def test_multiply_negative():
    m = Multiply(-2, 4)
    assert m.multiply() == -8  # -2 * 4 should be -8

# Test that a TypeError is raised when a non-integer is used
def test_type_error():
    with pytest.raises(TypeError):  # Expects a TypeError to be raised
        Multiply(2, "a")

# To run these tests, use the command: pytest