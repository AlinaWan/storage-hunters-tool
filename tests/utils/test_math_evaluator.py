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
    # Test that invalid strings or expressions return None
    assert evaluator.evaluate("invalid_var + 1") is None
    assert evaluator.evaluate("1 + + +") is None
    assert evaluator.evaluate("text_string") is None

def test_non_string_input(evaluator):
    assert evaluator.evaluate(100) == 100
    assert evaluator.evaluate(None) is None

def test_unary_operators(evaluator):
    assert evaluator.evaluate("+5") == 5
    assert evaluator.evaluate("-5") == -5
    assert evaluator.evaluate("-SCREEN_WIDTH") == -1920

def test_modulo_and_power(evaluator):
    assert evaluator.evaluate("10 % 3") == 1
    assert evaluator.evaluate("2 ** 8") == 256

def test_whitelisted_functions(evaluator):
    assert evaluator.evaluate("int(5.9)") == 5
    assert evaluator.evaluate("int()") == 0
    assert evaluator.evaluate("min(10, 3, 8)") == 3
    assert evaluator.evaluate("max(10, 3, 8)") == 10
    assert evaluator.evaluate("abs(-123)") == 123

def test_nested_function_calls(evaluator):
    assert evaluator.evaluate("max(abs(-5), min(8, 3))") == 5
    assert evaluator.evaluate("int(max(1.2, 2.8))") == 2

def test_invalid_function_calls(evaluator):
    assert evaluator.evaluate("round(1.5)") is None
    assert evaluator.evaluate("__import__('os')") is None
    assert evaluator.evaluate("eval('1+1')") is None

def test_invalid_attribute_calls(evaluator):
    assert evaluator.evaluate("math.floor(1.5)") is None
    assert evaluator.evaluate("(1).bit_length()") is None

def test_invalid_bitwise_operands(evaluator):
    assert evaluator.evaluate("1.5 & 1") is None
    assert evaluator.evaluate("1 | 2.5") is None
    assert evaluator.evaluate("3.0 ^ 1") is None

def test_invalid_function_arguments(evaluator):
    assert evaluator.evaluate("min()") is None
    assert evaluator.evaluate("max()") is None
    assert evaluator.evaluate("abs()") is None

def test_invalid_variable(evaluator):
    assert evaluator.evaluate("UNKNOWN_VARIABLE + 1") is None
    assert evaluator.evaluate("SCREEN_WIDTH + UNKNOWN_VARIABLE") is None

def test_unsupported_syntax(evaluator):
    assert evaluator.evaluate("[1, 2, 3]") is None
    assert evaluator.evaluate("{1: 2}") is None
    assert evaluator.evaluate("(1, 2)") is None