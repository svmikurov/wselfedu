import operator
from random import randint


class TwoOperandMathTask:
    """Class for simple math calculations with two operands."""

    task_text = None
    calculation = None
    OPS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.or_
    }

    def __init__(self, min_value, max_value, ops):
        if (
                not isinstance(min_value, int | float)
                or not isinstance(max_value, int | float)
        ):
            raise ValueError('number expected')
        if ops not in self.OPS:
            raise ValueError("operators must be: '+' or '-' or '*' or '/'")
        self.value_range = (min_value, max_value)
        self.ops = ops

    def __call__(self):
        operand1 = randint(*self.value_range)
        operand2 = randint(*self.value_range)
        self.calculation = self.OPS[self.ops](operand1, operand2)
        self.task_text = f"{operand1} {self.ops} {operand2}"
        return self.task_text

    def evaluate_solution(self, user_solution):
        return str(self.calculation) == str(user_solution)
