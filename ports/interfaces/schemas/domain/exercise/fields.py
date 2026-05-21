"""Exercise contract mixins."""

from typing import Generic, TypeVar

from pydantic import Field

from ports.contract.enums import exercise
from ports.interfaces.schemas import fields as general
from ports.interfaces.schemas.base import ArbitraryDTO, BaseDTO

ProgressT = TypeVar('ProgressT')
OptionT = TypeVar('OptionT')
DomainResult = TypeVar('DomainResult')
T = TypeVar('T')

# =================================================
# Process exercise case
# =================================================


class ExerciseActionField(BaseDTO):
    """Provides exercise process action DTO's field."""

    action: exercise.ExerciseAction = Field(
        description='Process exercise action',
    )


class ExerciseStatusField(general.StatusField[exercise.ExerciseStatus]):
    """Provides exercise *status* DTO field."""

    status: exercise.ExerciseStatus


class PhasesField(ArbitraryDTO):
    """Exercise perform phases DTO field."""

    phases: list[exercise.DisplayOrder] = Field(
        description="Current exercise phase's order",
    )


class OptionValueField(ArbitraryDTO):
    """User answer *option value* DTO field."""

    option_value: int = Field(
        description='User answer option value DTO field',
    )


class Option(
    general.ValueField,
    general.TextField,
):
    """Test exercise option schema.

    Parameter
    ---------
    value : `int`
        Option value.
    text : `str`
        Option text.
    """


class OptionsField(BaseDTO):
    """Options DTO field."""

    options: list[Option]


# =================================================
# Exercise task candidate
# =================================================


class DefineField(BaseDTO):
    """Define exercise item DTO text field."""

    define: str = Field(
        description='Question item text',
    )


class MeanField(BaseDTO):
    """Mean exercise case DTO text field."""

    mean: str = Field(
        description='Case mean text field',
    )


# =================================================
# Exercise case
# =================================================


class QuestionField(BaseDTO, Generic[T]):
    """Provides *question* DTO generic field."""

    question: T


class AnswerField(BaseDTO, Generic[T]):
    """Provides *answer* DTO generic field."""

    answer: T


class QuestionTextField(BaseDTO):
    """Exercise *question text* DTO field."""

    question_text: str


class AnswerTextField(BaseDTO):
    """Exercise *answer text* DTO field."""

    answer_text: str


class OptionValue(BaseDTO):
    """Option value DTO field."""

    question_option_value: int


class TaskItemField(BaseDTO, Generic[OptionT]):
    """task item DTO field."""

    item: OptionT


class TaskItemsField(BaseDTO, Generic[OptionT]):
    """Task items DTO field."""

    items: OptionT


# =================================================
# Exercise task meta
# =================================================


class ProgressValueField(BaseDTO):
    """Item study progress DTO integer field."""

    progress_value: int


class ProgressDataField(BaseDTO, Generic[ProgressT]):
    """Item study progress DTO integer field."""

    progress: ProgressT


class IsKnownField(BaseDTO):
    """Item study progress DTO integer field."""

    is_known: bool


# =================================================
# Existing case
# =================================================


class CaseField(BaseDTO, Generic[DomainResult]):
    """Case DTO field."""

    case: DomainResult | None = Field(
        description=('Case of exercise'),
        default=None,
    )


# =================================================
# Exercise check
# =================================================


class IsCorrectAnswerField(BaseDTO):
    """Is correct the user's answer DTO boolean field."""

    is_correct: bool = Field(
        description="Is correct the user's answer",
    )


class SelectedQuestionTextField(BaseDTO):
    """Selected question option DTO text field."""

    selected_question_text: str = Field(
        description='Question text for user answer text option select',
    )


class SelectedAnswerTextField(BaseDTO):
    """Selected answer option DTO text field."""

    selected_answer_text: str = Field(
        description='User answer text option select',
    )


# =================================================
# Explain
# =================================================


class QuestionDefineField(BaseDTO):
    """Task question define DTO field."""

    question_define: str


class QuestionMeanField(BaseDTO):
    """Task question mean DTO field."""

    question_mean: str


class AnswerDefineField(BaseDTO):
    """User answer definion DTO field."""

    answer_define: str


class AnswerMeanField(BaseDTO):
    """User answer meaning DTO field."""

    answer_mean: str
