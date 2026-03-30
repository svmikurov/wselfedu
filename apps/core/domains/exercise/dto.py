"""Core domain exercise DTOs."""

from typing import Any, TypeVar

from pydantic import Field, field_validator

from ..dto import ArbitraryDTO, BaseDTO
from .enums import DisplayOrder, ExerciseStatusEnum

DomainType = TypeVar('DomainType')
DomainResult = TypeVar('DomainResult')

# =================================================
# DTO fields
# =================================================


class ResourceIdentifierField(BaseDTO):
    """Database resource identifier DTO field."""

    pk: int = Field(
        description='Database item ID',
    )


class ExerciseStatusField(BaseDTO):
    """Exercise status DTO field with *explain case* default value."""

    status: ExerciseStatusEnum = Field(
        default=ExerciseStatusEnum.NEW_CASE,
        description='Exercise status',
    )


class TextField(BaseDTO):
    """Text value DTO field."""

    text: str = Field(
        description='Display option text',
    )


# -------------------------------------------------
# Exercise answer DTO fields
# -------------------------------------------------


class QuestionTextField(BaseDTO):
    """Exercise text question DTO field."""

    question_text: str = Field(
        description='Display question text',
    )


class AnswerTextField(BaseDTO):
    """Exercise text answer DTO field."""

    answer_text: str = Field(
        description='Display answer text',
    )


class DefineField(BaseDTO):
    """Define exercise item DTO text field."""

    define: str = Field(
        description='Question item text',
    )


class ExplainField(BaseDTO):
    """Explain exercise item DTO text field."""

    explain: str = Field(
        description='Answer item text',
    )


# -------------------------------------------------
# Exercise check DTO fields
# -------------------------------------------------


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


# -------------------------------------------------
# *Exercise* / *Current exercise case* meta data
# -------------------------------------------------


# HACK: Relocate from fields chapter
class ProgressDTO(BaseDTO):
    """Item study progress DTO."""

    value: int = Field(
        description='Item study current progress value',
    )
    update_url: str = Field(
        description='Item study update progress url',
    )
    increment_payload: dict[str, Any] = Field(
        description='Item study increment progress payload',
    )
    decrement_payload: dict[str, Any] = Field(
        description='Item study decrement progress payload',
    )


class ProgressValueField(BaseDTO):
    """Item study progress DTO integer field."""

    progress_value: int = Field(
        description='Item study progress',
    )


class ProgressDataField(BaseDTO):
    """Item study progress DTO integer field."""

    progress: ProgressDTO = Field(
        description='Item study progress',
    )


# =================================================
# DTO mixins
# =================================================


class WebParametersMixin:
    """Provides parameters validation."""

    @field_validator('mark', mode='before')
    @classmethod
    def fix_empty_list(cls, value: str) -> str | list[str]:
        """Fix empty list."""
        return [] if value == '[]' else value

    @field_validator(
        'category', 'source', 'start_period', 'end_period', mode='before'
    )
    @classmethod
    def fix_empty_int(cls, value: str) -> str | None:
        """Return None if string is empty else value."""
        return None if value == '' else value

    @field_validator(
        'is_study', 'is_repeat', 'is_examine', 'is_know', mode='before'
    )
    @classmethod
    def fix_empty_bool(cls, value: str) -> str | bool:
        """Return None if string is empty else value."""
        return True if value == '' else value


class WebSettingsMixin:
    """Provides settings validation."""

    @field_validator('item_count', mode='before')
    @classmethod
    def fix_empty_int(cls, value: str) -> str | None:
        """Return None if string is empty else value."""
        return None if value == '' else value


# =================================================
# DTOs
# =================================================

# -------------------------------------------------
# Exercise parameters DTO
# -------------------------------------------------


class ProgressConfigDTO(BaseDTO):
    """Item study progress config fields."""

    increment: int = Field(
        description='Increment item study progress value',
    )
    decrement: int = Field(
        description='Decrement item study progress value',
    )


class LookupConditionsDTO(
    WebParametersMixin,
    ArbitraryDTO,
):
    """Provides lookup conditions fields."""

    category: int | None = None
    mark: list[int] = []
    source: int | None = None
    start_period: int | None = None
    end_period: int | None = None

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


class ExerciseConfigDTO(
    WebSettingsMixin,
    BaseDTO,
):
    """Provides translation settings fields."""

    display_order: DisplayOrder = DisplayOrder.DEFINE
    item_count: int | None = None

    # NOTE: For translation exercise only.
    @field_validator('display_order', mode='before')
    @classmethod
    def normalize_display_order(cls, value: str) -> str:
        """Normalize 'display_order' field."""
        match value:
            case 'to_native':
                return DisplayOrder.EXPLAIN
            case 'from_native':
                return DisplayOrder.DEFINE
            case _:
                return value


class ExerciseParametersDTO(BaseDTO):
    """Regular request with study conditions."""

    conditions: LookupConditionsDTO = Field(
        default_factory=LookupConditionsDTO,
    )
    conf: ExerciseConfigDTO = Field(
        default_factory=ExerciseConfigDTO,
    )


# -------------------------------------------------
# Text exercise check result DTO
# -------------------------------------------------


class TextExerciseCheckResult(
    IsCorrectAnswerField,
    ExerciseStatusField,
    QuestionTextField,
    AnswerTextField,
    SelectedQuestionTextField,
    SelectedAnswerTextField,
    BaseDTO,
):
    """Explanation of the test answer option."""
