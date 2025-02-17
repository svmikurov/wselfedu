"""Base exercise."""

from abc import ABC, abstractmethod
from typing import Type

from django.core.exceptions import ValidationError
from djoser.conf import User

from contrib.exercise.cache import RedisTaskCache
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
