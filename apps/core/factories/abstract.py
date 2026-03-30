"""Abstract base class for factories."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

CaseDTO = TypeVar('CaseDTO')
ParametersDTO = TypeVar('ParametersDTO')
ResultDTO = TypeVar('ResultDTO')

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')


class AbstractExerciseDTOFactory(
    ABC,
    Generic[CaseDTO, ParametersDTO, ResultDTO],
):
    """ABC for exercise DTO factory."""

    @abstractmethod
    def build(self, case: CaseDTO, parameters: ParametersDTO) -> ResultDTO:
        """Create exercise DTO."""


class AbstractLockupConditionsFactory(
    ABC, Generic[LockupCommand, LockupConditions]
):
    """ABC for Database lockup conditions factory."""

    @abstractmethod
    def build(self, command: LockupCommand) -> LockupConditions:
        """Build lockup conditions."""
