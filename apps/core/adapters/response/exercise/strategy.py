"""Response adapter strategy."""

import logging
from typing import Generic, TypeVar, override

from apps.core.adapters.response.protocol import AdapterProtocol
from contracts.entity.domain.exercise.fields import HasExerciseStatus
from contracts.enums.exercise import ExerciseStatus

RequestContext = TypeVar('RequestContext')
DomainResult = TypeVar('DomainResult', bound=HasExerciseStatus)
Adapted = TypeVar('Adapted')

__all__ = ('ProcessExerciseAdapterStrategy',)

log = logging.getLogger('audit')


class ProcessExerciseAdapterStrategy(
    AdapterProtocol[DomainResult, RequestContext, Adapted],
    Generic[DomainResult, RequestContext, Adapted],
):
    """Router for process exercise result adapter select."""

    def __init__(
        self,
        registry: dict[
            ExerciseStatus,
            AdapterProtocol[DomainResult, RequestContext, Adapted],
        ],
    ) -> None:
        """Construct the strategy."""
        for key in registry.keys():
            if not isinstance(key, ExerciseStatus):
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

        adapted = adapter.to_response(domain_result, request_context)
        log.debug(
            f'Applied {type(adapter).__module__}.{type(adapter).__name__}'
        )
        return adapted
