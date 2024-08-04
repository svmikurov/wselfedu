"""
The mathematical calculate exercise module.
"""

import operator
from random import randint

from contrib.cache import set_cache_task_creation_time

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

    Stores in cache the date and time of task creation for a specific
    user.

    Parameters
    ----------
    user_id : `int`
        User performing the exercise.
    calculation_type : `str`
        Alias representation of mathematical operator of task.
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
        user_id: int | None = None,
        calculation_type: str,
        min_value: int,
        max_value: int,
        timeout: int | None = None,
    ) -> None:
        """Calculation exercise constructor."""
        self.user_id = user_id
        self.timeout = timeout
        self.calculation_type = calculation_type
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
        math_sign = self._OP_SIGNS.get(calculation_type)

        question = f'{first_operand} {math_sign} {second_operand}'
        answer = self._OPS[calculation_type](first_operand, second_operand)

        # The history of exercises performed by the logged-in user is
        # stored.
        # The time of exercise creation is saved in the database after
        # the user provides an answer, before that it is stored in the
        # cache
        if self.user_id:
            self._cache_task_creation_time()

        self.question_text = question
        self.answer_text = str(answer)

    def _cache_task_creation_time(self) -> None:
        """Store in cache the date and time of task creation
        for a specific user."""
        set_cache_task_creation_time(
            user_id=self.user_id,
            exercise_type=self.calculation_type,
        )
