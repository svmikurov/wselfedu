"""WEB request interfaces for exercise study progress."""

from ports.interfaces.schemas.domain.exercise.fields import (
    ExerciseActionField,
    IsKnownField,
)


class ValidatedExerciseProgress(
    ExerciseActionField,
    IsKnownField,
):
    """Validated update progress WEB request data.

    Parameter
    ---------
    action : 'enums.ExerciseAction`
        Exercise action.
    is_known : `bool`
        Is known task item.
    """
