"""Domain result schemas."""

from typing import Generic, TypeVar

from contracts import enums
from contracts.schemas.base import (
    ArbitraryConfigurationMixin,
    ArbitraryDTO,
    BaseDTO,
)
from contracts.schemas.domain.exercise import fields

CandidateT = TypeVar('CandidateT')
CandidatesT = TypeVar('CandidatesT')

DomainResult = TypeVar('DomainResult')


# =================================================
# Exercise domain result
# =================================================


class ExerciseFailure(ArbitraryDTO):
    """Exercise failure DTO."""

    exception: Exception


# TODO: Implement explain DTO
class ExplainExerciseDomainResult(BaseDTO):
    """Presentation exercise domain result DTO."""


# =================================================
# Exercise case
# =================================================


class ExerciseCase(BaseDTO, Generic[DomainResult]):
    """Exercise case DTO."""

    status: enums.ExerciseStatus
    domain: DomainResult


# =================================================
# Exercise task
# =================================================


class Task(BaseDTO):
    """Exercise task DTO.

    Parameter
    ---------
    status : `ExerciseStatus`
        Current exercise status enumeration.
    """

    status: enums.ExerciseStatus


class PresentationTask(
    Task,
    fields.QuestionTextField,
    fields.AnswerTextField,
    fields.ProgressValueField,
):
    """Presentation exercise task DTO.

    Parameter
    ---------
    status : `ExerciseStatus`
        Current exercise status enumeration.
    question_text : `str`
        Task question text.
    answer_text : `str`
        Task answer text.
    progress_value: `int`
        Current item study progress value.
    """


class TestExerciseTask(
    Task,
    fields.OptionValue,
    fields.TaskItemsField[CandidatesT],
    Generic[CandidatesT],
    ArbitraryConfigurationMixin,
):
    """Test exercise task DTO.

    Parameter
    ---------
    status : `ExerciseStatus`
        Current exercise status enumeration.
    option_value : `int`
        The question's option value (options index value).
    options : list[CandidatesT]
        The exercise test's options.
    """
