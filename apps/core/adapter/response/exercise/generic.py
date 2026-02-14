"""Generic response adapters."""

from typing import Generic, TypeVar

from apps.core.domain.exercise.enums import ExerciseStatusEnum
from apps.core.domain.exercise.types import ExerciseStatus

from ..abc import AbstractResponseAdapter

DomainType = TypeVar('DomainType', bound=ExerciseStatus)
NewCaseResponse = TypeVar('NewCaseResponse')
ExplainResponse = TypeVar('ExplainResponse')
ResponseType = TypeVar('ResponseType')


# HACK: Fix type ignore
class ResultStrategyAdapter(
    AbstractResponseAdapter[DomainType, ResponseType],
    Generic[DomainType, ResponseType, NewCaseResponse, ExplainResponse],
):
    """Router for new case or explain current case adapter select."""

    def __init__(
        self,
        new_case_adapter: AbstractResponseAdapter[DomainType, NewCaseResponse],
        explain_adapter: AbstractResponseAdapter[DomainType, ExplainResponse],
    ) -> None:
        """Construct the adapter."""
        self._new_case_adapter = new_case_adapter
        self._explain_adapter = explain_adapter

    def to_response(self, schema: DomainType) -> ResponseType:
        """Convert domain data to response representation."""
        match schema.exercise_status:
            case ExerciseStatusEnum.NEW_CASE:
                return self._new_case_adapter.to_response(schema)  # type: ignore[return-value]
            case ExerciseStatusEnum.EXPLAIN:
                return self._explain_adapter.to_response(schema)  # type: ignore[return-value]
            case _:
                raise RuntimeError('Unexpected case status')
