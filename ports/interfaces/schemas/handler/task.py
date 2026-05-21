"""Task action reqeust data validation schemas."""

from ports.interfaces.schemas.domain.exercise.fields import (
    ExerciseActionField,
    IsKnownField,
    OptionValueField,
)


class CreateTaskSchema(
    ExerciseActionField,
):
    """Create task WEB request data validation schema.

    Parameters
    ----------
    action : `ExerciseAction`
        Exercise action.

    """


class CheckTestAnswerSchema(
    ExerciseActionField,
    OptionValueField,
):
    """Check user answer test task WEB request data validation schema.

    Parameters
    ----------
    action : `ExerciseAction`
        Exercise action.
    option_value : `int`
        User answer option value.

    """


class ProgressUpdateSchema(
    ExerciseActionField,
    IsKnownField,
):
    """Update progress WEB request data validation schema.

    Parameters
    ----------
    action : 'ExerciseAction`
        Exercise action.
    is_known : `bool`
        Is known task item.

    """


class ExplainTaskSchema(
    ExerciseActionField,
):
    """Explain task schema.

    Parameters
    ----------
    action : 'ExerciseAction`
        Exercise action.

    """
