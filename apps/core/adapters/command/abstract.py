"""Abstract base class for assembler's command adapter interface."""

from abc import ABC, abstractmethod
from typing import TypeVar, TypeVarTuple, Unpack, override

from .protocol import CompositeAdapterProtocol

CommandT = TypeVar('CommandT')
ArgsT = TypeVarTuple('ArgsT')
AdaptedT = TypeVar('AdaptedT')


class AbstractCompositeAdapter(
    ABC,
    CompositeAdapterProtocol[
        CommandT,
        Unpack[ArgsT],
        AdaptedT,
    ],
):
    """ABC for assembler's command adapter interface."""

    @override
    @abstractmethod
    def adapt(
        self,
        command: CommandT,
        *args: Unpack[ArgsT],
    ) -> AdaptedT:
        """Adapt command with composite parameters."""
