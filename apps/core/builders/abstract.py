"""Abstract base class for DTO builder."""

from abc import ABC, abstractmethod
from typing import Generic, override

from . import aliases
from .protocol import DtoBuilderProtocol


class AbstractCaseFactory(
    ABC,
    DtoBuilderProtocol[aliases.DTO_contra, aliases.DTO_co],
):
    """ABC for exercise case DTO builder."""

    @override
    @abstractmethod
    def build(
        self,
        data: aliases.DTO_contra,
    ) -> aliases.DTO_co:
        """Build exercise case DTO."""


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
