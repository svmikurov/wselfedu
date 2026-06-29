"""Request handlers."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeVar, override

from wse.application.commands import CreateTestingTask

from .abstract import AbstractRequestHandler
from .dtos import ResponseDto
from .protocols import (
    HasContext,
    HasSessionIdentifier,
    SimpleRequestParamsProto,
)

if TYPE_CHECKING:
    from wse.application.protocols import (
        CerateTestingCommandProto,
        Executable,
        TaskDtoProto,
    )
    from wse.domain.protocols import Testable


ContextT = TypeVar('ContextT', bound=HasSessionIdentifier)
DataT = TypeVar('DataT')

type UseCaseT = Executable[CerateTestingCommandProto, TaskDtoProto[Testable]]


class ExerciseHandler(
    AbstractRequestHandler[
        SimpleRequestParamsProto[ContextT, DataT],
        HasContext[dict[str, str]],
    ]
):
    """Exercise performing request handler."""

    def __init__(
        self,
        use_case: UseCaseT,
    ) -> None:
        self._use_case = use_case

    @override
    def handle(
        self,
        params: SimpleRequestParamsProto[ContextT, DataT],
    ) -> HasContext[dict[str, str]]:
        """Handle the exercise request."""
        command = CreateTestingTask(session_id=params.context.session_id)
        result = self._use_case.execute(command)
        return ResponseDto(
            context={'question_text': result.task.question_text}
        )
