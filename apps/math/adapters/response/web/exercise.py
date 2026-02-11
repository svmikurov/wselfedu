"""Web exercise response adapters."""

from typing import Any

from apps.core.adapter.response.abc import AbstractResponseAdapter
from apps.math.adapters.response.web.dto import (
    CalculationConditionsPerformingWebResponse,
    CalculationConditionsWebResponse,
)
from apps.math.forms import CalculationConditionsForm
from apps.math.validators.web.dto import CalculationConditionsWebRequest

type UseCaseData = Any


class CalculationConditionsWebAdapter(
    AbstractResponseAdapter[UseCaseData, CalculationConditionsWebResponse],
):
    """Calculation conditions web response adapter."""

    def to_response(
        self, data: UseCaseData
    ) -> CalculationConditionsWebResponse:
        """Convert data to response representation."""
        return CalculationConditionsWebResponse(
            conditions_form=CalculationConditionsForm()
        )


class RegularConditionsWebAdapter(
    AbstractResponseAdapter[
        CalculationConditionsWebRequest,
        CalculationConditionsPerformingWebResponse,
    ],
):
    """Regular calculation conditions web response adapter."""

    def to_response(
        self, data: CalculationConditionsWebRequest
    ) -> CalculationConditionsPerformingWebResponse:
        """Convert data to response representation."""
        return CalculationConditionsPerformingWebResponse(**data.model_dump())
