"""Exercise process adapter."""

from typing import Generic, TypeVar, override

from .abstract import AbstractExerciseProcessAdapter

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
ExistingCaseT = TypeVar('ExistingCaseT')
AdaptedT = TypeVar('AdaptedT')


class ExerciseProcessAdapter(
    AbstractExerciseProcessAdapter[CommandT, ParamsT, ExistingCaseT, AdaptedT],
    Generic[CommandT, ParamsT, ExistingCaseT, AdaptedT],
):
    """Exercise process adapter."""

    @override
    def adapt(
        self,
        command: CommandT,
        params: ParamsT,
        existing_case: ExistingCaseT | None,
    ) -> AdaptedT:
        """Adapt for exercise process execute."""
        raise NotImplementedError
