"""WEB request interfaces for exercise study progress."""

from contracts.schemas.domain.exercise.fields import ExerciseActionField


class ValidatedCreateTaskRequest(
    ExerciseActionField,
):
    """Validated create task WEB request data.
    
    Parameter
    ---------
    action : `ExerciseAction`
        Exercise action.
    """
