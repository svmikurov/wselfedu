"""Web exercise response adapters."""

from decimal import Decimal
from typing import Any, NamedTuple, Protocol, TypeVar, override

from apps.core.adapters.response.abstract import (
    AbstractResponseAdapter,
)
from apps.core.adapters.response.protocol import AdapterProtocol
from apps.core.adapters.response.status import ResponseStatusEnum
from apps.core.handlers.protocol import RequestContextProtocol
from apps.math import forms
from apps.math.domains.dto import (
    CalculationCaseDTO,
    CalculationExplainDTO,
    StudentCalculationDTO,
    StudentExerciseDTO,
)
from interfaces import NullProtocol
from interfaces.entity.domain.exercise import fields
from interfaces.enums.exercise import ExerciseStatus
from interfaces.schemas.response.generic import (
    OobResponseDTO,
    ResponseDTO,
)

from .dto import (
    ConditionsFormDTO,
    ExerciseFormDTO,
    ExerciseWebDTO,
)

type UseCaseData = Any
DomainType = TypeVar('DomainType', bound=fields.HasExerciseStatus)


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
        NullProtocol,
        ResponseDTO,  # type: ignore
    ]
):
    """Student's exercises web adapter."""

    def to_response(
        self,
        schema: list[StudentExerciseDTO],
        request_context: NullProtocol,
    ) -> ResponseDTO:  # type: ignore
        """Adapt student's exercises for web response."""
        return ResponseDTO(
            domain_status=ResponseStatusEnum.OK,
            context={
                'exercises': [m.model_dump() for m in schema],
            },
        )


# =================================================
# Exercise conditions
# =================================================


class CalculationConditionsWebAdapter(
    AbstractResponseAdapter[
        UseCaseData,
        RequestContextProtocol,
        ConditionsFormDTO,
    ],
):
    """Calculation conditions web response adapter."""

    def to_response(
        self,
        schema: UseCaseData,
        request_context: RequestContextProtocol,
    ) -> ConditionsFormDTO:
        """Adapt calculation conditions for web response."""
        return ConditionsFormDTO(
            conditions_form=forms.RegularCalculationConditionsForm(),
        )


# =================================================
# Exercise case data
# =================================================


class ExerciseCaseSchemaType(Protocol):
    """Calculation exercise schema interface."""

    exercise_status: ExerciseStatus
    data: CalculationCaseDTO


class CalculationWebCaseAdapter(
    AdapterProtocol[
        StudentCalculationDTO,
        RequestContextProtocol,
        OobResponseDTO[Any, Any, Any],
    ]
):
    """Calculation exercise case web response adapter."""

    @override
    def to_response(
        self,
        domain_result: StudentCalculationDTO,
        request_context: RequestContextProtocol,
    ) -> OobResponseDTO[Any, Any, Any]:
        """Adapt current calculation case for web response."""
        return OobResponseDTO(
            domain_status=domain_result.exercise_status,
            context=ExerciseFormDTO(
                question_text=domain_result.data.question_text,
                answer_input_form=forms.NumberInputForm(),
            ),
        )


class StudentCalculationWebCaseAdapter(
    AdapterProtocol[
        StudentCalculationDTO,
        RequestContextProtocol,
        OobResponseDTO,  # type: ignore
    ]
):
    """Calculation exercise case web response adapter."""

    def __init__(self, domain_adapter: CalculationWebCaseAdapter) -> None:
        """Construct the adapter."""
        self._domain_adapter = domain_adapter

    def to_response(
        self,
        schema: StudentCalculationDTO,
        request_context: RequestContextProtocol,
    ) -> OobResponseDTO:  # type: ignore
        """Adapt current calculation case for web response."""
        # Response context contains question and form to answer input.
        adapted = self._domain_adapter.to_response(schema, request_context)

        oob_context = StudentDetailType(
            balance_total=request_context.user.balance_total,
            required_count=schema.availability.required_count,
            success_count=schema.completion.success_count,
        )

        context = adapted.extra_context
        context.setdefault('exercise', {})
        context['exercise'].update(
            {
                'success_count': schema.completion.success_count,
                'required_count': schema.availability.required_count,
            }
        )
        return OobResponseDTO(
            domain_status=adapted.domain_status,
            context=adapted.context,
            extra_context=context,
            oob_html=self._get_oob_html(oob_context),
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


class ExplainCalculationWebAdapter(
    AdapterProtocol[
        CalculationExplainDTO,
        RequestContextProtocol,
        ExerciseWebDTO,
    ]
):
    """Calculation exercise case explanation web response adapter."""

    def to_response(
        self,
        schema: CalculationExplainDTO,
        request_context: RequestContextProtocol,
    ) -> ExerciseWebDTO:
        """Adapt calculation case explanation for web response."""
        return ExerciseWebDTO(  # type: ignore
            exercise_status=schema.exercise_status,
            data=schema.data,
        )
