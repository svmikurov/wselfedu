"""Response adapter strategy."""

from typing import Generic, TypeVar

from apps.core.adapters.response.status import StatusEnum
from apps.core.domains.exercise.protocol import HasExerciseStatus
from apps.core.handlers.protocol import AdapterProtocol

DomainResult = TypeVar('DomainResult', bound=HasExerciseStatus)
RequestContext = TypeVar('RequestContext')
Adapted = TypeVar('Adapted')

__all__ = ('ExerciseAdapterStrategy',)


class ExerciseAdapterStrategy(
    AdapterProtocol[DomainResult, RequestContext, Adapted],
    Generic[DomainResult, RequestContext, Adapted],
):
    """Router for new case or explain current case adapter select."""

    def __init__(
        self,
        new_case_adapter: AdapterProtocol[
            DomainResult,
            RequestContext,
            Adapted,
        ],
        explain_adapter: AdapterProtocol[
            DomainResult,
            RequestContext,
            Adapted,
        ],
    ) -> None:
        """Construct the adapter."""
        self._new_case_adapter = new_case_adapter
        self._explain_adapter = explain_adapter

    def to_response(
        self,
        schema: DomainResult,
        request_context: RequestContext,
    ) -> Adapted:
        """Convert domain data to response representation."""
        match schema.exercise_status:
            case StatusEnum.NEW_CASE:
                return self._new_case_adapter.to_response(
                    schema,
                    request_context,
                )
            case StatusEnum.EXPLAIN:
                return self._explain_adapter.to_response(
                    schema,
                    request_context,
                )
            case _ as unexpected:
                raise ValueError(f'Unexpected exercise status: {unexpected}')
