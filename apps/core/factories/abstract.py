"""Abstract base class for exercise specification factory."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from ports.contract.infra.spec import ExerciseSpecFactoryProtocol

CommandT = TypeVar('CommandT')
ParamsT = TypeVar('ParamsT')
ExistingCaseT = TypeVar('ExistingCaseT')
SpecT = TypeVar('SpecT')


class AbstractExerciseSpecFactory(
    ABC,
    ExerciseSpecFactoryProtocol[
        CommandT,
        ParamsT,
        ExistingCaseT,
        SpecT,
    ],
):
    """ABC for exercise specification factory."""

    @override
    @abstractmethod
    def create(
        self,
        command: CommandT,
        params: ParamsT,
        case: ExistingCaseT | None,
    ) -> SpecT:
        """Create the exercise specification."""
