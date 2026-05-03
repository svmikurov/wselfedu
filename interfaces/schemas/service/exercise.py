"""Exercise service schema interface."""

from contracts.schemas.domain.exercise.flow import ExerciseCase
from interfaces.schemas.domain.exercise import (
    PresentationExerciseDomainResult,
    TestExerciseDomainResult,
)

# =================================================
# Exercise cases
# =================================================


class PresentationExerciseCase(ExerciseCase[PresentationExerciseDomainResult]):
    """Presentation exercise case DTO.

    Parameter
    ---------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : `PresentationExerciseDomainResult`
        Presentation exercise domain result.
    """


class TestExerciseCase(ExerciseCase[TestExerciseDomainResult]):
    """Test exercise case DTO.

    Parameter
    ---------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : `TestExerciseDomainResult`
        Test exercise domain result.
    """
