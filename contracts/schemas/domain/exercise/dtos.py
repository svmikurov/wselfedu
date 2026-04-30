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


class PresentationExerciseDomainResult(ArbitraryDTO, Generic[CandidateT]):
    """Presentation exercise domain result DTO."""

    option: CandidateT
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.PRESENTATION


class TestExerciseDomainResult(ArbitraryDTO, Generic[CandidateT]):
    """Test exercise domain result DTO."""

    option_value: int
    options: CandidateT
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST


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


class PresentationExerciseCase(BaseDTO):
    """Presentation exercise case DTO."""

    status: enums.ExerciseStatus
    domain: PresentationExerciseDomainResult  # type: ignore


class TestExerciseCase(BaseDTO):
    """Test exercise case DTO."""

    status: enums.ExerciseStatus
    domain: TestExerciseDomainResult  # type: ignore


# =================================================
# Exercise task
# =================================================


class Task(BaseDTO):
    """Exercise task DTO."""

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
    fields.OptionsField[CandidatesT],
    Generic[CandidatesT],
    ArbitraryConfigurationMixin,
):
    """Test exercise task DTO."""
