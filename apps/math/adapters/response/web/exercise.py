"""Web exercise response adapters."""

from typing import Any

from apps.core.adapter.response.abc import AbstractResponseAdapter
from apps.core.adapter.response.exercise.web.dto import WebCase
from apps.math import forms
from apps.math.domains.dto import CalculationData, CalculationExplain

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
            conditions_form=forms.CalculationConditionsForm()
        )


class CalculationWebCaseAdapter(
    AbstractResponseAdapter[
        CalculationData,
        WebCase,
    ],
):
    """Calculation exercise case web response adapter."""

    def to_response(self, schema: CalculationData) -> WebCase:
        """Adapt current calculation case for web response."""
        return WebCase(
            exercise_status=schema.exercise_status,
            data=CalculationWebCase(
                question_text=schema.data.question_text,
                answer_input_form=forms.NumberInputForm(),
            ),
        )


class ExplainCalculationWebAdapter(
    AbstractResponseAdapter[
        CalculationExplain,
        CalculationWebExplain,
    ],
):
    """Calculation exercise case explanation web response adapter."""

    def to_response(self, schema: CalculationExplain) -> CalculationWebExplain:
        """Adapt calculation case explanation for web response."""
        return CalculationWebExplain(
            exercise_status=schema.exercise_status,
            data=schema.data,
        )
