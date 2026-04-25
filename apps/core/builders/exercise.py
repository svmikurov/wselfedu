"""Exercise case DTO null builder."""

from typing import TypeVar

from apps.core.domains.exercise.presentation.protocol import (
    PresentationDomainResultProtocol,
    PresentationTaskProtocol,
)
from apps.core.domains.exercise.protocol import (
    ExerciseProcessResultProtocol,
)
from apps.core.domains.exercise.test.dto import TestExerciseCase
from apps.core.domains.exercise.test.protocol import (
    TestExerciseDomainResultProtocol,
    TestExerciseTaskProtocol,
)
from interfaces.enums.exercise import ExerciseStatus
from interfaces.protocols.domain.exercise import HasExerciseStatus
from interfaces.schemas.domain.exercise.presentation import (
    PresentationTask,
)
from interfaces.schemas.domain.exercise.result import (
    ExerciseDomainResultDTO,
)

from .protocol import ExerciseTaskBuilderProtocol

SpecT = TypeVar('SpecT')

# DEPRECATED: REmove type hint
DomainT = TypeVar('DomainT', bound=HasExerciseStatus)

# =================================================
# Presentation exercise task DTO builder
# =================================================


class ExercisePresentationBuilder(
    ExerciseTaskBuilderProtocol[
        PresentationDomainResultProtocol,
        SpecT,
        PresentationTaskProtocol,
    ],
):
    """Exercise case DTO null builder."""

    def build(
        self,
        domain: PresentationDomainResultProtocol,
        spec: SpecT,
    ) -> PresentationTaskProtocol:
        """Build exercise case DTO."""
        return PresentationTask(
            status=domain.status,
            question_text=domain.case.option.define,
            answer_text=domain.case.option.mean,
            progress_value=domain.case.option.progress,
        )


# =================================================
# Test exercise task DTO builder
# =================================================


class TestExerciseTaskBuilder(
    ExerciseTaskBuilderProtocol[
        TestExerciseDomainResultProtocol,
        SpecT,
        TestExerciseTaskProtocol,
    ],
):
    """Test exercise task DTO builder."""

    def build(
        self,
        domain: TestExerciseDomainResultProtocol,
        spec: SpecT,
    ) -> TestExerciseTaskProtocol:
        """Build exercise case DTO."""
        option_value = domain.case.value
        options = domain.case.options

        return TestExerciseCase(
            status=domain.status,
            question_text=options[option_value].define,
            options=options,
        )


# =================================================
# Simple exercise task DTO builder
# =================================================

# DEPRECATED: Remove exercise case DTO builder


class ExerciseCaseBuilder(
    ExerciseTaskBuilderProtocol[
        DomainT, SpecT, ExerciseProcessResultProtocol[DomainT]
    ],
):
    """Exercise case DTO builder."""

    def build(
        self,
        domain: DomainT,
        spec: SpecT,
    ) -> ExerciseProcessResultProtocol[DomainT]:
        """Build exercise case DTO."""
        return ExerciseDomainResultDTO(
            status=ExerciseStatus.NEW_TASK,
            case=domain,
        )
