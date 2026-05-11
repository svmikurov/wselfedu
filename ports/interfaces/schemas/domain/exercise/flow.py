"""Domain result schemas."""

from typing import Generic, TypeVar

from ports.contract import enums
from ports.interfaces.schemas.base import (
    ArbitraryConfigurationMixin,
    ArbitraryDTO,
    BaseDTO,
)
from ports.interfaces.schemas.domain.exercise import fields

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


# QUESTION: Is deprecated
class Task(BaseDTO):
    """Exercise task DTO.

    Parameter
    ---------
    status : `ExerciseStatus`
        Current exercise status enumeration.
    """

    status: enums.ExerciseStatus


class PresentationTask(
    fields.QuestionTextField,
    fields.AnswerTextField,
    fields.ProgressValueField,
):
    """Presentation exercise task DTO.

    Parameter
    ---------
    question_text : `str`
        Task question text.
    answer_text : `str`
        Task answer text.
    progress_value: `int`
        Current item study progress value.
    """


class TestExerciseTask(
    fields.OptionValue,
    fields.QuestionTextField,
    fields.TaskItemsField[CandidatesT],
    Generic[CandidatesT],
    ArbitraryConfigurationMixin,
):
    """Test exercise task DTO.

    Parameter
    ---------
    option_value : `int`
        The question's option value (options index value).
    question_text : `str`
        Task question text.
    options : list[CandidatesT]
        The exercise test's options.
    """

    __test__ = False
