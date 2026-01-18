"""Translation study test exercise schemas."""

from pydantic import BaseModel, ConfigDict, Field

from apps.core.enums import BaseEnum

from ..models import EnglishTranslation


class CaseStatus(BaseEnum):
    """Translation test status enumeration."""

    BAR = 'choice test bar'
    NEW = 'new_case'
    ANSWER = 'user_answer'
    WRONG = 'wrong_answer'
    EXPLANATION = 'correct and wrong answer explanation'
    CORRECT = 'correct_answer'


# ------------
# Inner models
# ------------


class Option(BaseModel):
    """Test case option."""

    value: int = Field(description='Option identifier for business logic')
    text: str = Field(description='Option text to display to the user')


class OptionId(BaseModel):
    """Database item ID matching with test option value."""

    value: int = Field(description='Option identifier for business logic')
    id: int = Field(description='Database item identifier')


class Translation(BaseModel):
    """Translation."""

    orm_model: EnglishTranslation
    model_config = ConfigDict(arbitrary_types_allowed=True)


class Case(BaseModel):
    """Item study test case."""

    status: CaseStatus = Field(
        default=CaseStatus.NEW,
        frozen=True,
    )
    case_uuid: str
    question: str
    options: list[Option]


class Explanation(BaseModel):
    """Explanation of the test answer option."""

    status: CaseStatus = Field(
        default=CaseStatus.EXPLANATION,
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

    status: CaseStatus
    case_uuid: str | None = None
    option_value: str | None = None


class StoryDomainResult(BaseModel):
    """Domain result to story for user answer validation."""

    translations: tuple[Translation, ...]
    question: str
    answer: str
    id: int = Field(description='Database question translation ID')
    option_value: int
    option_ids: list[OptionId]


class TestResponseData(BaseModel):
    """Translation study test exercise the response schema."""

    status: CaseStatus
    data: Case | Explanation
