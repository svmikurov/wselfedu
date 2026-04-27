"""Domain result schemas."""

from typing import Generic, TypeVar, override, Generic

from interfaces import enums
from interfaces.schemas.base import BaseDTO, ArbitraryDTO
from interfaces.schemas.domain.exercise import fields
from interfaces.entity.domain.exercise.fields import Candidate, Candidates
from interfaces.entity.domain.exercise import flow

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

    question_value: int
    options: CandidateT
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST


# TODO: Implement explain DTO
class ExplainExerciseDomainResult:
    """Presentation exercise domain result DTO."""


# =================================================
# Exercise case
# =================================================


class ExerciseCase(Generic[DomainResult]):
    """Exercise case DTO."""

    status: enums.ExerciseStatus
    domain: DomainResult


class PresentationExerciseCase:
    """Presentation exercise case DTO."""

    status: enums.ExerciseStatus
    domain: PresentationExerciseDomainResult


class TestExerciseCase:
    """Test exercise case DTO."""

    status: enums.ExerciseStatus
    domain: TestExerciseDomainResult


# =================================================
# Exercise task
# =================================================


class Task:
    """Exercise task DTO."""

    status: enums.ExerciseStatus


class PresentationTask(
    fields.QuestionTextField,
    fields.AnswerTextField,
    fields.ProgressValueField,
    Task,
):
    """Presentation exercise task DTO."""


class TestTask(
    fields.OptionValue,
    fields.OptionsField[CandidatesT],
    Task,
):
    """Test exercise task DTO."""
