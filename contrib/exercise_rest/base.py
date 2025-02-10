"""Base exercise.

Exercise - exercise type.
Task - task of Exercise.
Question - task question.
Answer - task answer.
Solution - user solution of task.
"""

import logging
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import redis

from config.constants import REDIS_PARAMS
from mathematics.exercise import SOLUTION_MODELS
from users.models import UserApp


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

    _user: UserApp

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
        mapping = conn.hgetall(self._name)
        return mapping

    def _del_data(self) -> None:
        """Delete data from cache."""
        pass


class PointsTask:
    """Award a points in exercise."""

    def __init__(self) -> None:
        """Construct the points."""
        super().__init__()


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


class AnswerHandler(Cache, PointsTask):
    """Class to check user answer on task, award points."""

    def __init__(self, user_solution: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__(user)
        self._solution = user_solution
        self._user = user
        self._is_correctly: bool | None = None

    def _check_user_answer(self) -> bool:
        return self.cached['answer'] == self._solution['answer']

    def handel(self) -> None:
        """Handel the user solution."""
        self._is_correctly = self._check_user_answer()
        self._save_user_solution()

    @cached_property
    def cached(self) -> dict:
        """Data from cache."""
        return self._from_cache()

    def _save_user_solution(self) -> None:
        """Save to database a user task solution."""
        model = SOLUTION_MODELS[self.cached['exercise']]
        data = {
            'user': self._user,
            'calculation_type': self.cached['exercise'],
            'first_operand': self.cached['operand1'],
            'second_operand': self.cached['operand2'],
            'user_solution': self._solution['answer'],
            'is_correctly': self._is_correctly,
            # 'solution_time': None,
        }
        model.objects.create(**data)
