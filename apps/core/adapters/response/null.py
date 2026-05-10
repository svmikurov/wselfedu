"""Null adapter."""

from typing import override

from ports.abstract.adapter import AbstractResponseAdapter


class NullResponseAdapter(AbstractResponseAdapter[object, object, object]):
    """Null response adapters."""

    @override
    def to_response(
        self,
        use_case_result: object,
        request_context: object,
    ) -> object:
        """Return use case execute result."""
        return use_case_result
