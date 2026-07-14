"""Domain object factory."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from .abstract import AbstractExerciseFactory
from .models import Exercise
from .protocols import ExerciseProtocol

if TYPE_CHECKING:
    from .protocols import Executable

__all__ = ('ExerciseFactory',)


class ExerciseFactory(AbstractExerciseFactory[ExerciseProtocol[Any]]):
    """Exercise factory."""

    def __init__(
        self,
        create_strategy: Executable[Any],
        check_strategy: Executable[Any],
    ) -> None:
        self._create_strategy = create_strategy
        self._check_strategy = check_strategy

    @override
    def create(self, session_id: str) -> ExerciseProtocol[Any]:
        """Create an exercise."""
        return Exercise(
            create_strategy=self._create_strategy,
            check_strategy=self._check_strategy,
            session_id=session_id,
        )
