"""Exercise web response DTOs."""

from apps.core.domain.base_dto import BaseDTO
from pydantic import Field
from apps.core.domain.exercise.enums import CaseStatus


class CaseWebResponse(BaseDTO):
    """Exercise case web response adapter DTO."""

    exercise_status: CaseStatus = Field(
        description='Current exercise case status',
    )
    exercise_case: BaseDTO = Field(
        description='Current exercise case data',
    )
    context: dict[str, str] = Field(
        description='Additional exercise page context',
        default_factory=dict,
    )
