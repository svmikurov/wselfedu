"""Application layer request handler result adapter."""

from wse.application.protocols import HasTask
from wse.domain.protocols import Testable

from .. import dto
from ..interfaces.response import CreateTestingTaskContext
from ..interfaces.protocols import HasContext, NullProto
from .abstract import AbstractAdapter


class NullAdapter(
    AbstractAdapter[NullProto, NullProto, NullProto],
):
    """Null adapter."""

    def to_response(self, source: NullProto, context: NullProto) -> NullProto:
        """Return original data."""
        return source


class CreateTestingAdapter(
    AbstractAdapter[
        HasTask[Testable],
        NullProto,
        HasContext[CreateTestingTaskContext],
    ],
):
    """Adapter for create testing task web response context."""

    def to_response(
        self,
        source: HasTask[Testable],
        context: NullProto,
    ) -> HasContext[CreateTestingTaskContext]:
        """Adapt for web response context."""
        return dto.ResponseDto(
            context={'question_text': source.task.question_text},
        )
