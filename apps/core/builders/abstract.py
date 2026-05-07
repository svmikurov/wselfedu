"""Abstract base class for DTO builder."""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, override

from . import aliases
from .protocol import (
    ConfDtoBuilderProtocol,
    DtoBuilderProtocol,
    SpecDtoBuilderProtocol,
)

DataT = TypeVar('DataT')
SpecT = TypeVar('SpecT')
DtoT = TypeVar('DtoT')


class AbstractCaseFactory(
    ABC,
    DtoBuilderProtocol[DataT, DtoT],
):
    """ABC for exercise case DTO builder."""

    @override
    @abstractmethod
    def build(
        self,
        data: DataT,
    ) -> DtoT:
        """Build exercise case DTO."""


class AbstractSpecDtoBuilder(
    SpecDtoBuilderProtocol[DataT, SpecT, DtoT],
):
    """ABC for a DTO builder that follows the specification."""

    @override
    @abstractmethod
    def build(
        self,
        data: DataT,
        spec: SpecT,
    ) -> DtoT:
        """Build a DTO according to the specification."""


class AbstractConfDtoBuilderProtocol(
    ConfDtoBuilderProtocol[DataT, SpecT, DtoT],
):
    """ABC for a DTO builder that follows the configuration."""

    @override
    @abstractmethod
    def build(
        self,
        data: DataT,
        conf: SpecT,
    ) -> DtoT:
        """Build a DTO according to the configuration."""


# DEPRECATED: Is deprecated?
class AbstractLockupConditionsFactory(
    ABC,
    Generic[aliases.LockupCommand, aliases.LockupConditions],
):
    """ABC for Database lockup conditions factory."""

    @abstractmethod
    def build(
        self,
        command: aliases.LockupCommand,
    ) -> aliases.LockupConditions:
        """Build lockup conditions."""
