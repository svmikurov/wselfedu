"""Use case strategy."""

import logging
from typing import Any, Generic, TypeVar, override

from apps.core.assemblers.protocol import DataCommandProtocol
from apps.core.domains.exercise.enums import ExerciseProcessEnum
from apps.core.use_cases.protocol import UseCaseProtocol
from apps.core.validators.request.data import ProcessExerciseWebData

from .abstract import AbstractUseCase

_DataCommandProtocol = DataCommandProtocol[ProcessExerciseWebData]

Command = TypeVar('Command', bound=_DataCommandProtocol)
UseCase = TypeVar('UseCase', bound=UseCaseProtocol[_DataCommandProtocol, Any])
Result = TypeVar('Result')

log = logging.getLogger(__name__)


class ProcessExerciseUseCaseStrategy(
    AbstractUseCase[Command, Result],
    Generic[Command, Result],
):
    """Process exercise use case strategy."""

    def __init__(
        self,
        registry: dict[ExerciseProcessEnum, UseCase],
    ) -> None:
        """Construct the strategy."""
        self._registry = registry

    @override
    def execute(self, command: Command) -> Result:
        """Execute."""
        action = command.data.action  # type: ignore

        try:
            use_case = self._registry[action]
        except KeyError as exc:
            log.error(
                f'Process exercise use case strategy error, '
                f'no registered process exercise use case for '
                f'"{action}" action.\n'
                f'Register the {exc} strategy key.'
            )
            raise

        return use_case.execute(command)  # type: ignore
