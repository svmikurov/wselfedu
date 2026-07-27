"""Use cases."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, TypeAlias

from wse.domain.protocols import ExerciseProtocol, HasSessionIdentifier

from .abstract import AbstractUseCase

CommandT: TypeAlias = HasSessionIdentifier
ResultT: TypeAlias = Any

if TYPE_CHECKING:
    from typing import Callable, Type

    from wse.domain.abstract import AbstractExerciseFactory
    from wse.domain.events import Event

    ExerciseT: TypeAlias = ExerciseProtocol[Any, Any, Any, Any, Any]
    FactoryT: TypeAlias = AbstractExerciseFactory[ExerciseT]
    ResultCollectorT: TypeAlias = Any
    HandlerResultT: TypeAlias = Any

    HandlersT: TypeAlias = dict[
        Type[Event],
        Callable[[Event], ResultCollectorT],
    ]

__all__ = ('ExerciseUseCase',)

log = logging.getLogger(__name__)


class ExerciseUseCase(
    AbstractUseCase[CommandT, ResultT],
):
    """Exercise use case."""

    def __init__(
        self,
        aggregate_factory: FactoryT,
        handler_registry: HandlersT,
        result_collector: ResultCollectorT,
    ):
        self._aggregate_factory = aggregate_factory
        self._handler_registry = handler_registry
        self._result_collector = result_collector
        self._events: list[Event] = []
        self._handler_results: list[HandlerResultT] = []

    def execute(self, cmd: CommandT) -> ResultT:
        """Execute exercise command."""
        aggregate = self._aggregate_factory.create(cmd.session_id)
        aggregate.handle(cmd)

        self._events.extend(aggregate.events)

        while aggregate.has_events():
            event = aggregate.pop_event()
            handler = self._handler_registry.get(type(event))

            if handler:
                try:
                    result = handler(event)
                    if result is not None:
                        self._handler_results.append(result)

                except Exception as e:
                    log.error(
                        f'Error in handler for {type(event).__name__}: {e}',
                        exc_info=True,
                    )

        return self._result_collector.collect(
            self._events,
            self._handler_results,
        )
