"""Exercise service schema interface."""

from ports.interfaces.schemas.domain.exercise.exercise import (
    PresentationTaskDomainResult,
    TaskItem,
    TestTaskDomainResult,
)
from ports.interfaces.schemas.domain.exercise.flow import (
    ExerciseCase,
    PresentationTask,
    TestTask,
)

# =================================================
# Create exercise task cases
# =================================================


class PresentationExerciseCase(
    ExerciseCase[PresentationTaskDomainResult, TestTask[TaskItem]]
):
    """Presentation exercise case DTO.

    Parameters
    ----------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : `PresentationExerciseDomainResult`
        Presentation exercise domain result.
    task : `TestExerciseTask[TaskItem]`.
        Test task.

    """


class TestExerciseCase(ExerciseCase[TestTaskDomainResult, PresentationTask]):
    """Test exercise case DTO.

    Parameters
    ----------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : `TestExerciseDomainResult`
        Test exercise domain result.
    task : `PresentationTask`
        Presentation task.

    """


# =================================================
# Update item study progress cases
# =================================================


class UpdateProgressCase(ExerciseCase[None, None]):
    """Test exercise case DTO.

    Parameters
    ----------
    status : `enums.ExerciseStatus`
        Exercise current status enumeration.
    domain : None
        No return data from update progress service.

    """
