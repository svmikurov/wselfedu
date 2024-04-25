import operator
from random import randint

from contrib_app.task.base_subject import BaseSubject

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


class _CalculationSubject(BaseSubject):
    """Calculation class with two operands."""

    def __init__(self):
        super().__init__()
        self._value_range = None
        self._first_operand = None
        self._second_operand = None
        self._ops = None

    def apply_subject(
            self,
            *,
            min_value,
            max_value,
            calculation_type,
            **kwargs
    ):
        """Apply the subject for task."""
        if min_value >= max_value:
            raise ValueError('min_value must be less than max_value')
        if not isinstance(min_value, int) or not isinstance(max_value, int):
            raise ValueError('number expected')
        if calculation_type not in OPS:
            raise ValueError(
                "calculation_type must be: '+' or '-' or '*' or '/'"
            )

        setattr(self, '_value_range', (min_value, max_value))
        setattr(self, '_first_operand', self._get_random_operand_value)
        setattr(self, '_second_operand', self._get_random_operand_value)
        setattr(self, '_ops', calculation_type)
        super().apply_subject()

    def _set_task_solution(self):
        """Create and set question text with answer text."""
        question = f"{self._first_operand} {self._ops} {self._second_operand}"
        answer = str(OPS[self._ops](self._first_operand, self._second_operand))
        setattr(self, '_question_text', question)
        setattr(self, '_answer_text', answer)

    @property
    def _get_random_operand_value(self):
        """Get random operand value."""
        return randint(*self._value_range)

    @property
    def subject_name(self):
        """Get subject name."""
        return 'calculation_subject'

    def __str__(self):
        return 'Математические вычисления'


calculation_subject = _CalculationSubject()
