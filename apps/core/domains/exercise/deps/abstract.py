"""Abstract base classes for exercise domain dependencies."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from interfaces.protocols.domain.exercise import CandidatesProtocol

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
        candidates: CandidatesProtocol,
        conf: Conf,
    ) -> CandidatesProtocol:
        """Select data for exercise."""
