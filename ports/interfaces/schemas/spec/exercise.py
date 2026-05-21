"""Exercise service specification schemas."""

from ports.interfaces.schemas.domain.exercise.exercise import (
    TestAnswer,
    TestTaskDomainResult,
)
from ports.interfaces.schemas.domain.exercise.fields import (
    AnswerField,
)
from ports.interfaces.schemas.fields import OptionDomainField


class CheckTestSpec(
    AnswerField[TestAnswer],
    OptionDomainField[TestTaskDomainResult],
):
    """Check test task answer service specification schema.

    Parameters
    ----------
    answer : `TestAnswer`
        User answer schema.
    domain : `TestTaskDomainResult`
        Stored test task domain result schema.

    """
