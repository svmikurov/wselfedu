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


class Calculation:
    """Exercise on calculation of two numbers."""

    def __init__(self) -> None:
        """Construct the calculation."""
        super().__init__()


class BaseExercise(CacheTask, PointsTask, LogicExercise):
    """Base exercise class."""

    def __init__(self) -> None:
        """Construct the exercise."""
        super().__init__()


class CalculationExercise(Calculation, BaseExercise):
    """Calculation exercise."""

    def __init__(self) -> None:
        """Construct the exercise."""
        super().__init__()
