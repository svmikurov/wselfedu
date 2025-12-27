"""Api presentation response adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import types
    from ..schemas import dto

    type DomainResult = dto.PresentationCase
    type ResponseData = types.TranslationAPI


class ApiPresentationAdapter:
    """Api presentation response adapter."""

    @classmethod
    def to_response(cls, presentation_case: DomainResult) -> ResponseData:
        """Convert presentation case to api payload."""
        return {
            'case_uuid': presentation_case.case_uuid,
            'question': presentation_case.question,
            'answer': presentation_case.answer,
            'progress': presentation_case.progress,
        }
