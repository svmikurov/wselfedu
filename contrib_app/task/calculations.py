import operator
from random import randint

from contrib_app.task.base import BaseSubject

OPS = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.or_
}


class _CalculationSubject(BaseSubject):
    """Calculation with two operand class.

    Examples:
    ---------
    subject_params = {'min_number': 2, 'max_number': 9, 'ops': '*'}
    calculation_subject.set_subject_params(**subject_params)
    """

    def __init__(self):
        super().__init__()
        self._number_range = None
        self._first_operand = None
        self._second_operand = None
        self._ops = None

    def set_subject_params(self, *, min_number, max_number, ops):
        """Set subject task params."""
        if min_number > max_number:
            raise ValueError('min_number greater than max_number')
        if not isinstance(min_number, int) or not isinstance(max_number, int):
            raise ValueError('number expected')
        if ops not in OPS:
            raise ValueError("operators must be: '+' or '-' or '*' or '/'")

        self._number_range = (min_number, max_number)
        self._ops = ops
        self._first_operand = self._get_random_operand_value()
        self._second_operand = self._get_random_operand_value()
        super().set_subject_params()

    def _get_random_operand_value(self):
        """Get random operand value."""
        return randint(*self._number_range)

    def _set_task_solution(self):
        """Create and set question and answer text."""
        self._question_text = (
            f"{self._first_operand} {self._ops} {self._second_operand}"
        )
        answer = OPS[self._ops](self._first_operand, self._second_operand)
        self._answer_text = str(answer)


calculation_subject = _CalculationSubject()
