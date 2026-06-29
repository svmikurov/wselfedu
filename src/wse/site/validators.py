"""Application layer validators."""

from .abstract import AbstractValidator
from .protocols import NullProto


class NullValidator(AbstractValidator[NullProto, NullProto]):
    """Null validator."""

    def validate(self, data: NullProto) -> NullProto:
        """Return input data without validation."""
        return data
