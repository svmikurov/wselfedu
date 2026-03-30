"""Test exercise domain DTOs (internal data transfer)."""

from typing import TypeVar

from pydantic import Field

from apps.core.domains.dto import (
    ArbitraryDTO,
    BaseDTO,
    ProtectDefaultStatusMixin,
)

from .. import dto
from .protocol import OptionMetaProtocol

OptionMetaT = TypeVar('OptionMetaT', bound=OptionMetaProtocol)


# =================================================
# Test exercise parameters
# =================================================


class TestExerciseConfigDTO(dto.ExerciseConfigDTO):
    """Provides test exercise configuration DTO."""

    option_count: int


# =================================================
# Test exercise options
# =================================================


class OptionValueField(BaseDTO):
    """Option value DTO field."""

    option_value: int = Field(
        description='Option value',
    )


# =================================================
# Test exercise options
# =================================================


class OptionDTO(
    OptionValueField,
    dto.TextField,
    BaseDTO,
):
    """Test exercise case option.

    Parameter
    ---------
    option_value : `int`
        Test exercise option *value* for answer choice.
    text : `str`
        Test exercise *answer text* option for answer choice.

    """


class OptionMetaDTO(
    dto.ResourceIdentifierField,
    OptionValueField,
    dto.DefineField,
    dto.ExplainField,
    BaseDTO,
):
    """Test exercise case option mapping with item ID.

    Parameter
    ---------
    pk : `int`
        Stored test exercise database identifier.
    option_value : `int`
        Test exercise option value of *correct answer*.
    define : `str`
        Correct question text.
    explain : `str`
        Correct answer text.

    """


class AnswerTextOptionsFiled(BaseDTO):
    """Exercise text options answer DTO field."""

    answer_text_options: list[OptionDTO] = Field(
        description='Display answer text options',
    )


class OptionsField(BaseDTO):
    """Option value DTO field."""

    options: list[OptionMetaDTO] = Field(
        description='Extended option data',
    )


# =================================================
# Create test exercise domain result
# =================================================


class TestExerciseCase(
    dto.ExerciseStatusSchema,
    dto.QuestionTextField,
    AnswerTextOptionsFiled,
    ArbitraryDTO,
):
    """Test exercise case.

    Parameter
    ---------
    status : `ExerciseStatusEnum`
        Current exercise perform status.
    question_text : `str`
        Display question text.
    answer_text_options : `list[OptionDTO]`
        Display answer text options.

    """


class TestExerciseMeta(
    ProtectDefaultStatusMixin,
    dto.ResourceIdentifierField,
    dto.QuestionTextField,
    dto.AnswerTextField,
    OptionValueField,
    OptionsField,
    ArbitraryDTO,
):
    """Test exercise meta to store for answer handle.

    Parameter
    ---------
    pk : `int`
        Stored exercise database item ID.
    question_text : `str`
        Display question text.
    answer_text : `str`
        Display answer text.
    option_value : `int`
        Correct answer option value.
    options : `list[OptionMetaDTO]`
        Exercise's options with them meta data.

    """

    def get_question_text(self, value: int) -> str:
        """Get option question text by value."""
        return self.options[value].define

    def get_answer_text(self, value: int) -> str:
        """Get option answer text by value."""
        return self.options[value].explain
