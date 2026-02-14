"""Exercise web response DTOs."""

from pydantic import BaseModel, Field

from apps.core.domain.base_dto import BaseDTO
from apps.core.domain.exercise.enums import ExerciseStatusEnum


class WebCase(BaseDTO):
    """Exercise case web response adapter DTO."""

    exercise_status: ExerciseStatusEnum = Field(
        description='Current exercise case status',
    )
    data: BaseModel = Field(
        description='Current exercise case data',
    )
    context: dict[str, str] = Field(
        description='Additional exercise page context',
        default_factory=dict,
    )
