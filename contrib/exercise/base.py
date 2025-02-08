"""Base exercise.

Exercise - current exercise type.
Task - current solution (question and answer) of exercise.
"""

import redis

from config.constants import REDIS_PARAMS
from contrib.exercise.calculations import CalculationExercise
from users.models import UserApp



class CacheTask:
    """Caching of task data."""

    _user: UserApp

    def __init__(self) -> None:
        """Construct the cache."""
        super().__init__()
        self.cache_time = 180
        self.cache_name = f'task_{self._user}'

    def _to_cache(self, mapping: dict) -> None:
        """Cache the task data."""
        conn = redis.Redis(**REDIS_PARAMS)
        conn.hset(self.cache_name, mapping=mapping)

    def _from_cache(self) -> dict:
        """Get task data from cache to check user answer."""
        conn = redis.Redis(**REDIS_PARAMS)
        mapping = conn.hgetall(self.cache_name)
        return mapping


class PointsTask:
    """Award a points in exercise."""

    def __init__(self) -> None:
        """Construct the points."""
        super().__init__()


class TaskCreator(CacheTask):
    """Class to create task."""

    EXERCISES = {
        'mul': CalculationExercise(calc_type='mul'),
    }

    def __init__(self, conditions: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__()
        exercise_type = conditions['exercise_type']
        exercise_class = self.EXERCISES[exercise_type]
        self._exercise = exercise_class()
        self._user = user

    def _create_task(self) -> None:
        self._exercise.create_task()
        # Task data is cached to check the user's answer.
        self._to_cache(self._exercise.cache_data)

    @property
    def data(self) -> dict:
        """The task data to render to user."""
        self._create_task()
        data = self._exercise.task_data
        return data


class AnswerHandler(CacheTask, PointsTask):
    """Class to check user answer on task, award points."""

    def __init__(self, solution: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__()

    def handel(self) -> None:
        """Handel the user solution."""
        pass
