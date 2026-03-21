"""Presentation exercise response adapters.

This module contains adapters for converting Presentation
exercise cases to different output formats (API and Web).
"""

from django.urls import reverse_lazy

from apps.core.adapters.response.abc import AbstractSimpleResponseAdapter
from apps.core.adapters.response.exercise.presentation import (
    PresentationApi,
    PresentationWeb,
    Progress,
    UpdateProgress,
)
from apps.core.domains.exercise.schema.presentation_dto import PresentationData


class ApiPresentationAdapter(
    AbstractSimpleResponseAdapter[PresentationData, PresentationApi]
):
    """API adapter for Presentation exercise type.

    Converts PresentationCase domain DTO to API response format (JSON).
    Used by mobile apps, SPAs, and third-party integrations.
    """

    def to_response(self, data: PresentationData) -> PresentationApi:
        """Convert Presentation case to API payload."""
        return PresentationApi(
            case_uuid=data.case_uuid,
            question_text=data.question_text,
            answer_text=data.answer_text,
            progress=data.progress,
        )


class WebPresentationAdapter(
    AbstractSimpleResponseAdapter[PresentationData, PresentationWeb]
):
    """WEB adapter for Presentation exercise type.

    Converts PresentationCase domain model to Web response format.
    Includes additional context needed for server-rendered templates.
    """

    PROGRESS_UPDATE_URL = 'lang_api:study-progress'

    def to_response(self, data: PresentationData) -> PresentationWeb:
        """Convert Presentation case to web context."""
        increment_payload = UpdateProgress(
            case_uuid=data.case_uuid, is_known=True
        )
        decrement_payload = UpdateProgress(
            case_uuid=data.case_uuid, is_known=False
        )
        return PresentationWeb(
            case_uuid=data.case_uuid,
            question_text=data.question_text,
            answer_text=data.answer_text,
            progress=Progress(
                current_value=data.progress,
                update_endpoint=str(reverse_lazy(self.PROGRESS_UPDATE_URL)),
                increment_payload=increment_payload,
                decrement_payload=decrement_payload,
            ),
        )
