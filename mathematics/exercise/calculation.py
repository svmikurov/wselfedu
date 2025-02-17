"""The mathematical calculate exercise module."""

import operator
from functools import cached_property
from random import randint

from django.forms import Form
from django.http import HttpRequest

from config.constants import (
    ADDITION,
    DIVISION,
    MULTIPLICATION,
    SUBSTRUCTION,
)
from contrib.cache import set_cache_task_creation_time
from mathematics.models import MathematicsTasks
from users.models import UserApp


class CalcExercise:
    """Calculation exercise with two operands."""

    _OPS = {
        'add': operator.add,
        'sub': operator.sub,
        'mul': operator.mul,
    }
    """Alias representation of mathematical operators."""
    _OP_SIGNS = {
        'add': '+',
        'sub': '-',
        'mul': 'x',
    }
    """Alias representation of mathematical sign."""

    def __init__(
        self,
        exercise: str,
        *,
        min_value: int = 1,
        max_value: int = 9,
    ) -> None:
        """Construct calculation exercise."""
        self._exercise: str = exercise
        self._min_value: int = min_value
        self._max_value: int = max_value
        self._operand1: int | None = None
        self._operand2: int | None = None
        self._question: str | None = None
        self._solution: int | None = None

    def create_task(self) -> None:
        """Create a task."""
        self._operand1 = randint(self._min_value, self._max_value)
        self._operand2 = randint(self._min_value, self._max_value)
        task_data = self._exercise, self._operand1, self._operand2

        self._question = self._create_question(*task_data)
        self._solution = self._create_solution(*task_data)

    @classmethod
    def _create_question(
        cls, exercise_type: str, operand1: int, operand2: int
    ) -> str:
        math_sign = cls._OP_SIGNS.get(exercise_type)
        return f'{operand1} {math_sign} {operand2}'

    @classmethod
    def _create_solution(
        cls, exercise_type: str, operand1: int, operand2: int
    ) -> int:
        return cls._OPS[exercise_type](operand1, operand2)

    @property
    def data_to_render(self) -> dict:
        """Task data to render."""
        return {
            'question': self._question,
            'solution': self._solution,
        }

    @cached_property
    def data_to_cache(self) -> dict:
        """Task data to cache."""
        return {
            'exercise': self._exercise,
            'operand1': self._operand1,
            'operand2': self._operand2,
            'solution': self._solution,
        }


class CalcExerciseBrowser:
    """Calculation exercise class with two operands for browser."""

    _OPS = {
        'add': operator.add,
        'sub': operator.sub,
        'mul': operator.mul,
    }
    """Alias representation of mathematical operators."""
    _OP_SIGNS = {
        'add': '+',
        'sub': '-',
        'mul': 'x',
    }
    """Alias representation of mathematical sign."""
    question_text = None
    answer_text = None

    def __init__(
        self,
        *,
        user_id: int | None = None,
        calculation_type: str,
        min_value: int = 1,
        max_value: int = 9,
        timeout: int | None = None,
    ) -> None:
        """Construct calculation exercise."""
        self.user_id = user_id
        self.timeout = timeout
        self.calculation_type = calculation_type
        # Create task
        self._create_task(calculation_type, min_value, max_value)

    def _create_task(
        self,
        calc_type: str,
        min_value: int,
        max_value: int,
    ) -> None:
        """Create a question and answer."""
        first_operand = randint(min_value, max_value)
        second_operand = randint(min_value, max_value)
        math_sign = self._OP_SIGNS.get(calc_type)

        self.question_text = f'{first_operand} {math_sign} {second_operand}'
        self.answer_text = str(
            self._OPS[calc_type](first_operand, second_operand)
        )

        if self.user_id:
            self._cache_task_creation_time()

    def _cache_task_creation_time(self) -> None:
        """Store in cache the date and time of task creation."""
        set_cache_task_creation_time(
            user_id=self.user_id,
            exercise=self.calculation_type,
        )

    # @property
    # def data(self) -> dict[str, str]:
    #     """Task data."""
    #     return {
    #         'question': self.question_text,
    #         'answer': self.answer_text,
    #     }


class CalculationExerciseCheck:
    """Calculation exercise check class."""

    MATH_CALCULATION_TYPE = (ADDITION, SUBSTRUCTION, MULTIPLICATION, DIVISION)
    user_id: int | None = None

    def __init__(self, *, request: HttpRequest, form: Form) -> None:
        """Construct check calculation exercise."""
        self.request = request
        self.form = form
        self.user_id: int = request.user.id
        self.question_text: str = request.session.get('question_text')
        self.answer_text: str = request.session.get('answer_text')
        self.calculation_type: str = request.session.get('calculation_type')
        self.first_operand: int = int(self.question_text.split()[0])
        self.second_operand: int = int(self.question_text.split()[-1])
        self.user_solution: str = str(form.cleaned_data.get('user_solution'))
        self.is_correct_answer: bool | None = None
        self.task_id: int | None = None

    @property
    def solution_time(self) -> int:
        """Time for user to solve the task (reade-only)."""
        # Temporary solution_time is fixed number.
        return 3

    def check_user_to_reward(self) -> bool:
        """Check if points should be awarded to the user."""
        pass

    def save_task_to_db(self) -> None:
        """Save task conditions and user solution to database."""
        user = UserApp.objects.get(pk=self.user_id)
        task_query = MathematicsTasks.objects.create(
            user=user,
            calculation_type=self.calculation_type,
            first_operand=self.first_operand,
            second_operand=self.second_operand,
            user_solution=self.user_solution,
            is_correctly=self.is_correct_answer,
            solution_time=self.solution_time,
        )
        task_query.save()
        task_id = task_query.pk
        self.task_id = task_id

    @property
    def award(self) -> int:
        """The number of points as a reward for success task solution
        (`int`, read-only).
        """  # noqa:  D205
        pass

    def check_and_save_user_solution(self) -> bool:
        """Check and save the user task with its solution."""
        try:
            assert self.calculation_type in self.MATH_CALCULATION_TYPE
            self.is_correct_answer = self.answer_text == self.user_solution
            if self.user_id:
                self.save_task_to_db()
        except AssertionError as exc:
            raise AttributeError(
                f'This class only checks the following calculations: '
                f'{self.MATH_CALCULATION_TYPE}'
            ) from exc

        # The logged-in user may be awarded points for completing the
        # task correctly.
        # Points are awarded only to those users who have a mentor.
        # The user is limited by the amount of reward per day.
        if self.is_correct_answer:
            should_user_be_rewarded = self.check_user_to_reward()
            if should_user_be_rewarded:
                # Points are not accumulated temporarily.
                pass

        return self.is_correct_answer
