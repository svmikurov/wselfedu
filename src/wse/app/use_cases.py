"""Use cases."""

import logging
from typing import TYPE_CHECKING

from .abstract import AbstractUseCase

if TYPE_CHECKING:
    from typing import Any, Callable, Type, TypeAlias

    from wse.domain.abstract import AbstractExerciseFactory
    from wse.domain.events import Event
    from wse.domain.protocols import (
        EventSourcedAggregate,
        HasSessionIdentifier,
    )

    CommandT: TypeAlias = HasSessionIdentifier
    ResultT: TypeAlias = Any

    AggregateT: TypeAlias = EventSourcedAggregate[CommandT, ResultT]
    FactoryT: TypeAlias = AbstractExerciseFactory[AggregateT]

    HandlersT: TypeAlias = dict[
        Type[Event],
        Callable[[AggregateT, Event], None],
    ]

__all__ = ('ExerciseUseCase',)

log = logging.getLogger(__name__)


class ExerciseUseCase(AbstractUseCase[CommandT, ResultT]):
    """Exercise use case."""

    def __init__(
        self,
        aggregate_factory: FactoryT,
        handlers: HandlersT,
    ) -> None:
        self._aggregate_factory = aggregate_factory
        self._handlers = handlers

    def execute(self, cmd: CommandT) -> ResultT:
        """Execute exercise command and handle domain events."""
        aggregate = self._aggregate_factory.create(cmd.session_id)
        result = aggregate.handle(cmd)

        while aggregate.has_events():
            event = aggregate.pop_event()
            handler = self._handlers.get(type(event))

            if handler:
                try:
                    handler(aggregate, event)
                except Exception as e:
                    log.error(
                        f'Error in handler for {type(event).__name__}: {e}',
                        exc_info=True,
                    )

        return result
