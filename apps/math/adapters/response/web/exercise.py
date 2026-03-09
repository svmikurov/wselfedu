"""Web exercise response adapters."""

from decimal import Decimal
from typing import Any, TypedDict, TypeVar

from apps.core.adapters.response.abc import (
    AbstractResponseAdapter,
    AbstractSimpleResponseAdapter,
)
from apps.core.adapters.response.exercise.web.dto import (
    WebExerciseCaseDTO,
    WebExerciseResponseDTO,
)
from apps.core.adapters.response.shared import WebResponseDTO
from apps.core.domains.exercise.types import ExerciseStatus
from apps.core.handlers.protocol import (
    ContextResponseAdapter,
    OobResultProtocol,
    RequestContextProtocol,
    RequestResultProtocol,
    ResponseAdapter,
)
from apps.math import forms
from apps.math.domains.dto import (
    CalculationDataDTO,
    CalculationExplainDTO,
    StudentExerciseDTO,
)

from .dto import (
    ConditionsFormDTO,
    ExerciseFormDTO,
    ExerciseWebDTO,
)

type UseCaseData = Any
DomainType = TypeVar('DomainType', bound=ExerciseStatus)


class StudentContextType(TypedDict):
    """Typed dict for student context."""

    balance_total: Decimal | None
    required_count: int
    success_count: int


# =================================================
# Student's exercises (Assigned by mentor)
# =================================================


class StudentExercisesWebAdapter(
    AbstractResponseAdapter[
        list[StudentExerciseDTO],
        RequestContextProtocol,
        WebResponseDTO,
    ]
):
    """Student's exercises web adapter."""

    def to_response(
        self,
        schema: list[StudentExerciseDTO],
        request_context: RequestContextProtocol,
    ) -> WebResponseDTO:
        """Adapt student's exercises for web response."""
        return WebResponseDTO(
            context={
                'exercises': [m.model_dump() for m in schema],
            }
        )


# =================================================
# Exercise conditions
# =================================================


class CalculationConditionsWebAdapter(
    AbstractSimpleResponseAdapter[UseCaseData, ConditionsFormDTO],
):
    """Calculation conditions web response adapter."""

    def to_response(self, schema: UseCaseData) -> ConditionsFormDTO:
        """Adapt calculation conditions for web response."""
        return ConditionsFormDTO(
            conditions_form=forms.RegularCalculationConditionsForm(),
        )


# =================================================
# Exercise case data
# =================================================


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

        context = StudentContextType(
            balance_total=request_context.user.balance_total,
            # HACK: Implement details transfer
            required_count=10,
            success_count=3,
        )

        return WebExerciseResponseDTO(
            exercise_status=adapted.exercise_status,
            data=adapted.data,
            oob_html=self._get_oob_html(context),
        )

    def _get_oob_html(self, context: StudentContextType) -> str:
        """Get additional context data."""
        html = """
        <span id="user-balance" hx-swap-oob="true">{}</span>
        <span id="exercise-completion-progress" hx-swap-oob="true">
        {} / {}
        </span>
        """.format(
            context['balance_total'],
            context['success_count'],
            context['required_count'],
        )
        return html


# =================================================
# Exercise explanation
# =================================================


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
