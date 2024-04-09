import operator
from random import randint


class TwoOperandMathTaskNotCall:
    """Class for simple math calculations with two operands."""

    task_text = None
    calculation = None

    def __init__(self, min_value, max_value, ops):
        if (
                not isinstance(min_value, int | float)
                or not isinstance(max_value, int | float)
        ):
            raise ValueError('number expected')
        self.value_range = (min_value, max_value)
        self.ops = ops

    def create_task(self):
        operand1 = randint(*self.value_range)
        operand2 = randint(*self.value_range)
        self.task_text = f"{operand1} {self.ops} {operand2}"
        self.calculation = eval(self.task_text)
        return self.task_text

    def get_calculation(self):
        return self.calculation

    def get_task_text(self):
        return self.task_text

    def evaluate_solution(self, user_solution):
        return str(self.calculation) == str(user_solution)
