"""Protocols for domain layer interface."""

from typing import Protocol, TypeVar

T = TypeVar('T')
T_cov = TypeVar('T_cov', covariant=True)
T_contra = TypeVar('T_contra', contravariant=True)


# #################################################
# Components
# #################################################


class HasLearnables(Protocol[T_cov]):
    @property
    def learnables(self) -> T_cov: ...


class HasIdentifier(Protocol):
    @property
    def pk(self) -> int: ...


class HasDefine(Protocol):
    @property
    def define(self) -> str: ...


class HasExplain(Protocol):
    @property
    def explain(self) -> str: ...


class HasQuestionValue(Protocol):
    @property
    def question_value(self) -> int: ...


class HasQuestionText(Protocol):
    @property
    def question_text(self) -> str: ...


class HasAnswerValue(Protocol):
    @property
    def answer_value(self) -> int: ...


class HasOptionValue(Protocol):
    @property
    def option_value(self) -> int: ...


class HasOptionText(Protocol):
    @property
    def option_text(self) -> str: ...


class HasOptions(Protocol[T]):
    @property
    def options(self) -> list[T]: ...


class HasSessionIdentifier(Protocol):
    @property
    def session_id(self) -> str: ...


class HasIsCorrect(Protocol):
    @property
    def is_correct(self) -> bool: ...


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


class Selectable(
    HasOptionValue,
    HasOptionText,
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


###################################################
# Services
###################################################


class ExerciseCreatable(Protocol[T_contra, T_cov]):
    def create(self, spec: T_contra) -> T_cov: ...


class AnswerCheckable(Protocol[T_contra, T_cov]):
    def check(self, spec: T_contra) -> T_cov: ...


###################################################
# Input interfaces
###################################################


class Repository(Protocol[T]):
    def add(self, item: T) -> None: ...
    def get(self, key: str) -> T: ...
    def list(self) -> list[T]: ...
