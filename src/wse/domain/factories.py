"""Domain object factory."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, override

from .abstract import AbstractExerciseFactory
from .model import Exercise, Presentation
from .protocols import ExerciseProtocol, Presentable

ExerciseT = ExerciseProtocol[Any, Any, Any, Any, Any]
PresentationT = Presentable[Any]

if TYPE_CHECKING:
    from typing import TypeAlias

    from .protocols import Executable

    StrategyT: TypeAlias = Executable[Any, Any]

__all__ = (
    'ExerciseFactory',
    'PresentationFactory',
)


class ExerciseFactory(AbstractExerciseFactory[ExerciseT]):
    """Exercise factory."""

    def __init__(
        self,
        create_strategy: StrategyT,
        check_strategy: StrategyT,
    ) -> None:
        self._create_strategy = create_strategy
        self._check_strategy = check_strategy

    @override
    def create(self, session_id: str) -> ExerciseT:
        """Create an exercise."""
        return Exercise(
            create_strategy=self._create_strategy,
            check_strategy=self._check_strategy,
            session_id=session_id,
        )


class PresentationFactory(AbstractExerciseFactory[PresentationT]):
    """Presentation exercise factory."""

    def __init__(
        self,
        create_strategy: StrategyT,
    ) -> None:
        self._create_strategy = create_strategy

    @override
    def create(self, session_id: str) -> PresentationT:
        """Create a presentation exercise."""
        return Presentation(
            create_strategy=self._create_strategy,
            session_id=session_id,
        )
