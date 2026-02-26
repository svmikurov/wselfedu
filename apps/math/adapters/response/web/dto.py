"""Calculation exercise response DTOs."""

from __future__ import annotations

from django.forms import Form
from pydantic import BaseModel, ConfigDict, Field

from apps.core.domains.exercise.enums import ExerciseStatusEnum


class ConditionsFormDTO(BaseModel):
    """Exercise conditions web response DTO."""

    conditions_form: Form

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class ExerciseFormDTO(BaseModel):
    """Exercise case web response DTO."""

    question_text: str
    answer_input_form: Form

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class ExerciseWebDTO(BaseModel):
    """Exercise explanation web response DTO."""

    exercise_status: ExerciseStatusEnum
    data: BaseModel = Field(
        description='Exercise data',
    )

    context: dict[str, str] = Field(
        description='Additional exercise page context',
        default_factory=dict,
    )
    oob_html: str = Field(
        description='Out-Of-Band (OOB) HTML content for HTMX responses',
        default_factory=str,
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )
