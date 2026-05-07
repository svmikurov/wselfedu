"""Abstract base class for DTO formatter."""

from abc import ABC, abstractmethod
from typing import TypeVar, override

from .protocol import ConfFormatterProtocol

DataT = TypeVar('DataT')
SpecT = TypeVar('SpecT')
DtoT = TypeVar('DtoT')


class AbstractConfFormatter(
    ABC,
    ConfFormatterProtocol[DataT, SpecT, DtoT],
):
    """ABC for a DTO formatter that follows the configuration."""

    @override
    @abstractmethod
    def format(self, data: DataT, conf: SpecT) -> DtoT:
        """Build a DTO according to the configuration."""
