"""Base exercise.

Exercise - current exercise type.
Task - current solution (question and answer) of exercise.
"""
from users.models import UserApp


class LogicExercise:
    """Exercise logic class."""

    def __init__(self) -> None:
        """Construct the logic."""
        super().__init__()


class CacheTask:
    """Caching of task data."""

    user: UserApp

    def __init__(self) -> None:
        """Construct the cache."""
        super().__init__()
        self.cache_time = 180  # Timeout to story task data.
        self.cache_name = str(self.user)  # Cache name of variable to story.

    def to_cache(self) -> None:
        """Cache the task data."""
        pass

    def to_check(self) -> None:
        """Get task data from cache to check user answer."""
        pass


class PointsTask:
    """Award a points in exercise."""

    def __init__(self) -> None:
        """Construct the points."""
        super().__init__()


class TaskCreator(CacheTask, LogicExercise):
    """Class to create task."""

    def __init__(self, conditions: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__()

    @property
    def data(self) -> dict:
        """The task data to render to user."""
        return {}


class AnswerHandler(CacheTask, PointsTask):
    """Class to check user answer on task, award points."""

    def __init__(self, solution: dict, user: UserApp) -> None:
        """Construct the exercise."""
        super().__init__()

    def handel(self) -> None:
        """Handel the user solution."""
