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

DomainResultT = TypeVar('DomainResultT')
TaskT = TypeVar('TaskT')


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


class ExerciseCase(
    BaseDTO,
    Generic[DomainResultT, TaskT],
):
    """Exercise case DTO.

    Parameters
    ----------
    status : `ExerciseStatus`
        Domain create task status, for registry choice.
    domain : `DomainResultT`
        Domain create task result, for user answer handling.
    task : `TaskT`
        Task, for context task representation.

    """

    status: enums.ExerciseStatus
    domain: DomainResultT
    task: TaskT


# =================================================
# Exercise task
# =================================================


# QUESTION: Is deprecated
class Task(BaseDTO):
    """Exercise task DTO.

    Parameters
    ----------
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

    Parameters
    ----------
    question_text : `str`
        Task question text.
    answer_text : `str`
        Task answer text.
    progress_value: `int`
        Current item study progress value.

    """


class TestTask(
    fields.QuestionTextField,
    fields.OptionsField,
    ArbitraryConfigurationMixin,
):
    """Test exercise task DTO.

    Parameters
    ----------
    question_text : `str`
        Test question text.
    options : `Option`
        Test answer options.

    """

    __test__ = False
