"""The mathematical calculate exercise module."""

import operator
from random import randint


class CalculationExercise:
    """Calculation exercise class with two operands.

    The user is shown a mathematical expression as a question. The user
    calculates the mathematical expression. After a timeout, the user
    is shown the result of the mathematical expression. The user
    compares his calculation with the result of the mathematical
    expression displayed on the page.

    Parameters
    ----------
    calculation_type : `str`
        The symbolic representation of mathematical operator of task.
    min_value : `int`
        Minimum value of operands.
    max_value : `int`
        Maximum value of operands.
    timeout : `int`
        Time value to display a math task before displaying the result,
        sec (None | `int`).

    """

    _OPS = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
    }
    """The symbolic representation of mathematical operators
    (Dict[`str`, object]).
    """
    question_text = None
    """The text representation of a mathematical expression to render to
    the user (None | `str`).
    """
    answer_text = None
    """The text representation of the result of calculating
    a mathematical expression (None | `str`).
    """

    def __init__(
        self,
        *,
        calculation_type: str,
        min_value: int,
        max_value: int,
        timeout: int,
    ) -> None:
        """Construct the calculation exercise."""
        self.timeout = timeout
        # Create task
        self._set_task_solution(calculation_type, min_value, max_value)

    def _set_task_solution(
        self,
        calculation_type: str,
        *value_range: tuple,
    ) -> None:
        """Create and set question text with answer text.

        Parameters
        ----------
        calculation_type : `str`
            The symbolic representation of the calculation type, can be
            '+', '-' or '*' operator.
        values_range : `tuple`
            Range of values, contains two element, its start and end values.

        """
        first_operand = randint(*value_range)
        second_operand = randint(*value_range)
        question = f'{first_operand} {calculation_type} {second_operand}'
        answer = self._OPS[calculation_type](first_operand, second_operand)

        self.question_text = question
        self.answer_text = str(answer)
