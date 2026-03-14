"""Core domain exercise DTOs."""

from typing import Generic, TypeVar
from uuid import UUID

from pydantic import Field

from apps.core.domains.base_dto import BaseDTO, UuidDTO
from apps.core.domains.exercise.enums import ExerciseStatusEnum
from apps.core.domains.exercise.test_dto import Option, OptionMeta

DomainType = TypeVar('DomainType')


class StoredCase(UuidDTO):
    """Stored exercise case."""

    case: BaseDTO


class ProgressConfigSchema(BaseDTO):
    """Iem study progress config schema."""

    increment: int
    decrement: int


# =================================================
# Test exercise DTOs
# =================================================


class TestCase(BaseDTO):
    """Item study test case."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE,
    )
    case_uuid: str
    question: str
    options: list[Option]


class Explanation(BaseDTO):
    """Explanation of the test answer option."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.EXPLAIN,
    )
    case_question: str
    case_answer: str
    selected_answer: str
    selected_question: str


class TestRequestDTO(BaseDTO):
    """Translation study test exercise the request schema."""

    exercise_status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE
    )
    case_uuid: UUID | None = None
    option_value: int | None = None


class DetailTestRequestDTO(TestRequestDTO):
    """Translation assigned test exercise the request schema."""

    pk: int = Field(description='The exercise DB identifier')


class StoryDomainResult(BaseDTO, Generic[DomainType]):
    """Test domain result to story for user answer validation."""

    cases: tuple[DomainType, ...] = Field(description='Test cases')
    question_pk: int = Field(description='Database question translation ID')
    question: str
    answer: str
    option_value: int
    option_ids: list[OptionMeta]


class TestResponseData(BaseDTO):
    """Translation study test exercise the response schema."""

    status: ExerciseStatusEnum
    data: TestCase | Explanation
