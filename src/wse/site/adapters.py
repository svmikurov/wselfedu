"""Application layer request handler result adapter."""

from .abstract import AbstractAdapter
from .protocols import NullProto


class NullAdapter(
    AbstractAdapter[NullProto, NullProto, NullProto],
):
    """Null validator."""

    def to_response(self, source: NullProto, context: NullProto) -> NullProto:
        """Return original data."""
        return source
