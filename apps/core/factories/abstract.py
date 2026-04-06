"""Abstract base class for factories."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from .protocol import CaseFactoryProtocol

CaseT = TypeVar('CaseT')
ConfT = TypeVar('ConfT')
TaskT = TypeVar('TaskT')

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')


class AbstractCaseFactory(
    ABC,
    CaseFactoryProtocol[ConfT, CaseT, TaskT],
):
    """ABC for exercise case DTO factory."""

    @override
    @abstractmethod
    def build(self, conf: ConfT, case: CaseT) -> TaskT:
        """Build exercise DTO."""


class AbstractLockupConditionsFactory(
    ABC, Generic[LockupCommand, LockupConditions]
):
    """ABC for Database lockup conditions factory."""

    @abstractmethod
    def build(self, command: LockupCommand) -> LockupConditions:
        """Build lockup conditions."""
