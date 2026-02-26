"""Web exercise response adapters."""

from typing import Any, TypeVar

from apps.core.adapter.response.abc import AbstractResponseAdapter
from apps.core.adapter.response.exercise.web.dto import (
    WebExerciseCaseDTO,
    WebExerciseResponseDTO,
)
from apps.core.domain.exercise.types import ExerciseStatus
from apps.core.handlers.protocol import (
    ContextResponseAdapter,
    OobResultProtocol,
    RequestContextProtocol,
    RequestResultProtocol,
    ResponseAdapter,
)
from apps.math import forms
from apps.math.domains.dto import CalculationDataDTO, CalculationExplainDTO

from .dto import (
    ConditionsFormDTO,
    ExerciseFormDTO,
    ExerciseWebDTO,
)

type UseCaseData = Any
DomainType = TypeVar('DomainType', bound=ExerciseStatus)

# ===============================================
# Exercise conditions
# ===============================================


class CalculationConditionsWebAdapter(
    AbstractResponseAdapter[UseCaseData, ConditionsFormDTO],
):
    """Calculation conditions web response adapter."""

    def to_response(self, schema: UseCaseData) -> ConditionsFormDTO:
        """Adapt calculation conditions for web response."""
        return ConditionsFormDTO(
            conditions_form=forms.RegularCalculationConditionsForm(),
        )


# ===============================================
# Exercise case data
# ===============================================


class CalculationWebCaseAdapter(ResponseAdapter[CalculationDataDTO]):
    """Calculation exercise case web response adapter."""

    def to_response(
        self,
        schema: CalculationDataDTO,
    ) -> WebExerciseCaseDTO:
        """Adapt current calculation case for web response."""
        return WebExerciseResponseDTO(
            exercise_status=schema.exercise_status,
            data=ExerciseFormDTO(
                question_text=schema.data.question_text,
                answer_input_form=forms.NumberInputForm(),
            ),
        )


class StudentCalculationWebCaseAdapter(
    ContextResponseAdapter[CalculationDataDTO]
):
    """Calculation exercise case web response adapter."""

    def __init__(
        self,
        domain_adapter: CalculationWebCaseAdapter,
    ) -> None:
        """Construct the adapter."""
        self._domain_adapter = domain_adapter

    def to_response(
        self,
        schema: CalculationDataDTO,
        request_context: RequestContextProtocol,
    ) -> OobResultProtocol:
        """Adapt current calculation case for web response."""
        adapted = self._domain_adapter.to_response(schema)

        return WebExerciseResponseDTO(
            exercise_status=adapted.exercise_status,
            data=adapted.data,
            oob_html=self._get_oob_html(request_context),
        )

    def _get_oob_html(self, context: RequestContextProtocol) -> str:
        """Get additional context data."""
        html = '<span id="user-balance" hx-swap-oob="true">{}</span>'.format(
            context.user.balance_total
        )
        return html


# ===============================================
# Exercise explanation
# ===============================================


class ExplainCalculationWebAdapter(ResponseAdapter[CalculationExplainDTO]):
    """Calculation exercise case explanation web response adapter."""

    def to_response(
        self,
        schema: CalculationExplainDTO,
    ) -> RequestResultProtocol:
        """Adapt calculation case explanation for web response."""
        return ExerciseWebDTO(
            exercise_status=schema.exercise_status,
            data=schema.data,
        )
