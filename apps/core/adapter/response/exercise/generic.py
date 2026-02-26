"""Generic response adapters."""

from typing import Generic, TypeVar

from apps.core.domain.exercise.enums import ExerciseStatusEnum
from apps.core.domain.exercise.types import ExerciseStatus
from apps.core.handlers.protocol import (
    RequestResultProtocol,
    SimpleResponseAdapter,
)

DomainResultDTO = TypeVar('DomainResultDTO', bound=ExerciseStatus)


class ResultStrategyAdapter(
    SimpleResponseAdapter[DomainResultDTO],
    Generic[DomainResultDTO],
):
    """Router for new case or explain current case adapter select."""

    def __init__(
        self,
        new_case_adapter: SimpleResponseAdapter[DomainResultDTO],
        explain_adapter: SimpleResponseAdapter[DomainResultDTO],
    ) -> None:
        """Construct the adapter."""
        self._new_case_adapter = new_case_adapter
        self._explain_adapter = explain_adapter

    def to_response(self, schema: DomainResultDTO) -> RequestResultProtocol:
        """Convert domain data to response representation."""
        match schema.exercise_status:
            case ExerciseStatusEnum.NEW_CASE:
                return self._new_case_adapter.to_response(schema)
            case ExerciseStatusEnum.EXPLAIN:
                return self._explain_adapter.to_response(schema)
            case _ as unexpected:
                raise ValueError(f'Unexpected exercise status: {unexpected}')
