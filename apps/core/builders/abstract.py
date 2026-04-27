"""Abstract base class for DTO builder."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from .protocol import DtoBuilderProtocol

ConfT = TypeVar('ConfT')
CandidateT = TypeVar('CandidateT')
CaseT = TypeVar('CaseT')

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')


class AbstractCaseFactory(
    ABC,
    DtoBuilderProtocol[CandidateT, CaseT],
):
    """ABC for exercise case DTO builder."""

    @override
    @abstractmethod
    def build(
        self,
        data: CandidateT,
    ) -> CaseT:
        """Build exercise case DTO."""


# DEPRECATED: Is deprecated?
class AbstractLockupConditionsFactory(
    ABC, Generic[LockupCommand, LockupConditions]
):
    """ABC for Database lockup conditions factory."""

    @abstractmethod
    def build(self, command: LockupCommand) -> LockupConditions:
        """Build lockup conditions."""
