"""Generic response adapters."""

from typing import Generic, TypeVar

from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.types import ExerciseStatus
from apps.core.handlers.protocol import (
    ContextResponseAdapterProtocol,
    RequestContextProtocol,
    RequestResultProtocol,
    ResponseAdapterProtocol,
)

DomainResultDTO = TypeVar('DomainResultDTO', bound=ExerciseStatus)


# FIXME: Fix type hint
# New case and explain adapters have different schema types
class ResultStrategyAdapter(
    ResponseAdapterProtocol[DomainResultDTO],
    Generic[DomainResultDTO],
):
    """Router for new case or explain current case adapter select."""

    def __init__(
        self,
        new_case_adapter: ResponseAdapterProtocol[DomainResultDTO],
        explain_adapter: ResponseAdapterProtocol[DomainResultDTO],
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
    ContextResponseAdapterProtocol[DomainResultDTO],
    Generic[DomainResultDTO],
):
    """Router for new case or explain current case with context.

    Adds balance update on template via OOB.
    """

    def __init__(
        self,
        new_case_adapter: ContextResponseAdapterProtocol[DomainResultDTO],
        explain_adapter: ResponseAdapterProtocol[DomainResultDTO],
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
