"""The mathematical calculate exercise module."""

import operator
import os
from random import randint

from django.forms import Form
from django.http import HttpRequest
from dotenv import load_dotenv

from config.constants import (
    ADDITION,
    ANSWER_TEXT,
    CALCULATION_TYPE,
    DIVISION,
    MULTIPLICATION,
    QUESTION_TEXT,
    SUBSTRUCTION,
    USER_SOLUTION,
)
from contrib.cache import set_cache_task_creation_time
from mathematics.models import MathematicsAnalytic
from users.models import Points, UserApp
from users.points import get_points_balance

load_dotenv('.env_vars/.env.wse')

POINTS_FOR_THE_TASK = int(os.getenv('POINTS_FOR_THE_TASK', 0))
"""The number of points awarded for a correctly completed task,
by default (`int`).
"""
MAX_POINTS_BALANCE = int(os.getenv('MAX_POINTS_BALANCE', 0))
"""The maximum allowed accumulation of points on the user's balance.
(`int`)
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
        ADDITION: operator.add,
        SUBSTRUCTION: operator.sub,
        MULTIPLICATION: operator.mul,
    }
    """Alias representation of mathematical operators
    (`Dict[str, object]`).
    """
    _OP_SIGNS = {
        ADDITION: '+',
        SUBSTRUCTION: '-',
        MULTIPLICATION: '*',
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
        """Construct calculation exercise."""
        self.user_id = user_id
        self.timeout = timeout
        self.calculation_type = calculation_type
        # Create task
        self._set_task_solution(calculation_type, min_value, max_value)

    def _set_task_solution(  # noqa: D417
        self,
        calculation_type: str,
        *value_range: tuple,
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
        """Store in cache the date and time of task creation."""
        set_cache_task_creation_time(
            user_id=self.user_id,
            exercise_type=self.calculation_type,
        )


class CalculationExerciseCheck:
    """Calculation exercise check class."""

    MATH_CALCULATION_TYPE = (ADDITION, SUBSTRUCTION, MULTIPLICATION, DIVISION)

    user_id: int | None = None
    """Current user id (`int | None`).
    """

    def __init__(
        self,
        *,
        request: HttpRequest,
        form: Form,
    ) -> None:
        """Construct check calculation exercise."""
        self.request = request
        self.form = form
        self.user_id: int = request.user.id
        self.question_text: str = request.session.get(QUESTION_TEXT)
        self.answer_text: str = request.session.get(ANSWER_TEXT)
        self.calculation_type: str = request.session.get(CALCULATION_TYPE)
        self.first_operand: int = int(self.question_text.split()[0])
        self.second_operand: int = int(self.question_text.split()[-1])
        self.user_solution: str = str(form.cleaned_data.get(USER_SOLUTION))
        self.is_correct_answer: bool | None = None
        # self.solution_time = get_cache_task_creation_time(
        #     self.user_id,
        #     self.calculation_type,
        # )
        self.task_id: int | None = None

    @property
    def solution_time(self) -> int:
        """Time for user to solve the task (reade-only)."""
        # Temporary solution_time is fixed number.
        return 3

    def check_user_to_reward(self) -> bool:
        """Check if points should be awarded to the user."""
        if not self.user_id:
            return False
        elif get_points_balance(self.user_id) >= MAX_POINTS_BALANCE:
            return False
        else:
            return True

    def save_task_to_db(self) -> None:
        """Save task conditions and user solution to database."""
        user = UserApp.objects.get(pk=self.user_id)
        task_query = MathematicsAnalytic.objects.create(
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
        # Temporary number_points is fixed number.
        number_points = POINTS_FOR_THE_TASK
        return number_points

    def accrue_reward(self) -> None:
        """Award points to the user for solving the task correctly."""
        user = UserApp.objects.get(pk=self.user_id)
        task = MathematicsAnalytic.objects.get(pk=self.task_id)
        balance = get_points_balance(self.user_id)

        query = Points.objects.create(
            user=user,
            task=task,
            award=self.award,
            balance=balance + self.award,
        )
        query.save()

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
                self.accrue_reward()

        return self.is_correct_answer
