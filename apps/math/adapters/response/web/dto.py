"""Calculation exercise response DTOs."""

from __future__ import annotations

from django.forms import Form
from pydantic import BaseModel, ConfigDict

from apps.core.domain.exercise.enums import ExerciseStatusEnum


class CalculationWebConditions(BaseModel):
    """Calculation exercise conditions web response DTO."""

    conditions_form: Form

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class CalculationWebCase(BaseModel):
    """Calculation exercise case web response DTO."""

    question_text: str
    answer_input_form: Form

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class CalculationWebExplain(BaseModel):
    """Calculation exercise explanation web response DTO."""

    exercise_status: ExerciseStatusEnum
    data: BaseModel

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )
