import ast
import operator as op
from typing import final as sealed

@sealed
class MathEvaluator:

    _OPERATORS = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.FloorDiv: op.floordiv,
        ast.Mod: op.mod,
        ast.Pow: op.pow,
        ast.UAdd: op.pos,
        ast.USub: op.neg,
        ast.BitOr: op.or_,
        ast.BitAnd: op.and_,
        ast.BitXor: op.xor,
    }

    def __init__(self, variables=None):
        self._variables = variables or {}

    def _eval(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers allowed")

        if isinstance(node, ast.Name):
            if node.id in self._variables:
                return self._variables[node.id]
            raise ValueError(f"Unknown variable: {node.id}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise ValueError(f"Operator {op_type.__name__} not allowed")

            left_val = self._eval(node.left)
            right_val = self._eval(node.right)

            bitwise_ops = (ast.BitOr, ast.BitAnd, ast.BitXor)
            if op_type in bitwise_ops:
                if not (isinstance(left_val, int) and isinstance(right_val, int)):
                    raise ValueError(f"Bitwise {op_type.__name__} requires integer operands")

            return self._OPERATORS[op_type](left_val, right_val)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise ValueError("Unary operator not allowed")

            return self._OPERATORS[op_type](self._eval(node.operand))

        raise ValueError("Unsupported expression")

    def evaluate(self, expression):
        if isinstance(expression, (int, float)):
            return expression

        if not isinstance(expression, str):
            return 0

        try:
            tree = ast.parse(expression, mode="eval")
            return self._eval(tree.body)
        except Exception:
            return 0
