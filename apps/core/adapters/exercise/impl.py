"""Exercise process adapter."""

from typing import Generic, TypeVar, override

from .abstract import AbstractExerciseProcessAdapter

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
CurrentCaseT = TypeVar('CurrentCaseT')
AdaptedT = TypeVar('AdaptedT')


class ExerciseProcessAdapter(
    AbstractExerciseProcessAdapter[CommandT, ParamsT, CurrentCaseT, AdaptedT],
    Generic[CommandT, ParamsT, CurrentCaseT, AdaptedT],
):
    """Exercise process adapter."""

    @override
    def adapt(
        self,
        command: CommandT,
        params: ParamsT,
        current_case: CurrentCaseT | None,
    ) -> AdaptedT:
        """Adapt for exercise process execute."""
        raise NotImplementedError
