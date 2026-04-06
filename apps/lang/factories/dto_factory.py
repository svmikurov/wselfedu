"""Language discipline DTO factory."""

from typing import override

from apps.core.domains.exercise.dto import ExerciseParametersDTO
from apps.core.domains.exercise.presentation.dto import PresentationCase
from apps.core.domains.exercise.test.dto import TestExerciseCase
from apps.core.factories.abstract import AbstractCaseFactory


# HACK: Simple implementation
class PresentationDTOFactory(
    AbstractCaseFactory[
        ExerciseParametersDTO, PresentationCase, PresentationCase
    ]
):
    """Presentation case DTO factory."""

    @override
    def build(
        self,
        conf: ExerciseParametersDTO,
        case: PresentationCase,
    ) -> PresentationCase:
        """Build presentation exercise DTO."""
        return case


class TestExerciseDTOFactory(
    AbstractCaseFactory[
        ExerciseParametersDTO, TestExerciseCase, TestExerciseCase
    ]
):
    """Presentation case DTO factory."""

    @override
    def build(
        self,
        conf: ExerciseParametersDTO,
        case: TestExerciseCase,
    ) -> TestExerciseCase:
        """Build presentation exercise DTO."""
        return case
