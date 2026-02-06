"""Presentation exercise response DTOs."""

from __future__ import annotations

import uuid

from pydantic import Field

from apps.core.domain.base_dto import BaseDTO

# -------------------------------
# API Response DTO (external API)
# -------------------------------


class PresentationApi(BaseDTO):
    """API response DTO for presentation exercises."""

    case_uuid: uuid.UUID
    question_text: str
    answer_text: str
    progress: int


# -------------------------------
# Web View DTO (template context)
# -------------------------------


class PresentationWeb(BaseDTO):
    """WEB response DTO for presentation exercises."""

    case_uuid: uuid.UUID
    question_text: str
    answer_text: str
    progress: Progress


# Nested models
# -------------


class Progress(BaseDTO):
    """Progress data for response."""

    current_value: int
    update_endpoint: str = Field(
        description='API endpoint for progress updates'
    )
    increment_payload: UpdateProgress
    decrement_payload: UpdateProgress


class UpdateProgress(BaseDTO):
    """Progress update payload."""

    case_uuid: uuid.UUID
    is_known: bool
