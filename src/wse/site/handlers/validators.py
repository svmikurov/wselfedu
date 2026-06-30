"""Application layer validators."""

from ..interfaces.protocols import NullProto
from .abstract import AbstractValidator


class NullValidator(AbstractValidator[NullProto, NullProto]):
    """Null validator."""

    def validate(self, data: NullProto) -> NullProto:
        """Return input data without validation."""
        return data
