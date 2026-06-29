"""Application layer assemblers."""

from .abstract import AbstractAssembler
from .dtos import NullDTO
from .protocols import NullProto


class NullAssembler(
    AbstractAssembler[NullProto, NullProto, NullProto, NullProto],
):
    """Null validator."""

    def prepare(
        self, params: NullProto, context: NullProto, data: NullProto
    ) -> NullProto:
        """Return null command."""
        return NullDTO()
