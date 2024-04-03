import operator
from random import randint


class TwoOperandMathTask:
    """Class for simple math calculations with two operands."""

    calculation = None
    OPS = {'+': operator.add, '-': operator.sub,
           '*': operator.mul, '/': operator.or_}

    def __init__(self, min_value, max_value, ops):
        if not isinstance(min_value, int | float)\
                or not isinstance(max_value, int | float):
            raise ValueError('number expected')
        self.value_range = (min_value, max_value)
        if ops not in self.OPS:
            raise ValueError("operators must be: '+' or '-' or '*' or '/'")
        self.ops = ops

    def __call__(self):
        operand1 = randint(*self.value_range)
        operand2 = randint(*self.value_range)
        self.calculation = self.OPS[self.ops](operand1, operand2)
        return f"{operand1} {self.ops} {operand2}"

    def evaluate_solution(self, user_solution):
        return str(self.calculation) == str(user_solution)
