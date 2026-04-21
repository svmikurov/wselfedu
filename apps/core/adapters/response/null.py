"""Null adapter."""

from typing import override

from .abstract import AbstractResponseAdapter


class NullResponseAdapter(AbstractResponseAdapter[object, object, object]):
    """Null response adapters."""

    @override
    def to_response(
        self,
        domain_result: object,
        request_context: object,
    ) -> object:
        """Return use case execute result."""
        return domain_result
