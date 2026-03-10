"""Exercise web response DTOs."""

from typing import Any

from pydantic import BaseModel, Field

from apps.core.domains.base_dto import BaseDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum


class WebExerciseCaseDTO(BaseDTO):
    """Exercise case web response adapter DTO."""

    exercise_status: ExerciseStatusEnum = Field(
        description='Current exercise case status',
    )
    data: BaseModel = Field(
        description='Current exercise case data',
    )
    context: dict[str, Any] = Field(
        description='Additional exercise page context',
        default_factory=dict,
    )


class WebExerciseResponseDTO(WebExerciseCaseDTO):
    """Exercise case web response DTO with additional content."""

    oob_html: str = Field(
        description='Out Of Band',
        default_factory=str,
    )
