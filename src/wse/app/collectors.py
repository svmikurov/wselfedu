"""Use case result builders."""

from dataclasses import dataclass
from typing import Any, Callable, TypeAlias

from wse.domain.events import Event, TaskCreated
from wse.domain.protocols import TaskProtocol

from .abstract import AbstractResultCollector

# FIX: Any type hint
HandlerRegistryT: TypeAlias = dict[Any, Callable[[Any], Any]]


# TODO: Relocate handler result definition
class HandlerResult:
    """Event handling result."""


# TODO: Relocate handler result definition
@dataclass(frozen=True, slots=True)
class ExerciseResult(HandlerResult):
    """Exercise use case command handling result."""

    task: TaskProtocol


def build_task_created_result(event: TaskCreated) -> ExerciseResult:
    """Handle task task created event."""
    return ExerciseResult(
        task=event.task,
    )


RESULT_REGISTRY: HandlerRegistryT = {
    TaskCreated: build_task_created_result,
}


# IDEA: Experimental result collector
class ExerciseResultCollector(
    AbstractResultCollector[HandlerResult, Any],
):
    """Exercise event results collector."""

    def __init__(
        self,
        handler_registry: HandlerRegistryT | None = None,
    ) -> None:
        self._handler_registry = handler_registry or RESULT_REGISTRY

    def collect(
        self,
        events: list[Event],
        handler_results: list[HandlerResult],
    ) -> Any:
        """Collect exercise use case result."""
        # TODO: Add custom exceptions `EventCollectionError`

        for event in events:
            try:
                handler = self._handler_registry[type(event)]
            except KeyError as e:
                raise NotImplementedError(
                    f'Not implemented {type(event).__name__} '
                    'event collection yet'
                ) from e

            return handler(event)
