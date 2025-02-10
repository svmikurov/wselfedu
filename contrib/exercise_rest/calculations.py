"""The mathematical calculate exercise."""

import os
from abc import ABC, abstractmethod
from typing import Any

from dotenv import load_dotenv

load_dotenv('.env_vars/.env.wse')

POINTS_FOR_THE_TASK = int(os.getenv('POINTS_FOR_THE_TASK', 0))
"""The number of points awarded for a correctly completed task,
by default (`int`).
"""
MAX_POINTS_BALANCE = int(os.getenv('MAX_POINTS_BALANCE', 0))
"""The maximum allowed accumulation of points on the user's balance.
(`int`)
"""


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

    @abstractmethod
    def check_answer(self, *args: object) -> bool:
        """Check the answer."""
        pass
