"""Exercise service specification schemas."""

from pydantic import Field

from ports.interfaces.schemas.base import BaseDTO
from ports.interfaces.schemas.domain.exercise.exercise import (
    TestAnswer,
    TestTaskDomainResult,
)


class CheckTestSpec(BaseDTO):
    """Check test task answer service specification schema."""

    answer: TestAnswer = Field(
        description='User answer on test task',
    )
    domain: TestTaskDomainResult | None = Field(
        description='Stored performing test task, domain result',
    )
