import operator
from random import randint

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.or_,
}
"""Operators dictionary, where the key is the textual representation of the
calculation type and the value is the method for implementing the calculation
type.
"""


class CalculationExercise:
    """Calculation exercise class with two operands."""

    question_text = None
    answer_text = None

    def __init__(self, *, calculation_type, min_value, max_value, timeout):
        self.timeout = timeout
        self._set_task_solution(calculation_type, min_value, max_value)

    def _set_task_solution(self, calculation_type, *value_range):
        """Create and set question text with answer text."""
        first_operand = randint(*value_range)
        second_operand = randint(*value_range)
        question = f"{first_operand} {calculation_type} {second_operand}"
        answer = str(OPS[calculation_type](first_operand, second_operand))

        setattr(self, 'question_text', question)
        setattr(self, 'answer_text', answer)
