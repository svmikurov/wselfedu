"""Calculation exercise response DTOs."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from apps.math.forms import CalculationConditionsForm
from apps.math.schemas.exercise import CalculationConditionsDTO


class CalculationConditionsWebResponse(BaseModel):
    """Calculation exercise conditions web response DTO."""

    conditions_form: CalculationConditionsForm

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
        frozen=True,
    )


class CalculationConditionsPerformingWebResponse(CalculationConditionsDTO):
    """Calculation exercise conditions performing web response DTO."""
