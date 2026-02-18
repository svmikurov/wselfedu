"""Mathematical exercise service."""

from __future__ import annotations

from typing import TYPE_CHECKING, Type

from wse_exercises.core.math.base.exercise import CalcExercise
from wse_exercises.core.math.base.services import OperandGeneratorABC

from apps.core.domain.exercise.enums import ExerciseStatusEnum
from apps.core.service.exercise.abstract import (
    AbstractExerciseCheck,
    AbstractExerciseExplain,
    AbstractMilestone,
    AbstractRegularExerciseCreate,
)
from apps.math.domains.dto import (
    CalculationAnswerDTO,
    CalculationCaseDTO,
    CalculationConditionDTO,
    CalculationDataDTO,
    CalculationExplainDTO,
    CalculationMetaDTO,
    CalculationResultDTO,
    CalculationSolutionDTO,
)

from ..domains.enums import CalculationEnum

if TYPE_CHECKING:
    from wse_exercises.core.math.task import CalcTask

    from apps.users.models import Person


class CalculationCreateService(
    AbstractRegularExerciseCreate[
        CalculationConditionDTO,
        tuple[CalculationDataDTO, CalculationMetaDTO],
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

    def execute(
        self,
        conditions: CalculationConditionDTO,
    ) -> tuple[CalculationDataDTO, CalculationMetaDTO]:
        """Get calculation exercise case data."""
        task = self._create_task(conditions)
        data = self._build_data(task)
        meta = self._build_meta(task, conditions)
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
    def _build_data(task: CalcTask) -> CalculationDataDTO:
        return CalculationDataDTO(
            exercise_status=ExerciseStatusEnum.NEW_CASE,
            data=CalculationCaseDTO(question_text=task.question.text),
        )

    @staticmethod
    def _build_meta(
        task: CalcTask, conditions: CalculationConditionDTO
    ) -> CalculationMetaDTO:
        return CalculationMetaDTO(
            question_text=task.question.text,
            correct_answer=task.answer.number,
            conditions=conditions,
        )


class CalculationCheckService(
    AbstractExerciseCheck[
        CalculationAnswerDTO,
        CalculationMetaDTO,
        CalculationResultDTO,
    ]
):
    """Calculation exercise user's answer check service."""

    def execute(
        self,
        answer: CalculationAnswerDTO,
        case_meta: CalculationMetaDTO,
    ) -> CalculationResultDTO:
        """Check calculation exercise user'a answer."""
        is_correct = bool(case_meta.correct_answer == int(answer.user_answer))
        return CalculationResultDTO(is_correct=is_correct)


class CalculationMilestoneService(
    AbstractMilestone[CalculationResultDTO, CalculationMetaDTO]
):
    """Calculation exercise milestone."""

    def execute(
        self,
        user: Person,
        result: CalculationResultDTO,
        case_meta: CalculationMetaDTO,
    ) -> None:
        """Apply the answer result."""
        return


class CalculationExplainService(
    AbstractExerciseExplain[
        CalculationAnswerDTO, CalculationMetaDTO, CalculationExplainDTO
    ]
):
    """Explain the calculation exercise solution."""

    def execute(
        self,
        answer: CalculationAnswerDTO,
        case_meta: CalculationMetaDTO,
    ) -> CalculationExplainDTO:
        """Explain the exercise case."""
        return CalculationExplainDTO(
            exercise_status=ExerciseStatusEnum.EXPLAIN,
            data=CalculationSolutionDTO(
                solution_text=(
                    f'{case_meta.question_text} = {case_meta.correct_answer}'
                ),
            ),
        )
