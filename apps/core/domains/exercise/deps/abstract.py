"""Abstract base classes for exercise domain dependencies."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from contracts.infra.domain.selector import SelectorProtocol
from interfaces.protocols.domain.exercise import CandidatesT

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
        candidates: CandidatesT,
        conf: Conf,
    ) -> CandidatesT:
        """Select data for exercise."""
