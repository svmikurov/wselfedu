"""Response adapter strategy."""

import logging
from typing import Generic, TypeVar, override

from apps.core.adapters.response.protocol import AdapterProtocol
from contracts.entity.domain.exercise.fields import HasExerciseStatus
from contracts.enums.exercise import ExerciseStatus
from utils.audit.impl import NullAuditor
from utils.audit.protocol import AuditorProtocol

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
        auditor: AuditorProtocol | None = None,
        name: str | None = None,
    ) -> None:
        """Construct the strategy."""
        for key in registry.keys():
            if not isinstance(key, ExerciseStatus):
                raise AttributeError(
                    f'Expected `ExerciseStatusEnum`, got: {type(key).__name__}'
                )
        self._registry = registry
        self._auditor = auditor or NullAuditor()
        self._name = name or 'undefined'

    @override
    def to_response(
        self,
        domain_result: DomainResult,
        request_context: RequestContext,
    ) -> Adapted:
        """Convert to response."""
        try:
            adapter = self._registry[domain_result.status]
            self._auditor.record('adapter_strategy.select', obj=adapter)
        except KeyError:
            log.error('Adapter strategy error')
            raise

        adapted = adapter.to_response(domain_result, request_context)
        return adapted

    @property
    def name(self) -> str:
        """Return adapter name."""
        return self._name
