"""Abstract base class for assembler's command adapter interface."""

from abc import ABC, abstractmethod
from typing import TypeVar, TypeVarTuple, Unpack, override

from .protocol import CompositeAdapterProtocol

Command = TypeVar('Command')
CompositeParams = TypeVarTuple('CompositeParams')
Adapted = TypeVar('Adapted')


class AbstractCompositeAdapter(
    ABC,
    CompositeAdapterProtocol[
        Command,
        Unpack[CompositeParams],
        Adapted,
    ],
):
    """ABC for assembler's command adapter interface."""

    @override
    @abstractmethod
    def adapt(
        self,
        command: Command,
        *params: Unpack[CompositeParams],
    ) -> Adapted:
        """Adapt command with composite parameters."""
