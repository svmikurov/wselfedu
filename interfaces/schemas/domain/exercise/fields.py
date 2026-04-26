"""Exercise contract mixins."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import Field

from interfaces.enums import exercise
from interfaces.schemas import fields as general
from interfaces.schemas.base import ArbitraryDTO, BaseDTO

ProgressT = TypeVar('ProgressT')
OptionT = TypeVar('OptionT')
DomainResult = TypeVar('DomainResult')

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


@dataclass
class QuestionTextField:
    """Exercise *question text* DTO field."""

    question_text: str


@dataclass
class AnswerTextField:
    """Exercise *answer text* DTO field."""

    answer_text: str


@dataclass
class OptionValue:
    """Option value DTO field."""

    option_value: int


@dataclass
class OptionField(Generic[OptionT]):
    """Option DTO field."""

    option: OptionT


@dataclass
class OptionsField(Generic[OptionT]):
    """Options DTO field."""

    options: OptionT


# =================================================
# Exercise task meta
# =================================================


@dataclass
class ProgressValueField:
    """Item study progress DTO integer field."""

    progress_value: int


@dataclass
class ProgressDataField(Generic[ProgressT]):
    """Item study progress DTO integer field."""

    progress: ProgressT


# =================================================
# Existing case
# =================================================


class ExistingCaseField(BaseDTO, Generic[DomainResult]):
    """Existing case DTO field."""

    existing_case: DomainResult | None = Field(
        description=('Existing case of exercise'),
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
