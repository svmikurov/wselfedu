"""Abstract base class for DTO builder."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from ports.contract.infra.builder import (
    DtoBuilderProtocol,
    SpecDtoBuilderProtocol,
)

CaseT = TypeVar('CaseT')
SpecT = TypeVar('SpecT')
DtoT = TypeVar('DtoT')

LockupCommand = TypeVar('LockupCommand')
LockupConditions = TypeVar('LockupConditions')


class AbstractCaseFactory(
    ABC,
    DtoBuilderProtocol[CaseT, DtoT],
):
    """ABC for exercise case DTO builder."""

    @override
    @abstractmethod
    def build(
        self,
        case: CaseT,
    ) -> DtoT:
        """Build exercise case DTO."""


class AbstractSpecDtoBuilder(
    SpecDtoBuilderProtocol[CaseT, SpecT, DtoT],
):
    """ABC for a DTO builder that follows the specification."""

    @override
    @abstractmethod
    def build(
        self,
        case: CaseT,
        spec: SpecT,
    ) -> DtoT:
        """Build a DTO according to the specification."""


# QUESTION: Is deprecated?
class AbstractLockupConditionsFactory(
    ABC,
    Generic[LockupCommand, LockupConditions],
):
    """ABC for Database lockup conditions factory."""

    @abstractmethod
    def build(
        self,
        command: LockupCommand,
    ) -> LockupConditions:
        """Build lockup conditions."""
