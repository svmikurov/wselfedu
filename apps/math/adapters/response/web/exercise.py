"""Web exercise response adapters."""

from decimal import Decimal
from typing import Any, NamedTuple, TypeVar

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
    CalculationDTO,
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


class StudentDetailType(NamedTuple):
    """Student exercise detail type."""

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


class CalculationWebCaseAdapter(ResponseAdapter[CalculationDTO]):
    """Calculation exercise case web response adapter."""

    def to_response(
        self,
        schema: CalculationDTO,
    ) -> WebExerciseCaseDTO:
        """Adapt current calculation case for web response."""
        return WebExerciseResponseDTO(
            exercise_status=schema.exercise_status,
            data=ExerciseFormDTO(
                question_text=schema.data.question_text,
                answer_input_form=forms.NumberInputForm(),
            ),
        )


class StudentCalculationWebCaseAdapter(ContextResponseAdapter[CalculationDTO]):
    """Calculation exercise case web response adapter."""

    def __init__(self, domain_adapter: CalculationWebCaseAdapter) -> None:
        """Construct the adapter."""
        self._domain_adapter = domain_adapter

    def to_response(
        self,
        schema: CalculationDTO,
        request_context: RequestContextProtocol,
    ) -> OobResultProtocol:
        """Adapt current calculation case for web response."""
        # Response context contains question and form to answer input.
        adapted = self._domain_adapter.to_response(schema)

        oob_context = StudentDetailType(
            balance_total=request_context.user.balance_total,
            required_count=schema.parameters.availability.required_count,
            success_count=schema.parameters.completion.success_count,
        )

        return WebExerciseResponseDTO(
            exercise_status=adapted.exercise_status,
            data=adapted.data,
            oob_html=self._get_oob_html(oob_context),
            context={
                'exercise': {
                    'success_count': oob_context.success_count,
                    'required_count': oob_context.required_count,
                }
            }
        )

    def _get_oob_html(self, context: StudentDetailType) -> str:
        return f"""
        <span id="user-balance" hx-swap-oob="true">
        {context.balance_total}
        </span>
        <span id="exercise-completion-progress" hx-swap-oob="true">
        {context.success_count} / {context.required_count}
        </span>
        """


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
