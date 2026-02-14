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
    CalculationAnswer,
    CalculationCase,
    CalculationConditions,
    CalculationData,
    CalculationExplain,
    CalculationMeta,
    CalculationResult,
    CalculationSolution,
)

from ..domains.enums import CalculationEnum

if TYPE_CHECKING:
    from wse_exercises.core.math.task import CalcTask

    from apps.users.models import Person


class CalculationCreateService(
    AbstractRegularExerciseCreate[
        CalculationConditions,
        tuple[CalculationData, CalculationMeta],
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
        conditions: CalculationConditions,
    ) -> tuple[CalculationData, CalculationMeta]:
        """Get calculation exercise case data."""
        task = self._create_task(conditions)
        data = self._build_data(task)
        meta = self._build_meta(task, conditions)
        return data, meta

    def _create_task(self, request_data: CalculationConditions) -> CalcTask:
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
    def _build_data(task: CalcTask) -> CalculationData:
        return CalculationData(
            exercise_status=ExerciseStatusEnum.NEW_CASE,
            data=CalculationCase(question_text=task.question.text),
        )

    @staticmethod
    def _build_meta(
        task: CalcTask, conditions: CalculationConditions
    ) -> CalculationMeta:
        return CalculationMeta(
            question_text=task.question.text,
            correct_answer=task.answer.number,
            conditions=conditions,
        )


class CalculationCheckService(
    AbstractExerciseCheck[
        CalculationAnswer,
        CalculationMeta,
        CalculationResult,
    ]
):
    """Calculation exercise user's answer check service."""

    def execute(
        self,
        answer: CalculationAnswer,
        case_meta: CalculationMeta,
    ) -> CalculationResult:
        """Check calculation exercise user'a answer."""
        is_correct = bool(case_meta.correct_answer == int(answer.user_answer))
        return CalculationResult(is_correct=is_correct)


class CalculationMilestoneService(
    AbstractMilestone[CalculationResult, CalculationMeta]
):
    """Calculation exercise milestone."""

    def execute(
        self,
        user: Person,
        result: CalculationResult,
        case_meta: CalculationMeta,
    ) -> None:
        """Apply the answer result."""
        return


class CalculationExplainService(
    AbstractExerciseExplain[
        CalculationAnswer, CalculationMeta, CalculationExplain
    ]
):
    """Explain the calculation exercise solution."""

    def execute(
        self,
        answer: CalculationAnswer,
        case_meta: CalculationMeta,
    ) -> CalculationExplain:
        """Explain the exercise case."""
        return CalculationExplain(
            exercise_status=ExerciseStatusEnum.EXPLAIN,
            data=CalculationSolution(
                solution_text=(
                    f'{case_meta.question_text} = {case_meta.correct_answer}'
                ),
            ),
        )
