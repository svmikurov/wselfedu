"""
The mathematical calculate exercise module.
"""

import operator
from random import randint

MATH_CALCULATION_TYPE = (
    ('add', 'Сложение'),
    ('sub', 'Вычитание'),
    ('mul', 'Умножение'),
    ('div', 'Деление'),
)
"""Mathematical exercise type choice.

Use in choices, note: max_length=10.
"""


class CalculationExercise:
    """Calculation exercise class with two operands.

    Parameters
    ----------
    calculation_type : `str`
        The symbolic representation of mathematical operator of task.
    min_value : `int`
        Minimum value of operands.
    max_value : `int`
        Maximum value of operands.
    timeout : `int` | None
        Time value to display a math task before displaying the result,
        sec (None | `int`).
    """

    _OPS = {
        'add': operator.add,
        'sub': operator.sub,
        'mul': operator.mul,
    }
    """Alias representation of mathematical operators
    (`Dict[str, object]`).
    """
    _OP_SIGNS = {
        'add': '+',
        'sub': '-',
        'mul': '*',
    }
    """Alias representation of mathematical sign
    (`Dict[str, str]`).
    """
    question_text = None
    """Еhe text representation of a mathematical expression to render to
    the user(None | `str`).
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
        timeout: int | None = None,
    ) -> None:
        """Calculation exercise constructor."""
        self.timeout = timeout
        # Create task
        self._set_task_solution(calculation_type, min_value, max_value)

    def _set_task_solution(
        self,
        calculation_type,
        *value_range,
    ) -> None:
        """Create and set question text with answer text.

        Parameters
        ----------
        calculation_type : `str`
            Alias representation of the calculation type, can be
            'add', 'sub' or 'mul' operator.
        values_range : `tuple`
            Range of values, contains two element, min and max values.
        """
        first_operand = randint(*value_range)
        second_operand = randint(*value_range)
        question = f'{first_operand} {calculation_type} {second_operand}'
        answer = self._OPS[calculation_type](first_operand, second_operand)

        self.question_text = question
        self.answer_text = str(answer)
