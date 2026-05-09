"""WEB request interfaces for exercise study progress."""

from contracts.schemas.domain.exercise.fields import (
    ExerciseActionField,
    OptionValueField,
)


class ValidatedCreateTask(
    ExerciseActionField,
):
    """Validated create task WEB request data.

    Parameter
    ---------
    action : `ExerciseAction`
        Exercise action.

    """


class ValidatedCheckTestAnswer(
    ExerciseActionField,
    OptionValueField,
):
    """Validated check user answer on test task WEB request data.

    Parameter
    ---------
    action : `ExerciseAction`
        Exercise action.
    option_value : `int`
        User answer option value.

    """
