"""Abstract base classes for exercise domain dependencies."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from contracts.aliases import CandidatesAlias

from .protocol import SelectorProtocol

Conf = TypeVar('Conf')


class AbstractSelector(
    ABC,
    SelectorProtocol[Conf],
    Generic[Conf],
):
    """ABC for candidates selector by configuration."""

    @override
    @abstractmethod
    def select(
        self,
        candidates: CandidatesAlias,
        conf: Conf,
    ) -> CandidatesAlias:
        """Select data for exercise."""
