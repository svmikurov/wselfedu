"""Exercise service schema interface."""

from ports.interfaces.schemas.domain.exercise.exercise import (
    PresentationExerciseDomainResult,
    TestExerciseDomainResult,
)
from ports.interfaces.schemas.domain.exercise.flow import ExerciseCase

# =================================================
# Create exercise task cases
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


# =================================================
# Update item study progress cases
# =================================================


class UpdateProgressCase(ExerciseCase[None]):
    """Test exercise case DTO.

    Parameters
    ----------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : None
        No return data from update progress service.

    """
