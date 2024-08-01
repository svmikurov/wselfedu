"""Task manager module."""

from datetime import timezone, datetime

from django.core.cache import cache
from django.forms import Form
from django.http import HttpRequest

CACHE_STORAGE_TIME = 300
"""The number of seconds the value should be stored in the cache
(`int`).
"""

MATH_CALCULATION_TYPE = ('add', 'sub', 'mul', 'div')


class TaskManager:
    """Task manager class.
    """

    def __init__(
        self,
        *,
        request: HttpRequest | None = None,
        form: Form | None = None,
    ) -> None:
        self.request = request
        self.form = form

    def check_user_to_reward(self) -> bool:
        return True

    def accrue_reward(self) -> None:
        return None

    def check_user_solution(self) -> bool:
        """"""
        answer_text = self.request.session.get('answer_text')
        user_solution = str(self.form.cleaned_data.get('user_solution'))
        is_correct_answer = answer_text == user_solution

        # The logged in user may be awarded points for completing the
        # task correctly.
        # Points are awarded only to those users who have a guardian.
        # The user is limited by the amount of reward per day.
        should_user_be_rewarded = self.check_user_to_reward()
        if should_user_be_rewarded:
            self.accrue_reward()

        return is_correct_answer

    @staticmethod
    def time_cache_key(user_id: int, exercise_type: str) -> str:
        """Key to get start time exercise from cache."""
        cache_key = f'user_{user_id}_exc_{exercise_type}_start_time'
        return cache_key

    def set_cache_task_creation_time(
        self,
        user_id: int,
        exercise_type: str,
    ) -> None:
        """Store in cache the date and time of task creation
        for a specific user."""
        key = self.time_cache_key(user_id, exercise_type)
        data_time_now = datetime.now(tz=timezone.utc)
        cache.set(key, data_time_now, CACHE_STORAGE_TIME)

    def get_cache_task_creation_time(
        self,
        user_id: int,
        exercise_type: str,
    ) -> object:
        """Get from cache the date and time of task creation
        for a specific user."""
        key = self.time_cache_key(user_id, exercise_type)
        return cache.get(key)
