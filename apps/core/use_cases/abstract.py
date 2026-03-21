"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from apps.core.handlers.protocol import UseCaseProtocol

__all__ = ('AbstractUseCase',)

CommandData = TypeVar('CommandData')
ResultData = TypeVar('ResultData')


class AbstractUseCase(ABC, UseCaseProtocol[CommandData, ResultData]):
    """ABC for generic request use case."""

    @override
    @abstractmethod
    def execute(self, command: CommandData) -> ResultData:
        """Execute use case."""
