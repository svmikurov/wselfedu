"""Web exercise response adapters."""

from typing import Any

from apps.core.adapter.response.abc import AbstractResponseAdapter
from apps.core.adapter.response.exercise.web.dto import WebExerciseCaseDTO
from apps.math import forms
from apps.math.domains.dto import CalculationDataDTO, CalculationExplainDTO

from .dto import (
    CalculationWebCase,
    CalculationWebConditions,
    CalculationWebExplain,
)

type UseCaseData = Any


class CalculationConditionsWebAdapter(
    AbstractResponseAdapter[UseCaseData, CalculationWebConditions],
):
    """Calculation conditions web response adapter."""

    def to_response(self, schema: UseCaseData) -> CalculationWebConditions:
        """Adapt calculation conditions for web response."""
        return CalculationWebConditions(
            conditions_form=forms.RegularCalculationConditionsForm(),
        )


class CalculationWebCaseAdapter(
    AbstractResponseAdapter[
        CalculationDataDTO,
        WebExerciseCaseDTO,
    ],
):
    """Calculation exercise case web response adapter."""

    def to_response(self, schema: CalculationDataDTO) -> WebExerciseCaseDTO:
        """Adapt current calculation case for web response."""
        return WebExerciseCaseDTO(
            exercise_status=schema.exercise_status,
            data=CalculationWebCase(
                question_text=schema.data.question_text,
                answer_input_form=forms.NumberInputForm(),
            ),
        )


class ExplainCalculationWebAdapter(
    AbstractResponseAdapter[
        CalculationExplainDTO,
        CalculationWebExplain,
    ],
):
    """Calculation exercise case explanation web response adapter."""

    def to_response(
        self, schema: CalculationExplainDTO
    ) -> CalculationWebExplain:
        """Adapt calculation case explanation for web response."""
        return CalculationWebExplain(
            exercise_status=schema.exercise_status,
            data=schema.data,
        )
