"""Translation study test exercise schemas."""

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from apps.core.domain.exercise import ExerciseStatusEnum
from apps.core.domain.exercise.test_dto import Option, OptionMeta

from ..models import EnglishTranslation

# ------------
# Inner models
# ------------


class Translation(BaseModel):
    """Translation."""

    orm_model: EnglishTranslation
    model_config = ConfigDict(arbitrary_types_allowed=True)


class TestCase(BaseModel):
    """Item study test case."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE,
        frozen=True,
    )
    case_uuid: str
    question: str
    options: list[Option]


class Explanation(BaseModel):
    """Explanation of the test answer option."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.EXPLAIN,
        frozen=True,
    )
    case_question: str
    case_answer: str
    selected_answer: str
    selected_question: str


# -----------------
# Dependency models
# -----------------


class TestRequestDTO(BaseModel):
    """Translation study test exercise the request schema."""

    exercise_status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE
    )
    case_uuid: UUID | None = None
    option_value: int | None = None


class DetailTestRequestDTO(TestRequestDTO):
    """Translation assigned test exercise the request schema."""

    pk: int = Field(description='The exercise DB identifier')


class StoryDomainResult(BaseModel):
    """Domain result to story for user answer validation."""

    translations: tuple[Translation, ...]
    question_pk: int = Field(description='Database question translation ID')
    question: str
    answer: str
    option_value: int
    option_ids: list[OptionMeta]


class TestResponseData(BaseModel):
    """Translation study test exercise the response schema."""

    status: ExerciseStatusEnum
    data: TestCase | Explanation
