"""Mathematical exercise service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from wse_exercises.core.math.base.exercise import CalcExercise
from wse_exercises.core.math.base.services import OperandGeneratorABC

from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationDomainDTO,
    CalculationExplainDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
    CalculationSolutionDTO,
)
from ports.abstract.service import (
    AbstractUserSpecService,
)
from ports.contract.enums.exercise import ExerciseStatus

from ..domains.enums import CalculationEnum

if TYPE_CHECKING:
    from wse_exercises.core.math.task import CalcTask


class CalculationCreateService(
    AbstractUserSpecService[
        CalculationConditionDTO,
        CalculationDomainDTO,
    ]
):
    """Create calculation exercise service."""

    def __init__(
        self,
        domains: dict[CalculationEnum, Type[CalcExercise]],
        operand_generator: OperandGeneratorABC,
    ) -> None:
        """Construct the service."""
        self._domains = domains
        self._operand_generator = operand_generator

    def execute(  # type: ignore
        self,
        configuration: CalculationConditionDTO,
    ) -> tuple[CalculationDomainDTO, CalculationMetaDTO]:
        """Get calculation exercise case data."""
        task = self._create_task(configuration.conditions)  # type: ignore
        data = self._build_data(task)
        meta = self._build_meta(task)
        return data, meta

    def _create_task(self, request_data: CalculationConditionDTO) -> CalcTask:
        domain_type = self._domains[
            CalculationEnum(request_data.operation_type)
        ]
        exercise = domain_type(
            operand_generator=self._operand_generator,
            config={
                'min_value': request_data.min_operand,
                'max_value': request_data.max_operand,
            },
        )
        return exercise.create_task()

    @staticmethod
    def _build_data(task: CalcTask) -> CalculationDomainDTO:
        return CalculationDomainDTO(
            exercise_status=ExerciseStatus.NEW_TASK,
            data=CalculationCaseDTO(
                question_text=task.question.text,
            ),
        )

    @staticmethod
    def _build_meta(task: CalcTask) -> CalculationMetaDTO:
        return CalculationMetaDTO(
            question_text=task.question.text,
            correct_answer=task.answer.number,
        )


class CalculationCheckService(
    AbstractUserSpecService[
        CalculationAnswerDTO,
        CalculationMetaDTO,
    ]
):
    """Calculation exercise user's answer check service."""

    def execute(  # type: ignore
        self,
        answer: CalculationAnswerDTO,  # type: ignore
        case_meta: CalculationMetaDTO,  # type: ignore
    ) -> CalculationResultDTO:
        """Check calculation exercise user'a answer."""
        is_correct = bool(case_meta.correct_answer == int(answer.user_answer))
        return CalculationResultDTO(is_correct=is_correct)


class CalculationExplainService(
    AbstractUserSpecService[
        CalculationAnswerDTO,
        CalculationMetaDTO,
    ]
):
    """Explain the calculation exercise solution."""

    def execute(  # type: ignore
        self,
        answer: CalculationAnswerDTO,  # type: ignore
        case_meta: CalculationMetaDTO,  # type: ignore
    ) -> CalculationExplainDTO:
        """Explain the exercise case."""
        return CalculationExplainDTO(
            exercise_status=ExerciseStatus.EXPLAIN,
            data=CalculationSolutionDTO(
                solution_text=(
                    f'{case_meta.question_text} = {case_meta.correct_answer}'
                ),
            ),
        )
