import operator
from random import randint


class CalculationExercise:
    """Calculation exercise class with two operands."""

    _OPS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
    }
    question_text = None
    answer_text = None

    def __init__(self, *, calculation_type, min_value, max_value, timeout):
        self.timeout = timeout
        # Create task
        self._set_task_solution(calculation_type, min_value, max_value)

    def _set_task_solution(self, calculation_type, *value_range):
        """Create and set question text with answer text.

        Parameters:
        -----------
        calculation_type : `str`
            The symbolic representation of the calculation type, can be
            '+', '-' or '*' operator.
        values_range : `tuple`
            Range of values, contains two element, its start and end values.
        """
        first_operand = randint(*value_range)
        second_operand = randint(*value_range)
        question = f"{first_operand} {calculation_type} {second_operand}"
        answer = self._OPS[calculation_type](first_operand, second_operand)

        setattr(self, 'question_text', question)
        setattr(self, 'answer_text', str(answer))
