"""Test exercise domain DTOs (internal data transfer)."""

from typing import Generic, TypeVar

from contracts.schemas.base import (
    ArbitraryDTO,
    BaseDTO,
)
from contracts.schemas.domain.exercise.fields import (
    DefineField,
    ExerciseStatusField,
    MeanField,
    QuestionTextField,
    TaskItemsField,
)
from contracts.schemas.fields import (
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
    TaskItemsField[OptionT],
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
