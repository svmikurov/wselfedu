"""Null adapter."""

from typing import override

from .abstract import AbstractResponseAdapter


class NullResponseAdapter(AbstractResponseAdapter[object, object, object]):
    """Null response adapters."""

    @override
    def to_response(
        self,
        context: object,
        extra_context: object,
    ) -> object:
        """Return use case execute result."""
        return context
