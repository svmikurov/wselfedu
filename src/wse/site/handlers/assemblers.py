"""Application layer assemblers."""

from typing import override

from wse.application.commands import CreateTestingTask

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


class CreateTestingTaskAssembler(
    AbstractAssembler[
        NullProto,
        HasSessionIdentifier,
        NullProto,
        HasSessionIdentifier,
    ],
):
    """Assembler for create testing exercise task command."""

    @override
    def prepare(
        self,
        params: NullProto,
        context: HasSessionIdentifier,
        validated: NullProto,
    ) -> HasSessionIdentifier:
        """Return null command."""
        return CreateTestingTask(
            session_id=context.session_id,
        )
