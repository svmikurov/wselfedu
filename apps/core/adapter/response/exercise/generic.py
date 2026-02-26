"""Generic response adapters."""

from typing import Generic, TypeVar

from apps.core.domain.exercise.enums import ExerciseStatusEnum
from apps.core.domain.exercise.types import ExerciseStatus
from apps.core.handlers.protocol import (
    ContextResponseAdapter,
    RequestContextProtocol,
    RequestResultProtocol,
    ResponseAdapter,
)

DomainResultDTO = TypeVar('DomainResultDTO', bound=ExerciseStatus)


class ResultStrategyAdapter(
    ResponseAdapter[DomainResultDTO],
    Generic[DomainResultDTO],
):
    """Router for new case or explain current case adapter select."""

    def __init__(
        self,
        new_case_adapter: ResponseAdapter[DomainResultDTO],
        explain_adapter: ResponseAdapter[DomainResultDTO],
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


class ResultContextStrategyAdapter(
    ContextResponseAdapter[DomainResultDTO],
    Generic[DomainResultDTO],
):
    """Router for new case or explain current case with context.

    Adds balance update on template via OOB.
    """

    def __init__(
        self,
        new_case_adapter: ContextResponseAdapter[DomainResultDTO],
        explain_adapter: ResponseAdapter[DomainResultDTO],
    ) -> None:
        """Construct the adapter."""
        self._new_case_adapter = new_case_adapter
        self._explain_adapter = explain_adapter

    def to_response(
        self,
        schema: DomainResultDTO,
        request_context: RequestContextProtocol,
    ) -> RequestResultProtocol:
        """Convert domain data to response representation."""
        match schema.exercise_status:
            case ExerciseStatusEnum.NEW_CASE:
                return self._new_case_adapter.to_response(
                    schema, request_context
                )
            case ExerciseStatusEnum.EXPLAIN:
                return self._explain_adapter.to_response(schema)
            case _ as unexpected:
                raise ValueError(f'Unexpected exercise status: {unexpected}')
