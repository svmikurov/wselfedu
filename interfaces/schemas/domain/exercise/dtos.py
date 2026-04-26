"""Domain result schemas."""

from dataclasses import dataclass
from typing import Generic, TypeVar, override

from interfaces import enums
from interfaces.schemas.domain.exercise import fields
from interfaces.entity.domain.exercise.fields import Candidate, Candidates
from interfaces.entity.domain.exercise import flow

CandidateT = TypeVar('CandidateT')
CandidatesT = TypeVar('CandidatesT')

DomainResult = TypeVar('DomainResult')


# =================================================
# Exercise domain result
# =================================================


@dataclass
class ExerciseFailure:
    """Exercise failure DTO."""

    exception: Exception


@dataclass(frozen=True)
class PresentationExerciseDomainResult(flow.PresentationDomainResultProtocol):
    """Presentation exercise domain result DTO."""

    option: Candidate
    status: enums.ExerciseStatus
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.PRESENTATION


@dataclass
class TestExerciseDomainResult:
    """Test exercise domain result DTO."""

    question_value: int
    options: Candidates
    exercise_kind: enums.ExerciseKind = enums.ExerciseKind.TEST


# TODO: Implement explain DTO
@dataclass
class ExplainExerciseDomainResult:
    """Presentation exercise domain result DTO."""


# =================================================
# Exercise case
# =================================================


@dataclass
class ExerciseCase(Generic[DomainResult]):
    """Exercise case DTO."""

    status: enums.ExerciseStatus
    domain: DomainResult


@dataclass
class PresentationExerciseCase:
    """Presentation exercise case DTO."""

    status: enums.ExerciseStatus
    domain: PresentationExerciseDomainResult


@dataclass
class TestExerciseCase:
    """Test exercise case DTO."""

    status: enums.ExerciseStatus
    domain: TestExerciseDomainResult


# =================================================
# Exercise task
# =================================================


@dataclass
class Task:
    """Exercise task DTO."""

    status: enums.ExerciseStatus


@dataclass
class PresentationTask(
    fields.QuestionTextField,
    fields.AnswerTextField,
    fields.ProgressValueField,
    Task,
):
    """Presentation exercise task DTO."""


@dataclass
class TestTask(
    fields.OptionValue,
    fields.OptionsField[CandidatesT],
    Task,
):
    """Test exercise task DTO."""
