"""Abstract base classes for use cases."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from utils.audit.mixins import BaseAuditable

from .protocol import UseCaseProtocol

__all__ = ('AbstractUseCase',)

CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')


class AbstractUseCase(
    BaseAuditable,
    ABC,
    UseCaseProtocol[CommandT, ResultT],
):
    """ABC for request use case."""

    @override
    @abstractmethod
    def execute(self, command: CommandT) -> ResultT:
        """Execute use case."""
