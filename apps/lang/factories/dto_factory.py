"""Language discipline DTO factory."""

from apps.core.domains.exercise.dto import ExerciseParametersDTO
from apps.core.domains.exercise.presentation.dto import PresentationCase
from apps.core.domains.exercise.test.dto import TestExerciseCase
from apps.core.factories.abstract import AbstractExerciseDTOFactory


# HACK: Simple implementation
class PresentationDTOFactory(
    AbstractExerciseDTOFactory[
        PresentationCase, ExerciseParametersDTO, PresentationCase
    ]
):
    """Presentation case DTO factory."""

    def build(
        self,
        case: PresentationCase,
        parameters: ExerciseParametersDTO,
    ) -> PresentationCase:
        """Build presentation exercise DTO."""
        return case


class TestExerciseDTOFactory(
    AbstractExerciseDTOFactory[
        TestExerciseCase, ExerciseParametersDTO, TestExerciseCase
    ]
):
    """Presentation case DTO factory."""

    def build(
        self,
        case: TestExerciseCase,
        parameters: ExerciseParametersDTO,
    ) -> TestExerciseCase:
        """Build presentation exercise DTO."""
        return case
