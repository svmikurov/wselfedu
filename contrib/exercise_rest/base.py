"""Base exercise.

Exercise - current exercise type.
Task - current solution (question and answer) of exercise.
"""
import logging
from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import redis

from config.constants import REDIS_PARAMS
from mathematics.exercise import CalcExercise
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
        self._answer = self._solution['answer']
        self._user = user

    def _check_user_answer(self) -> bool:
        return CalcExercise.check_answer(*self.cached.values(), self._answer)

    def handel(self) -> None:
        """Handel the user solution."""
        is_correct = self._check_user_answer()
        logging.info(f'>>> {is_correct = }')

    @cached_property
    def cached(self):
        return self._from_cache()
