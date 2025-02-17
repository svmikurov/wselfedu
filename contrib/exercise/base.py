"""Base exercise.

Exercise - exercise type.
Task - task of Exercise.
Question - task question.
Answer - user answer.
Solution - solution of task.
"""
import logging
from abc import ABC, abstractmethod
from typing import Any, Type

import redis
from django.core.exceptions import ValidationError
from djoser.conf import User

from config.constants import REDIS_PARAMS
from mathematics.exercise import EXERCISES
from mathematics.models import MathematicsTasks
from users.models import UserApp
from users.models.points import Transaction, UserAccount

SAVE_ANSWER_MODELS = {
    'mul': MathematicsTasks,
}


class BaseExercise(ABC):
    """Base exercise class."""

    @abstractmethod
    def create_task(self) -> None:
        """Create a task."""
        raise NotImplementedError('The create_task() is not implemented')

    @property
    @abstractmethod
    def data_to_render(self) -> dict:
        """Task data to render."""
        raise NotImplementedError('The data_to_render() is not implemented')

    @property
    @abstractmethod
    def data_to_cache(self) -> dict:
        """Task data to cache."""
        raise NotImplementedError('The data_to_cache() is not implemented')


class TaskStory:
    """Task data story."""

    def __init__(self, user: UserApp) -> None:
        """Construct the story."""
        self._user = user

    def save_data(self, mapping: dict[str, Any]) -> None:
        """Save task data."""
        raise NotImplementedError('The method save_data is not implemented')

    def get_data(self) -> dict:
        """Get data."""
        raise NotImplementedError('The method get_data is not implemented')


class RedisTaskCache(TaskStory):
    """Story data in Redis."""

    def __init__(self, user: UserApp) -> None:
        """Construct the story."""
        super().__init__(user)
        self._time = 180
        self._name = str(user)

    def save_data(self, mapping: dict[str, Any]) -> None:
        """Cache the data."""
        conn = redis.Redis(**REDIS_PARAMS)
        conn.hset(self._name, mapping=mapping)
        conn.expire(self._name, self._time)

    def get_data(self) -> dict:
        """Get data from cache."""
        conn = redis.Redis(**REDIS_PARAMS)
        data = conn.hgetall(self._name)
        return data


########################################################################
# View task functions


def award_points(user: UserApp, points: int) -> Transaction:
    """Award user points to account."""
    account, _ = UserAccount.objects.get_or_create(user=user)
    try:
        transaction = account.add_award(points)
    except ValidationError as e:
        print(e)
        transaction = None
    return transaction


def save_answer(user: UserApp, **data: object) -> None:
    """Save the user answer."""
    model = SAVE_ANSWER_MODELS[data['exercise']]
    model.objects.create(user=user, **data)


def has_award() -> bool:
    """Has user an awards."""
    return True


def get_award(user: UserApp) -> int:
    """Get user award for task."""
    return 5


def create_task(exercise_conditions: dict, user: Type[User]) -> BaseExercise:
    """Create task."""
    exercise_class = EXERCISES[exercise_conditions['exercise']]
    task = exercise_class(**exercise_conditions)
    task.create_task()

    if task.data_to_cache:
        RedisTaskCache(user).save_data(task.data_to_cache)

    return task


def handel_answer(answer: dict, user: Type[User]) -> bool:
    """Handel the user answer."""
    award = get_award(user)
    task_data = RedisTaskCache(user).get_data()
    task_data['is_correctly'] = task_data.pop('solution') == answer['answer']

    if task_data['is_correctly'] and has_award():
        transaction = award_points(user, award)
    else:
        transaction = None

    save_answer(user=user, **task_data, **answer, transaction=transaction)
    return task_data['is_correctly']
