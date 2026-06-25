"""Request handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar

from wse.application.commands import CreateTestingTask

from .dtos import ResponseDto

if TYPE_CHECKING:
    from wse.application.protocols import (
        CerateTestingCommandProto,
        Executable,
        TaskDtoProto,
    )
    from wse.domain.protocols import Testable

    from .protocols import HasContext, SimpleRequestParamsProto

ContextT = TypeVar('ContextT')
DataT = TypeVar('DataT')

type UseCaseT = Executable[CerateTestingCommandProto, TaskDtoProto[Testable]]


class ExerciseHandler:
    """Exercise performing request handler."""

    def __init__(
        self,
        use_case: UseCaseT,
    ) -> None:
        self._use_case = use_case

    def execute(
        self,
        params: SimpleRequestParamsProto[ContextT, DataT],
    ) -> HasContext[dict[str, str]]:
        """Execute the exercise request."""
        command = CreateTestingTask(session_id='session_123')
        result = self._use_case.execute(command)
        return ResponseDto(
            context={'question_text': result.task.question_text}
        )
