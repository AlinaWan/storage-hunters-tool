import pytest
from src.utils.math_evaluator import MathEvaluator

@pytest.fixture
def evaluator():
    # Setup with dummy screen constants
    return MathEvaluator({"SCREEN_WIDTH": 1920, "SCREEN_HEIGHT": 1080})

def test_basic_arithmetic(evaluator):
    assert evaluator.evaluate("1 + 2") == 3
    assert evaluator.evaluate("10 - 5") == 5
    assert evaluator.evaluate("2 * 3") == 6
    assert evaluator.evaluate("10 / 2") == 5.0
    assert evaluator.evaluate("10 // 3") == 3

def test_variable_substitution(evaluator):
    assert evaluator.evaluate("SCREEN_WIDTH / 2") == 960.0
    assert evaluator.evaluate("SCREEN_HEIGHT * 0.5") == 540.0

def test_bitwise_operations(evaluator):
    assert evaluator.evaluate("1 & 1") == 1
    assert evaluator.evaluate("1 | 2") == 3
    assert evaluator.evaluate("3 ^ 1") == 2

def test_operator_precedence(evaluator):
    assert evaluator.evaluate("1 + 2 * 3") == 7
    assert evaluator.evaluate("(1 + 2) * 3") == 9

def test_invalid_input(evaluator):
    # Test that invalid strings or expressions return 0
    assert evaluator.evaluate("invalid_var + 1") == 0
    assert evaluator.evaluate("1 + + +") == 0
    assert evaluator.evaluate("text_string") == 0

def test_non_string_input(evaluator):
    assert evaluator.evaluate(100) == 100
    assert evaluator.evaluate(None) == 0