"""Shared response DTOs."""

import uuid
from typing import Any

from pydantic import Field

from apps.core.domains.base_dto import BaseDTO


class WebResponseDTO(BaseDTO):
    """Web response adapter DTO."""

    context: dict[str, Any] = Field(
        description='Response context',
        default_factory=dict,
    )


class UpdateProgress(BaseDTO):
    """Progress update payload."""

    case_uuid: uuid.UUID
    is_known: bool


class Progress(BaseDTO):
    """Progress data for response."""

    current_value: int
    update_endpoint: str = Field(
        description='API endpoint for progress updates'
    )
    increment_payload: UpdateProgress
    decrement_payload: UpdateProgress
