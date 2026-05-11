"""Exercise service specification schemas."""

from pydantic import Field

from interfaces.schemas.domain.exercise import (
    TestAnswer,
    TestExerciseDomainResult,
)
from ports.interfaces.schemas.base import BaseDTO


class CheckTestSpec(BaseDTO):
    """Check test task answer service specification schema."""

    answer: TestAnswer = Field(
        description='User answer on test task',
    )
    case: TestExerciseDomainResult | None = Field(
        description='Stored performing test task, domain result',
    )
