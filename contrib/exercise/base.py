"""Base exercise.

Exercise - exercise type.
Task - task of Exercise.
Question - task question.
Answer - user answer.
Solution - solution of task.
"""

from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import redis
from django.core.exceptions import ValidationError

from config.constants import REDIS_PARAMS
from mathematics.models import MathematicsAnalytic
from users.models import UserApp
from users.models.points import UserAccount

SAVE_ANSWER_MODELS = {
    'mul': MathematicsAnalytic,
}


class BaseExercise(ABC):
    """Base exercise class."""

    @abstractmethod
    def create_task(self) -> None:
        """Create a task."""
        pass

    @property
    @abstractmethod
    def task_data(self) -> dict[str, str]:
        """Task data."""
        pass

    @property
    @abstractmethod
    def cache_data(self) -> dict[str, Any]:
        """Cache a task data."""
        pass


class Cache:
    """Caching of data."""

    def __init__(self, user: UserApp) -> None:
        """Construct the cache."""
        super().__init__()
        self._time = 180
        self._name = str(user)

    def _to_cache(self, mapping: dict[str, Any]) -> None:
        """Cache the data."""
        conn = redis.Redis(**REDIS_PARAMS)
        conn.hset(self._name, mapping=mapping)
        conn.expire(self._name, self._time)

    def _from_cache(self) -> dict:
        """Get data from cache."""
        conn = redis.Redis(**REDIS_PARAMS)
        data = conn.hgetall(self._name)
        return data


class TaskCreator(Cache):
    """Class to create task."""

    def __init__(self, exercise: BaseExercise, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__(user)
        self._exercise = exercise
        self._user = user

    def _create_task(self) -> None:
        self._exercise.create_task()

    def _cache_task_data(self) -> None:
        # Task data is cached to check the user's answer.
        self._to_cache(self._exercise.cache_data)

    @property
    def data(self) -> dict:
        """The task data to render to user."""
        self._create_task()
        self._cache_task_data()
        data = self._exercise.task_data
        return data


class AnswerHandler(Cache):
    """Class to check user answer on task, award points."""

    def __init__(self, answer: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__(user)
        self._answer = answer

        self._user = user
        self._answer_is_correct: bool | None = None
        # TODO: Fix annotation, the choice of the task model
        #       is carried out programmatically.
        self._task: MathematicsAnalytic | None = None
        self._points = 5

    def handel(self) -> None:
        """Handel the user solution."""
        self._check_answer()
        self._save_answer()
        if self._answer_is_correct and self.has_award:
            self._add_award()
        else:
            self._add_penalty()

    def _check_answer(self) -> None:
        self._answer_is_correct = (
            self.cached['solution'] == self._answer['answer']
        )

    def _save_answer(self) -> None:
        """Save to database a user task solution."""
        model = SAVE_ANSWER_MODELS[self.cached['exercise']]
        data = {
            'user': self._user,
            'calculation_type': self.cached['exercise'],
            'first_operand': self.cached['operand1'],
            'second_operand': self.cached['operand2'],
            'user_solution': self._answer['answer'],
            'is_correctly': self._answer_is_correct,
            # 'solution_time': None,
        }
        self._task = model.objects.create(**data)

    @property
    def has_award(self) -> bool:
        """Has user award."""
        return True

    def _add_award(self) -> None:
        """Add award point to user account."""
        account, _ = UserAccount.objects.get_or_create(user=self._user)
        try:
            account.add_award(self._points)
        except ValidationError as e:
            print(e)

    def _add_penalty(self) -> None:
        pass

    @cached_property
    def cached(self) -> dict:
        """Data from cache."""
        return self._from_cache()


def handel_answer(answer: dict, user: UserApp) -> None:
    """Handel the user answer."""
    AnswerHandler(answer, user).handel()
