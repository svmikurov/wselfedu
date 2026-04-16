"""Abstract base classes for resolver."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import ResolverProtocol

__all__ = ('AbstractResolver',)

CommandT = TypeVar('CommandT')
ResultT = TypeVar('ResultT')


class AbstractResolver(
    ABC,
    ResolverProtocol[CommandT, ResultT],
):
    """ABC for resolver."""

    @override
    @abstractmethod
    def resolve(self, command: CommandT) -> ResultT:
        """Resolve."""
