"""Domain layer contracts."""

from typing import Protocol, TypeVar

from . import enums

T = TypeVar('T')
T_contra = TypeVar('T_contra', contravariant=True)
T_cov = TypeVar('T_cov', covariant=True)


# #################################################
# Components
# #################################################


class HasIdentifier(Protocol):
    @property
    def pk(self) -> int: ...


class HasDefine(Protocol):
    @property
    def define(self) -> str: ...


class HasExplain(Protocol):
    @property
    def explain(self) -> str: ...


class HasQuestionText(Protocol):
    @property
    def question_text(self) -> str: ...


class HasAnswerText(Protocol):
    @property
    def answer_text(self) -> str: ...


class HasAnswerValue(Protocol):
    @property
    def answer_value(self) -> int: ...


class HasQuestionValue(Protocol):
    @property
    def question_value(self) -> int: ...


class HasValue(Protocol):
    @property
    def value(self) -> int: ...


class HasText(Protocol):
    @property
    def text(self) -> str: ...


class HasOptions(Protocol[T]):
    @property
    def options(self) -> list[T]: ...


class HasCorrect(Protocol):
    @property
    def is_correct(self) -> bool: ...


class HasTask(Protocol[T_cov]):
    @property
    def task(self) -> T_cov: ...


class HasExerciseAction(Protocol):
    @property
    def action(self) -> enums.ExerciseAction: ...


# #################################################
# Compositions
# #################################################


class Learnable(
    HasDefine,
    HasExplain,
    Protocol,
): ...


class UniqueLearnable(
    HasIdentifier,
    Learnable,
    Protocol,
): ...


class Presentable(
    HasQuestionText,
    HasAnswerText,
    Protocol,
): ...


class Selectable(
    HasValue,
    HasText,
    Protocol,
): ...


class Testable(
    HasQuestionText,
    HasQuestionValue,
    HasOptions[Selectable],
    Protocol,
): ...


class CheckableOption(
    HasQuestionValue,
    HasAnswerValue,
    Protocol,
): ...


class ExerciseResultProto(
    HasTask[T_cov],
    Protocol,
): ...


###################################################
# Commands
###################################################


class ExerciseCommandProto(
    HasExerciseAction,
    Protocol,
): ...


###################################################
# Events
###################################################


class EventProto(Protocol): ...


###################################################
# Services
###################################################


class CreateTaskServiceProtocol(Protocol[T_cov]):
    def execute(self, candidates: list[UniqueLearnable]) -> T_cov: ...


class AnswerCheckableService(Protocol[T_contra, T_cov]):
    def execute(self, spec: T_contra) -> T_cov: ...


###################################################
# Repositories
###################################################


class CandidatesRepositoryProtocol(Protocol):
    def list(self) -> list[UniqueLearnable]: ...
