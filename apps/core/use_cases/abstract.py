"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import ResolverProtocol, UseCaseProtocol

__all__ = ('AbstractUseCase',)

UseCase = TypeVar('UseCase')
Command = TypeVar('Command')
Result = TypeVar('Result')


class AbstractUseCase(
    ABC,
    UseCaseProtocol[Command, Result],
):
    """ABC for generic request use case."""

    @override
    @abstractmethod
    def execute(self, command: Command) -> Result:
        """Execute use case."""


class AbstractResolver(
    ABC,
    ResolverProtocol[Command, Result],
):
    """ABC for resolver."""

    @override
    @abstractmethod
    def resolve(self, command: Command) -> Result:
        """Resolve."""
