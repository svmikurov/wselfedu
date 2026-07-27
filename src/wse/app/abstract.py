"""Abstract base classes for application layer."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from wse.domain.events import Event

CommandT = TypeVar('CommandT')
UseCaseResultT = TypeVar('UseCaseResultT')

# HACK: Update handler result type after result definition refactor
HandlerResultT = TypeVar('HandlerResultT')


class AbstractUseCase(
    ABC,
    Generic[CommandT, UseCaseResultT],
):
    """ABC for use case."""

    @abstractmethod
    def execute(self, cmd: CommandT) -> UseCaseResultT:
        """Execute command."""


class AbstractResultCollector(
    ABC,
    Generic[HandlerResultT, UseCaseResultT],
):
    """ABC for use case result collector."""

    @abstractmethod
    def collect(
        self,
        events: list[Event],
        handler_results: list[HandlerResultT],
    ) -> UseCaseResultT:
        """Collect result with domain events and application results."""
