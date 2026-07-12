"""Application layer assemblers."""

from typing import override

from wse.application.commands import TaskPerform

from ..dto import NullDTO
from ..interfaces.protocols import HasSessionIdentifier, NullProto
from .abstract import AbstractAssembler


class NullAssembler(
    AbstractAssembler[NullProto, NullProto, NullProto, NullProto],
):
    """Null assembler."""

    @override
    def prepare(
        self, params: NullProto, context: NullProto, data: NullProto
    ) -> NullProto:
        """Return null command."""
        return NullDTO()


class TaskAssembler(
    AbstractAssembler[
        NullProto,
        HasSessionIdentifier,
        NullProto,
        HasSessionIdentifier,
    ],
):
    """Builds a command to perform an exercise task."""

    @override
    def prepare(
        self,
        params: NullProto,
        context: HasSessionIdentifier,
        validated: NullProto,
    ) -> HasSessionIdentifier:
        """Build a command to perform the exercise task."""
        return TaskPerform(
            session_id=context.session_id,
        )
