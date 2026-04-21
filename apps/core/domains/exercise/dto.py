"""Core domain exercise DTOs."""

from typing import Any, Generic, TypeVar

from pydantic import Field, field_validator

from ..dto import ArbitraryDTO, BaseDTO
from .enums import DisplayOrder, ExerciseStatusEnum

DomainType = TypeVar('DomainType')
DomainResult = TypeVar('DomainResult')
OptionT = TypeVar('OptionT')

# =================================================
# DTO fields
# =================================================


class ResourceIdentifierField(BaseDTO):
    """Database resource identifier DTO field."""

    pk: int = Field(
        description='Database item ID',
    )


class ExerciseStatusSchema(BaseDTO):
    """Exercise status schema with *explain case* default value."""

    status: ExerciseStatusEnum = Field(
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


class OptionField(BaseDTO, Generic[OptionT]):
    """Option DTO field."""

    option: OptionT


class AnswerTextOptionsFiled(BaseDTO, Generic[OptionT]):
    """Exercise text options answer DTO field."""

    answer_text_options: list[OptionT] = Field(
        description='Display answer text options',
    )


class OptionsField(ArbitraryDTO, Generic[OptionT]):
    """Option value DTO field."""

    options: list[OptionT] = Field(
        description='Extended option data',
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
# Progress configuration DTO
# -------------------------------------------------


class ProgressConfigDTO(BaseDTO):
    """Item study progress config fields."""

    increment: int = Field(
        description='Increment item study progress value',
    )
    decrement: int = Field(
        description='Decrement item study progress value',
    )


# -------------------------------------------------
# Exercise parameters DTO
# -------------------------------------------------


class LookupConditionsDTO(
    WebParametersMixin,
    ArbitraryDTO,
):
    """Provides lookup conditions fields."""

    category: int | None = None
    mark: list[int] = Field(
        default_factory=list,
    )
    source: int | None = None
    start_period: int | None = None
    end_period: int | None = None

    is_study: bool = True
    is_repeat: bool = True
    is_examine: bool = True
    is_know: bool = True


# HACK: Split to field composition
class ExerciseConfigDTO(
    WebSettingsMixin,
    BaseDTO,
):
    """Exercise config DTO."""

    display_order: DisplayOrder = Field(
        default=DisplayOrder.DEFINE,
    )
    item_count: int | None = Field(
        description='Candidates of items to exercise count',
        default=None,
    )
    option_count: int | None = Field(
        description='Exercise task option cont (for test exercise)',
        default=7,
    )

    # NOTE: For translation exercise only.
    @field_validator('display_order', mode='before')
    @classmethod
    def normalize_display_order(cls, value: str) -> str:
        """Normalize 'display_order' field."""
        match value:
            case 'to_native':
                return DisplayOrder.MEAN
            case 'from_native':
                return DisplayOrder.DEFINE
            case _:
                return value


class ExerciseSettingsDTO(
    BaseDTO,
):
    """Provides translation settings fields."""

    question_timeout: int | None = None
    answer_timeout: int | None = None


class LookupConditionsField(BaseDTO):
    """Lockup conditions DTO field."""

    conditions: LookupConditionsDTO = Field(
        default_factory=LookupConditionsDTO,
    )


class ExerciseConfigField(BaseDTO):
    """Exercise configuration DTO field."""

    conf: ExerciseConfigDTO = Field(
        default_factory=ExerciseConfigDTO,
    )


class ExerciseSettingsField(BaseDTO):
    """Exercise settings DTO field."""

    settings: ExerciseSettingsDTO = Field(
        default_factory=ExerciseSettingsDTO,
    )


class ExistingCaseField(BaseDTO, Generic[DomainResult]):
    """Existing case DTO field."""

    existing_case: DomainResult | None = Field(
        description=('Existing case of exercise'),
        default=None,
    )


class ExerciseParametersDTO(
    LookupConditionsField,
    ExerciseConfigField,
    ExerciseSettingsField,
):
    """Exercise parameters DTO."""


class ExerciseSpecDTO(
    LookupConditionsField,
    ExerciseConfigField,
    ExerciseSettingsField,
    ExistingCaseField[DomainResult],
    Generic[DomainResult],
):
    """Exercise spec DTO."""


# -------------------------------------------------
# Exercise service result case DTO
# -------------------------------------------------


class CaseDTO(
    ExerciseStatusSchema,
):
    """Case DTO."""


# -------------------------------------------------
# Text exercise check result DTO
# -------------------------------------------------


class TextExerciseCheckResult(
    IsCorrectAnswerField,
    # QuestionTextField,
    # AnswerTextField,
    # SelectedQuestionTextField,
    # SelectedAnswerTextField,
    BaseDTO,
):
    """Explanation of the test answer option."""


# -------------------------------------------------
# Text exercise explain DTO
# -------------------------------------------------


class TextExerciseExplainDTO(
    QuestionTextField,
    AnswerTextField,
    SelectedQuestionTextField,
    SelectedAnswerTextField,
    BaseDTO,
):
    """Explanation of the test answer option."""


# -------------------------------------------------
# Text exercise domain result DTO
# -------------------------------------------------


class ExerciseDomainResultDTO(ArbitraryDTO, Generic[DomainResult]):
    """Exercise domain result DTO."""

    status: ExerciseStatusEnum
    case: DomainResult


# =================================================


class TestExerciseConfigDTO(
    ExerciseSettingsDTO,
):
    """Provides test exercise configuration DTO."""

    option_count: int


class OptionValueField(BaseDTO):
    """Option value DTO field."""

    value: int = Field(
        description='Option value',
    )


class PhasesField(ArbitraryDTO):
    """Exercise perform phases DTO field."""

    phases: list[DisplayOrder] = Field(
        description="Current exercise phase's order",
    )
