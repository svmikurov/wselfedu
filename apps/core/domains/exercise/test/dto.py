"""Test exercise domain DTOs (internal data transfer)."""

from typing import Generic, TypeVar

from interfaces.schemas.base import (
    ArbitraryDTO,
    BaseDTO,
    ProtectDefaultStatusMixin,
)
from interfaces.schemas.domain.exercise.fields import (
    AnswerTextField,
    DefineField,
    ExerciseStatusField,
    MeanField,
    OptionsField,
    QuestionTextField,
)
from interfaces.schemas.fields import (
    ResourceIdentifierField,
    TextField,
    ValueField,
)

OptionT = TypeVar('OptionT')


class OptionDTO(
    ValueField,
    TextField,
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
    ResourceIdentifierField,
    ValueField,
    DefineField,
    MeanField,
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


# =================================================
# Create test exercise domain result
# =================================================


class TestExerciseCase(
    ExerciseStatusField,
    QuestionTextField,
    OptionsField[OptionT],
    ArbitraryDTO,
    Generic[OptionT],
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
    ResourceIdentifierField,
    QuestionTextField,
    AnswerTextField,
    ValueField,
    OptionsField[OptionT],
    ArbitraryDTO,
    Generic[OptionT],
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
        return self.options[value].define  # type: ignore

    def get_answer_text(self, value: int) -> str:
        """Get option answer text by value."""
        return self.options[value].mean  # type: ignore


# =================================================
# Experimental test exercise case DTO
# =================================================


class Option(
    DefineField,
    MeanField,
    BaseDTO,
):
    """Exercise case option DTO."""


class TestDomainResult(
    ValueField,
    OptionsField[OptionT],
    ArbitraryDTO,
):
    """Test exercise create domain result."""

    @property
    def question_text(self) -> str:
        """Get question text."""
        return self.options[self.value - 1].define  # type: ignore

    @property
    def answer_text(self) -> str:
        """Get answer text."""
        return self.options[self.value - 1].mean  # type: ignore
