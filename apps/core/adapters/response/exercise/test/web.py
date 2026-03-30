"""Test exercise response adapters."""

from apps.core.adapters.response.abstract import AbstractResponseAdapter
from apps.core.adapters.response.dto import ResponseDTO
from apps.core.domains.exercise.dto import TextExerciseCheckResult
from apps.core.domains.protocol import NullProtocol


class WebTestAdapter(
    AbstractResponseAdapter[
        TextExerciseCheckResult,
        ResponseDTO,
        NullProtocol,
    ]
):
    """Web test exercise response adapter.

    Returns response DTO.
    """

    def to_response(
        self,
        schema: TextExerciseCheckResult,
        request_context: NullProtocol,
    ) -> ResponseDTO:
        """Convert domain result to web representation context."""
        return ResponseDTO(
            status=schema.status,
            context=schema,
        )
