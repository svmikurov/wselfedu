"""Protocol for exercise process parameters adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import ExerciseProcessAdapterProtocol

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
ExistingCaseT = TypeVar('ExistingCaseT')
AdaptedT = TypeVar('AdaptedT')


class AbstractExerciseProcessAdapter(
    ABC,
    ExerciseProcessAdapterProtocol[
        CommandT,
        ParamsT,
        ExistingCaseT,
        AdaptedT,
    ],
):
    """Protocol for adapt parameters for exercise process interface."""

    @override
    @abstractmethod
    def adapt(
        self,
        command: CommandT,
        params: ParamsT,
        case: ExistingCaseT | None,
    ) -> AdaptedT:
        """Adapt for exercise precess execute."""
