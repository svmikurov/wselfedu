"""Protocol for exercise process parameters adapter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import ExerciseProcessAdapterProtocol

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
CurrentCaseT = TypeVar('CurrentCaseT')
AdaptedT = TypeVar('AdaptedT')


class AbstractExerciseProcessAdapter(
    ABC,
    ExerciseProcessAdapterProtocol[
        CommandT,
        ParamsT,
        CurrentCaseT,
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
        current_case: CurrentCaseT | None,
    ) -> AdaptedT:
        """Adapt for exercise precess execute."""
