"""Use case result bulders."""

from dataclasses import dataclass
from typing import Any

from wse.domain.events import Event, TaskCreated
from wse.domain.protocols import TaskProtocol

from .abstract import AbstractResultCollector

# TODO: Relocate handler result definition


class HandlerResult:
    """Event handling result."""


@dataclass(frozen=True, slots=True)
class ExerciseResult(HandlerResult):
    """Exercise use case command handling result."""

    task: TaskProtocol


# IDEA: Experimental result collector
class ExerciseResultCollector(
    AbstractResultCollector[HandlerResult, Any],
):
    """Exercise event results collector."""

    def collect(
        self,
        events: list[Event],
        handler_results: list[HandlerResult],
    ) -> Any:
        """Collect exercise use case result."""
        for event in events:
            if isinstance(event, TaskCreated):
                return ExerciseResult(
                    task=event.task,
                )
            else:
                raise NotImplementedError(
                    f'Not implemented {type(event).__name__} '
                    'event collection yet'
                )
