"""Shared response DTOs."""

import uuid

from pydantic import Field

from ...domains.base_dto import BaseDTO


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
