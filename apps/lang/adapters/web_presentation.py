"""Web presentation response adapter."""

from __future__ import annotations

from typing import TYPE_CHECKING

from django.urls import reverse_lazy

from .. import schemas

if TYPE_CHECKING:
    from .. import types
    from ..schemas import dto

    type DomainResult = dto.PresentationCase
    type ResponseData = types.TranslationWEB

UPDATE_PROGRESS_URL = reverse_lazy('lang_api:study-progress')


class WebPresentationAdapter:
    """Web presentation response adapter.

    Converts presentation case domain data to web-ready format.
    """

    @classmethod
    def to_response(cls, presentation_case: DomainResult) -> ResponseData:
        """Convert presentation case to web context."""
        increment_progress = schemas.UpdateProgress(
            case_uuid=str(presentation_case.case_uuid),
            is_known=True,
        )
        decrement_progress = schemas.UpdateProgress(
            case_uuid=str(presentation_case.case_uuid),
            is_known=False,
        )
        return {
            'case_uuid': str(presentation_case.case_uuid),
            'question': presentation_case.question,
            'answer': presentation_case.answer,
            'progress': {
                'current': presentation_case.progress,
                'update_url': str(UPDATE_PROGRESS_URL),
                'increment_payload': increment_progress.model_dump_json(),
                'decrement_payload': decrement_progress.model_dump_json(),
            },
        }
