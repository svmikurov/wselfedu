"""Response adapter strategy."""

import logging
from typing import Generic, TypeVar, override

from apps.core.adapters.response.protocol import AdapterProtocol
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.protocol import HasExerciseStatus

RequestContext = TypeVar('RequestContext')
DomainResult = TypeVar('DomainResult', bound=HasExerciseStatus)
Adapted = TypeVar('Adapted')

__all__ = ('ProcessExerciseAdapterStrategy',)

log = logging.getLogger(__name__)


class ProcessExerciseAdapterStrategy(
    AdapterProtocol[DomainResult, RequestContext, Adapted],
    Generic[DomainResult, RequestContext, Adapted],
):
    """Router for process exercise result adapter select."""

    def __init__(
        self,
        registry: dict[
            ExerciseStatusEnum,
            AdapterProtocol[DomainResult, RequestContext, Adapted],
        ],
    ) -> None:
        """Construct the strategy."""
        for key in registry.keys():
            if not isinstance(key, ExerciseStatusEnum):
                raise AttributeError(
                    f'Expected `ExerciseStatusEnum`, got: {type(key).__name__}'
                )
        self._registry = registry

    @override
    def to_response(
        self,
        domain_result: DomainResult,
        request_context: RequestContext,
    ) -> Adapted:
        """Convert to response."""
        try:
            adapter = self._registry[domain_result.status]
        except KeyError:
            log.error('Adapter strategy error')
            raise
        return adapter.to_response(domain_result, request_context)
