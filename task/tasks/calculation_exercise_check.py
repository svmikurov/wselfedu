import os

from django.forms import Form
from django.http import HttpRequest
from dotenv import load_dotenv

from task.models import Points
from task.models.exercises_math import MathematicalExercise
from task.points import get_points_balance
from users.models import UserModel

load_dotenv('.env_vars/.env.wse')

POINTS_FOR_THE_TASK = int(os.getenv('POINTS_FOR_THE_TASK'))
"""The number of points awarded for a correctly completed task,
by default (`int`).
"""
MAX_POINTS_BALANCE = int(os.getenv('MAX_POINTS_BALANCE'))
"""The maximum allowed accumulation of points on the user's balance.
(`int`)
"""


class CalculationExerciseCheck:
    """Calculation exercise check class."""

    MATH_CALCULATION_TYPE = ('add', 'sub', 'mul', 'div')

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
        self.question_text: str = request.session.get('question_text')
        self.answer_text: str = request.session.get('answer_text')
        self.calculation_type: str = request.session.get('calculation_type')
        self.first_operand: int = int(self.question_text.split()[0])
        self.second_operand: int = int(self.question_text.split()[-1])
        self.user_solution: str = str(form.cleaned_data.get('user_solution'))
        self.is_correct_answer: bool | None = None
        # self.solution_time = get_cache_task_creation_time(
        #     self.user_id,
        #     self.calculation_type,
        # )
        self.task_id: int | None = None

    @property
    def solution_time(self):
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
        user = UserModel.objects.get(pk=self.user_id)
        task_query = MathematicalExercise.objects.create(
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
        """
        # Temporary number_points is fixed number.
        number_points = POINTS_FOR_THE_TASK
        return number_points

    def accrue_reward(self) -> None:
        """Award points to the user for solving the task correctly."""
        user = UserModel.objects.get(pk=self.user_id)
        task = MathematicalExercise.objects.get(pk=self.task_id)
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
